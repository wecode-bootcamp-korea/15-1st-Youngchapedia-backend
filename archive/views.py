import json

from django.http  import JsonResponse
from django.views import View
from django.utils import timezone

from archive.models import Rating, ArchiveType, Archive
from content.models import Content
from user.models    import User
# from user.utils     import id_auth

class RatingView(View):
#    @id_auth
    def post(self, request, content_pk):
        try:
            data   = json.loads(request.body)
            print(data)
            # user = request.user
            user    = User.objects.get(id=data['user'])
            content = Content.objects.get(id=content_pk)
            rating  = data['rating']

            if Rating.objects.filter(user = user, content = content):
                return JsonResponse({"message": "ALREADY_EIXST"}, status = 400)

            Rating.objects.create(user = user, content = content, rating = rating)
            return JsonResponse({"message": "SUCCESS"}, status = 201)
        
        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
    def get(self, request):
        try:
            data = json.loads(request.body)
            results = [] 

            if data.get('user') and data.get('content'):
                ratings = Rating.objects.filter(user_id = data['user'], content = ['content'])
            elif data.get('user'):
                ratings = Rating.objects.filter(user_id = data['user'])
            elif data.get('content'):
                ratings = Rating.objects.filter(content_id = data['content'])
            else:
                raise KeyError

            if ratings.exists: 
                for rating in ratings:
                    results.append(
                        {
                            "id"      : rating.id,
                            "user"    : User.objects.get(id=rating.user_id).usernmae,
                            "content" : Content.objects.get(id=rating.content_id).title_korean,
                            "rating"  : rating.rating
                        }
                    )   
                return JsonResponse({"result": results}, status = 200)
            return JsonResponse({"message": "NO_RESULT"}, status = 400)

        except json.JSONDecodeError as e:
            return JsonResponse({"message" f"{e}"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
    
