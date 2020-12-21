import json

from django.http      import JsonResponse
from django.shortcuts import render
from django.views     import View

from review.models  import Review, ReviewLike
from user.models    import User
from user.utils     import id_auth
from archive.models import Rating, Archive
from content.models import Content


class ReviewView(View):
    @id_auth
    def post(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id = content_pk)
            body    = data['review']

            if Review.objects.filter(user = user, content = content).exists():
                return JsonResponse({"message": "ALREADY_EXIST"}, status = 400)

            Review.objects.create(user = user, content = content, body = body)
            return JsonResponse({"message": "SUCCESS"}, status = 201)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_CONTENT"}, status = 400)

    @id_auth
    def get(self, request, content_pk):
        try:
            user = request.user
            if Content.objects.filter(id = content_pk).exists():
                my_review = Review.objects.get(user = user, content_id = content_pk)
                reviews = Review.objects.filter(content_id = content_pk)
                results = []
                for review in reviews:
                    results.append(
                        {
                            "id"     : review.id,
                            "user_id": review.user_id,
                            "user"   : review.user.username,
                            "content": review.content.title_korean,
                            "review" : review.body
                        }
                    )
                my_review_result = { 
                        "id" : my_review.id, 
                        "user_id": my_review.user_id, 
                        "user": my_review.user.username, 
                        "content": my_review.content.title_korean, 
                        "review": my_review.body
                        }
                return JsonResponse({"my_result": my_review_result, "result": results}, status = 200)
            return JsonResponse({"message": "INVALID_CONTENT_ID"}, status = 400)
        except Review.DoesNotExist:
            return JsonResponse({"message": "MY_REVIEW_DOES_NOT_EXIST"}, status = 400)
        
    @id_auth
    def patch(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id = content_pk)
            body    = data['review']

            patch_object = Review.objects.get(user = user, content = content)
            patch_object.body = body
            patch_object.save()
            return JsonResponse({"message": "REVIEW_UPDATED"}, status = 201)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status = 400)
        except Review.DoesNotExist:
            return JsonResponse({"message": "NO_REVIEW"}, status = 400)
    @id_auth
    def delete(self, request, content_pk):
        user   = request.user
        content = Content.objects.get(id=content_pk)

        if Review.objects.filter(user = user, content = content).exists():
            Review.objects.get(user = user, content = content).delete()
            return JsonResponse({"message": "REVIEW_DELETED"}, status = 204)
        return JsonResponse({"message": "NOT_RATED"}, status = 400)


class ContentReviewView(View):
    def get(self, request, content_pk):
        try:
            content  = Content.objects.get(id = content_pk)
            if Review.objects.filter(content = content).exists():
                reviews  = Review.objects.select_related('user').prefetch_related('user__rated_movie', 'liked_user', 'user__archives').filter(content = content_pk)
                # reviews  = Review.objects.filter(content = content_pk)
                
                results = []

                for review in reviews:
                    if Rating.objects.filter(user = review.user, content = content).exists():
                        rating  = Rating.objects.get(user = review.user, content = content).rating
                        archive = ''
                    elif Archive.objects.filter(user = review.user, content = content).exists():
                        rating  = ''
                        archive = Archive.objects.get(user = review.user, content = content).archive_type
                    else:
                        rating  = ''
                        archive = ''
                    likes = ReviewLike.objects.filter(review_id = review.id).count()
                    results.append(
                        {
                            "id"         : review.id,
                            "user_id"    : review.user.id,
                            "user"       : review.user.username,
                            "rating"     : rating,
                            "archive"    : archive,
                            "review"     : review.body,
                            "created_at" : review.created_at,
                            "updated_at" : review.updated_at,
                            "likes"      : likes
                        }
                    )
                return JsonResponse({"result": results}, status = 200)
            return JsonResponse({"results": []}, status = 200)
        except Content.DoesNotExist:
            return JsonResponse({"message": "UNVALID_CONTENT"}, status = 400)


class ReviewLikeView(View):
    @id_auth
    def post(self, request, review_pk):
        try:
            user   = request.user
            review = Review.objects.get(id = review_pk)
            
            if ReviewLike.objects.filter(user = user, review = review).exists():
                return JsonResponse({"message": "ALREADY_LIKED"}, status = 400)
            ReviewLike.objects.create(user = user, review = review)
            return JsonResponse({"message": "SUCCESS"}, status = 203)
        except ReviewLike.DoesNotExist:
            return JsonResponse({"message": "UNVALID_REVIEW"}, status = 400)

    @id_auth
    def delete(self, request, review_pk):
        try:
            user       = request.user
            review     = Review.objects.get(id = review_pk)
            reviewlike = ReviewLike.objects.get(user = user, review = review)
            reviewlike.delete()
            return JsonResponse({"message": "LIKE_DELETED"}, status = 204)
        except Review.DoesNotExist:
            return JsonResponse({"message": "INVALID_REVIEW"}, status = 400)

