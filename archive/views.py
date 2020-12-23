import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg

from archive.models import Rating, ArchiveType, Archive
from archive.utils  import calculate_ratings
from content.models import Content
from user.models    import User
from user.utils     import id_auth


class RatingView(View):
    @id_auth
    def post(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id=content_pk)
            rating  = data['rating']

            if Rating.objects.filter(user = user, content = content).exists():
                return JsonResponse({"message": "ALREADY_EIXST"}, status = 400)

            Rating.objects.create(user = user, content = content, rating = rating)
            return JsonResponse({"message": "SUCCESS"}, status = 201)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

    @id_auth
    def get(self, request, content_pk):
        try:
            user    = request.user
            result  = {
                            "id"      : user.rated_contents.get(content_id = content_pk).id,
                            "rating"  : user.rated_contents.get(content_id = content_pk).rating,
                      }
            return JsonResponse({"result": result}, status = 200)

        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_CONTENT"}, status = 400)
        except Rating.DoesNotExist:
            return JsonResponse({"message": "INVALID_RATING"}, status = 400)

    @id_auth
    def patch(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id=content_pk)
            rating  = data['rating']

            patch_object = Rating.objects.get(user = user, content = content)

            if patch_object.rating == float(rating):
                return JsonResponse({"message": "SAME_RATING_SCORE"}, status = 400)
            patch_object.rating = rating
            patch_object.save()
            return JsonResponse({"message": "RATING_UPDATED"}, status = 201)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status = 400)
        except Rating.DoesNotExist:
            return JsonResponse({"message": "INVALID_RATING"}, status = 400)

    @id_auth
    def delete(self, request, content_pk):
        user = request.user
        content = Content.objects.get(id=content_pk)

        if Rating.objects.filter(user = user, content = content).exists():
            Rating.objects.get(user = user, content = content).delete()
            return JsonResponse({"message": "RATING_DELETED"}, status = 203)
        return JsonResponse({"message": "NOT_RATED"}, status = 400)


class ArchiveView(View):
    @id_auth
    def post(self, request, content_pk):
        try:
            data        = json.loads(request.body)
            user        = request.user
            content     = Content.objects.get(id=content_pk)
            archivetype = ArchiveType.objects.get(id=data['archive_type'])

            if user.archived_contents.filter(content_id = content_pk).exists():
                return JsonResponse({"message": "ALREADY_EXIST"}, status = 400)

            Archive.objects.create(user = user, content = content, archive_type = archivetype)
            return JsonResponse({"message": "SUCCESS"}, status = 200)
        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_CONTENT"}, status = 400)
        except ArchiveType.DoesNotExist:
            return JsonResponse({"message": "INVALID_ARCHIVETYPE"}, status = 400)

    @id_auth
    def get(self, request, content_pk):
        try:
            user = request.user

            if user.archived_contents.filter(content = content_pk).exists():
                archive = Archive.objects.get(user = user, content = content_pk)
                return JsonResponse({"archive_type" : archive.archive_type.name}, status = 200)
            return JsonResponse({"archive_type" : ''}, status = 200)
        except Archive.DoesNotExist:
            return JsonResponse({"message": "INVALID_ARCHIVE"}, status = 400)

    @id_auth
    def patch(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id = content_pk)
            archivetype = ArchiveType.objects.get(id = data['archivetype'])

            if Archive.objects.filter(user = user, content = content).exists():
                patch_object = Archive.objects.get(user = user, content = content)
                if patch_object.archive_type == archivetype:
                    return JsonResponse({"message": "SAME_ARCHIVETYPE"}, status = 400)
                patch_object.archive_type = archivetype
                patch_object.save()
                return JsonResponse({"message": "ARCHIVE_UPDATED"}, status = 200)
            return JsonResponse({"message": "INVALID_ARCHIVE"}, status = 400)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_CONTENT"}, status = 400)
        except ArchiveType.DoesNotExist:
            return JsonResponse({"message": "INVALID_ARCHIVETYPE"}, status = 400)

    @id_auth
    def delete(self, request, content_pk):
        try:
            user = request.user
            content = Content.objects.get(id = content_pk)

            Archive.objects.get(user = user, content = content).delete()
            return JsonResponse({"message": "NO_CONTENT"}, status = 204)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_CONTENT"}, stauts = 400)
        except Archive.DoesNotExist:
            return JsonResponse({"message": "INVALID_ARCHIVE"}, status = 400)


class ContentRatingView(View):
    def get(self, request, content_pk):
        try:
            content = Content.objects.get(id = content_pk)
            ratings = content.rating_users.all().select_related('user', 'content')
            results = [{
                        "id"      : rating.id,
                        "user_id" : rating.user_id,
                        "user"    : rating.user.username,
                        "content" : rating.content.title_korean,
                        "rating"  : rating.rating
                      } for rating in ratings]

            average_rating = calculate_ratings(content_pk)
            return JsonResponse({"result": results, "avg_rating": average_rating['rating__avg']}, status = 200)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_CONTENT"}, status = 400)


class UserMainView(View):
    @id_auth
    def get(self, request):
        user  = request.user
        rated = Rating.objects.filter(user = user).count()
        wish  = Archive.objects.filter(user = user, archive_type_id = 1).count()
        watch = Archive.objects.filter(user = user, archive_type_id = 2).count()
        return JsonResponse({"username": user.username, "rate": rated, "wish": wish, "watching": watch}, status = 200)


class UserArchiveView(View):
    @id_auth
    def get(self, request):
        try:
            user        = request.user
            archivetype = request.GET['archive_type']
            if Archive.objects.filter(user = user, archive_type = archivetype).exists():
                archives    = Archive.objects.filter(user = user, archive_type = archivetype).select_related('content')
                results     = [{
                                "id"            : archive.id,
                                "content_id"    : archive.content.id,
                                "content_title" : archive.content.title_korean,
                                "content_image" : archive.content.main_image_url,
                                "rating"        : calculate_ratings(archive.content_id)['rating__avg'],
                                "updated_at"    : archive.updated_at,
                            } for archive in archives]

                return JsonResponse({"result": results}, status = 200)
            return JsonResponse({"result": []}, status = 200)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status = 400)
        except ArchiveType.DoesNotExist:
            return JsonResponse({"message": "INVALID_ARCHIVETYPE"}, status = 400)


class UserRatingView(View):
    @id_auth
    def get(self, request):
        try:
            user    = request.user
            if Rating.objects.filter(user = user).exists():
                ratings = Rating.objects.filter(user = user).select_related('content')
                results = [{
                            "id"            : rating.id,
                            "content_id"    : rating.content.id,
                            "content_title" : rating.content.title_korean,
                            "content_image" : rating.content.main_image_url,
                            "rating"        : rating.rating,
                            "updated_at"    : rating.updated_at,
                            } for rating in ratings]

                return JsonResponse({"result": results}, status = 200)
            return JsonResponse({"result": []}, status = 200)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status = 400)
