import json

from django.http    import JsonResponse
from django.views   import View

from content.models import ContentPeople, ContentGenre, ContentTag, Content, People, Genre, Tag

# Create your views here.

class PeopleContent(View):
    def get(self, request, people_id):
        try:
            people       = People.objects.get(id=people_id)
            jobs         = people.contentpeople_set.all()
            job_list     = list(set([job.job.name for job in jobs]))
            contents     = Content.objects.filter(id__in = ContentPeople.objects.filter(people = people)).select_related('category').prefetch_related('movieoverview_set') 
            #contents     = ContentPeople.objects.filter(people_id=people_id).select_related('content', 'people')
            content_list = []

            for content in contents:
                content_list.append(
                    {
                        'id'             : content.id,
                        'title_korean'   : content.title_korean,
                        'title_original' : content.movieoverview_set.all()[0].title_original,
                        'category'       : content.category.name,
                        'main_image_url' : content.main_image_url,
                    }
                )
            results      = [
                {
                    'id'                : people.id,
                    'name'              : people.name,
                    'title'             : job_list,
                    'profile_image_url' : people.profile_image_url,
                    'contents'          : content_list,
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except People.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_PEOPLE_ID'}, status=400)


class GenreContent(View):
    def get(self, request, genre_id):
        try:
            genre        = Genre.objects.get(id=genre_id)
            contents     = Content.objects.filter(id__in = ContentGenre.objects.filter(genre = genre)).select_related('category').prefetch_related('movieoverview_set')
            #contents     = ContentGenre.objects.filter(genre_id=genre_id)
            content_list = []

            for content in contents:
                content_list.append(
                    {
                        'id'             : content.id,
                        'title_korean'   : content.title_korean,
                        'title_original' : content.movieoverview_set.all()[0].title_original,
                        'category'       : content.category.name,
                        'main_image_url' : content.main_image_url,
                    }
                )
            results      = [
                {
                    'genre_id'   : genre.id,
                    'genre_name' : genre.name,
                    'contents'   : content_list,
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Genre.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INAVLID_GENRE_ID'}, status=400)

class TagContent(View):
    def get(self, request, tag_id):
        try:
            tag          = Tag.objects.get(id=tag_id)
            
            contents     = Content.objects.filter(id__in = ContentTag.objects.filter(tag = tag)).select_related('category').prefetch_related('movieoverview_set')
            content_list = []

            for content in contents:
                content_list.append(
                    {
                        'id'             : content.id,
                        'title_korean'   : content.title_korean,
                        'title_original' : content.movieoverview_set.all()[0].title_original,
                        'category'       : content.category.name,
                        'main_image_url' : content.main_image_url,
                    }
                )
            results      = [
                {
                    'tag_id'   : tag.id,
                    'tag_name' : tag.name,
                    'contents' : content_list,
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Tag.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_TAG_ID'}, status=400)


class ContentDetail(View):
    def get(self, request, content_id):
        try:
            content   = Content.objects.get(id=content_id)
            genres    = content.contentgenre_set.all()
            countries = content.contentcountry_set.all()

            results = [
                {
                    'content_id'     : content.id,
                    'title_korean'   : content.title_korean,
                    'main_image_url' : content.main_image_url,
                    'release_year'   : content.release_year,
                    'genre'          : [genre.genre.name for genre in genres],
                    'country'        : [country.country.name for country in countries],
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENT_ID'}, status=400)
