import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from content.models   import ContentPeople, ContentGenre, ContentTag, Content, People, Genre
from content.models   import Tag, MovieOverview, ContentAvailableService, ContentService, ContentPhoto

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
            results = [
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


class ContentOverview(View):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)

            result = {
                'content_id'     : content.id,
                'title_original' : content.movieoverview_set.all()[0].title_original,
                'release_year'   : content.release_year,
                'genre'          : [genre.genre.name for genre in content.contentgenre_set.all()],
                'runtime'        : content.movieoverview_set.all()[0].runtime,
                'description'    : content.movieoverview_set.all()[0].description,
            }
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENTS_ID'}, status=400)


class ContentCast(View):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)

            results = [
                {
                    'people_id'        : people.people.id,
                    'people_name'      : people.people.name,
                    'role'             : people.role_name,
                    'people_image_url' : people.people.profile_image_url,
                } for people in content.contentpeople_set.all().select_related('people')
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENT_ID'}, status=400)


class WatchaContent(View):
    def get(self, request):
        content_services = ContentService.objects.get(name='watcha')
        watcha_content_list = [
            {
                'id'             : watcha_content.content.id,
                'title_korean'   : watcha_content.content.title_korean,
                'title_original' : watcha_content.content.movieoverview_set.all()[0].title_original,
                'category'       : watcha_content.content.category.name,
                'main_image_url' : watcha_content.content.main_image_url,
            } for watcha_content in content_services.contentavailableservice_set.all().select_related('content').prefetch_related('content__category', 'content__movieoverview_set')
        ]

        results = {
                'service_id'   : content_services.id,
                'service_name' : content_services.name,
                'contents'     : watcha_content_list,
            }
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)


class NetflixContent(View):
    def get(self, request):
        content_services = ContentService.objects.get(name='netflix')
        netflix_content_list = [
            {
                'id'             : netflix_content.content.id,
                'title_korean'   : netflix_content.content.title_korean,
                'title_original' : netflix_content.content.movieoverview_set.all()[0].title_original,
                'category'       : netflix_content.content.category.name,
                'main_image_url' : netflix_content.content.main_image_url,
            } for netflix_content in content_services.contentavailableservice_set.all().select_related('content').prefetch_related('content__category', 'content__movieoverview_set')
        ]

        results = {
                'service_id'   : content_services.id,
                'service_name' : content_services.name,
                'contents'     : netflix_content_list,
            }
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)


class ContentGallery(View):
    def get(self, request, content_id):
        try:
            content            = Content.objects.get(id=content_id)
            gallery_photo_list = [gallery_photo.photo_url for gallery_photo in content.contentphoto_set.all()]

            results = {
                'content_id'           : content.id,
                'content_title_korean' : content.title_korean,
                'gallery_images'       : gallery_photo_list,
                }
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENT_ID'}, status=400)


class ContentSearch(View):
    def get(self, request):
        search_keyword = request.GET.get('keyword', None)
        content_list = ContentPeople.objects.filter(Q(content__title_korean__contains=search_keyword) |Q(people__name=search_keyword)).select_related('content')
        results = [
            {
                'id' : content.id,
                'title_korean' : content.content.title_korean,
                'main_image_url' : content.content.main_image_url,
                'release_year' : content.content.release_year,
            }
            for content in content_list
        ]
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results})
