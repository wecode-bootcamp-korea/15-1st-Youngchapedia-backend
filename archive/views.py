import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg

from archive.models import Rating, ArchiveType, Archive
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

    def get(self, request, content_pk):
        if Content.objects.filter(id = content_pk).exists():
            ratings     = Rating.objects.filter(content = content_pk)
            results     = []
        
            for rating in ratings:
                results.append(
                    {
                        "id"      : rating.id,
                        "user_id" : rating.user_id,
                        "user"    : rating.user.username,
                        "content" : rating.content.title_korean,
                        "rating"  : rating.rating
                    }
                )
            average_rating = ratings.aggregate(Avg('rating'))
            return JsonResponse({"result": results, "avg_rating": average_rating['rating__avg']}, status = 200)
        return JsonResponse({"message": "INVALID_CONTENT_ID"}, status = 400)

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
            

