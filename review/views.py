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

        

class UserReviewView(View):
    def temp(self):
        print("Under Contruction")
