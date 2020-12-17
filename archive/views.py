from django.shortcuts import render

from django.http import JsonResponse
from django.views import View

from archive.models import Rating, ArchiveType, Archive
from content.models import Content



class RatingView(view):
#    @id_auth
    def post(self, request):
        try:
            data = json.loads(request.body)

            # user = request.user
            user    = Content.obejcts.get(data['user'])
            content = Content.objects.get(data['content'])
            rating  = data['rating']
            
            if Rating.objects.filter(user = user, content = content):
                if Rating.objects.filter(user = user, content = content, rating = rating):
                    Rating.objects.get(user = user, content = content, rating = rating).delete()
                elif:
                    Rating.objects.update(rating = rating)
            else:
                Rating.objects.create(user = user, content = content, rating = rating)
            return JsonResponse({"message": "SUCCESS"}, status = 200)
        
        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except KeyError:
            retrun JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
    def get(self, request):
        try:
            data = json.loads(request.body)

            user = data.get('user')
            content = data.get('content')

            results = []
            ratings = Rating.objects.filter(user = 

            for post in ratings:
                results.append(
                    {
                        "user"
    
                    }
                )
