from django.http  import JsonResponse
from django.views import View
from django.utils import timezone

from archive.models import Rating, ArchiveType, Archive
from content.models import Content
from user.models    import User


class RatingView(View):
#    @id_auth
    def post(self, request):
        try:
            data = json.loads(request.body)

            # user = request.user
            user    = Content.obejcts.get(data['user'])
            content = Content.objects.get(data['content'])
            rating  = data['rating']

            if Rating.objects.filter(user_id = user, content_id = content):
                exist_rating = Rating.objects.get(user_id = user, content_id = content)
                if exist_rating.rating == rating:
                    exist_rating.delete()
                    return JsonResponse({"message": "RATING_DELETED"}, status = 200)
                else:
                    exist_rating.update(rating = rating)
                    return JsonResponse({"message": "RATING_UPDATED"}, status = 200)

            Rating.objects.create(user_id = user, content_id = content, rating = rating)
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
