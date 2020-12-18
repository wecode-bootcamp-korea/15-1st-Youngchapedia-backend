import json

from django.shortcuts import render
from django.utils     import timezone
from django.views     import View

from review.models  import Review
from user.models    import User
from user.utils     import id_auth
from content.models import Content


class ReviewView(View):
    @id_auth
    def post(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id = content_pk)
            body    = data['review']

            if Review.objects.filter(user = user, content = content):
                return JsonResponse({"message": "ALREADY_EXIST"}, status = 400)

            Rating.objects.create(user = user, content = content, body = body)
            return JsonResponse({"message": "SUCCESS"}, status = 201)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
    def get(self, request, content_pk):
        if not Content.objects.filter(id = content_pk):
            return JsonResponse({"message": "INVALID_CONTENT_ID"}, status = 400)
        reviews = Review.objects.get(id = content_pk)
        results = []

        for review in reviews:
            results.append(
                {
                    "id"   :review.id,
                    "user" : User.objects.get(id=rating.user_id).username,
                    "content": Content.objects.get(id=rating.content_id).title_korean,
                    "review" : raview.body
                }
            )

        return JsonResponse({"result": results}, status = 200)

    @id_auth
    def patch(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id = content_pk)
            body    = data['review']

            patch_object = Review.objects.get(user = user, content = content)
            patch_object.body = body
            patch_object.updated_at = timezone.now()
            
            patch_object.save()
            return JsonResponse({"message": "REVIEW_UPDATED"}, staus = 201)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except Content.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status = 400)

    @id_auth
    def delete(self, request, contetn_pk):
        user   = request.user
        content = Content.objects.get(id=content_pk)

        if Review.objects.filter(user = user, content = content).exists():
            Review.objects.get(user = user, content = content).delete()
            return JsonResponse({"message": "REVIEW_DELETED"}, status = 203)
        return JsonResponse({"message": "NOT_RATED"}, status = 400)

class UserReviewView(View):
    def temp(self):
        print("Under Contruction")
