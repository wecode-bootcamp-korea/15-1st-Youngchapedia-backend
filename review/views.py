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
            
            review, created = Review.objects.get_or_create(user    = user, 
                                                           content = content)
            if created:
                review.body = data['body']
                review.save()
                return JsonResponse({"message": "SUCCESS"}, status = 201)

            return JsonResponse({"message": "ALREADY_EXIST"}, status = 400)
 
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
            if Review.objects.filter(id = content_pk).exists():
                my_review = Review.objects.select_related('user', 'content').get(user = user, content_id = content_pk)
                my_review_result = { 
                        "id"           : my_review.id, 
                        "user_id"      : my_review.user_id, 
                        "user"         : my_review.user.username, 
                        "user_profile" : my_review.user.profile_image_url,
                        "content"      : my_review.content.title_korean, 
                        "review"       : my_review.body,
                        }
                return JsonResponse({"my_result": my_review_result}, status = 200)
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
                reviews  = Review.objects.select_related('user').prefetch_related('liked_users').filter(content = content_pk)
                
                results = [
                            {
                                "id"           : review.id,
                                "user_id"      : review.user.id,
                                "user"         : review.user.username,
                                "user_profile" : review.user.profile_image_url,
                                "rating"       : review.user.rated_contents.get(content_id = content_pk).rating if Rating.objects.filter(user=review.user, content = content).exists() else '',
                                "archive"      : review.user.archived_contents.get(content_id = content_pk).archive_type_id if Archive.objects.filter(user=review.user, content=content).exists() else '',
                                "review"       : review.body,
                                "created_at"   : review.created_at,
                                "updated_at"   : review.updated_at,
                                "likes"        : review.liked_users.count(),
                            } for review in reviews  
                        ]

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
            
            like, created = ReviewLike.objects.get_or_create(user = user, review = review) 
            if not created:
                return JsonResponse({"message": "ALREADY_LIKED"}, status = 400)
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

