import json

from django.http    import JsonResponse
from django.views   import View

from content.models import ContentPeople, ContentGenre, ContentTag, Content, People, Genre, Tag, MovieOverview, ContentAvailableService, ContentService, ContentPhoto

# Create your views here.

class PeopleContent(View):
    def get(self, request, people_id):
        try:
            people       = People.objects.get(id=people_id)
            jobs         = people.contentpeople_set.all()
            job_list     = list(set([job.job.name for job in jobs]))
            contents     = ContentPeople.objects.filter(people_id=people_id)
            content_list = []

            for content in contents:
                content_list.append(
                    {
                        'id'             : content.content.id,
                        'title_korean'   : content.content.title_korean,
                        'title_original' : content.content.movieoverview_set.get().title_original,
                        'category'       : content.content.category.name,
                        'main_image_url' : content.content.main_image_url,
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
            contents     = ContentGenre.objects.filter(genre_id=genre_id)
            content_list = []

            for content in contents:
                content_list.append(
                    {
                        'id'             : content.content.id,
                        'title_korean'   : content.content.title_korean,
                        'title_original' : content.content.movieoverview_set.get().title_original,
                        'category'       : content.content.category.name,
                        'main_image_url' : content.content.main_image_url,
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
            contents     = ContentTag.objects.filter(tag_id=tag_id)
            content_list = []

            for content in contents:
                content_list.append(
                    {
                        'id'             : content.content.id,
                        'title_korean'   : content.content.title_korean,
                        'title_original' : content.content.movieoverview_set.get().title_original,
                        'category'       : content.content.category.name,
                        'main_image_url' : content.content.main_image_url,
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
            content          = Content.objects.get(id=content_id)
            content_overview = content.movieoverview_set.get()
            genres           = content.contentgenre_set.all()

            result = [
                {
                    'content_id'     : content.id,
                    'title_original' : content_overview.title_original,
                    'release_year'   : content.release_year,
                    'genre'          : [genre.genre.name for genre in genres],
                    'runtime'        : content_overview.runtime,
                    'description'    : content_overview.description,
                }
            ]
            return JsonResponse({'MESSAGE' : result}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENTS_ID'}, status=400)


class ContentCast(View):
    def get(self, request, content_id):
        try:
            content     = Content.objects.get(id=content_id)
            people_list = content.contentpeople_set.all()

            result = [
                {
                    'people_id'        : people.people.id,
                    'people_name'      : people.people.name,
                    'role'             : people.role_name,
                    'people_image_url' : people.people.profile_image_url,
                } for people in people_list
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENT_ID'}, status=400)


class WatchaContent(View):
    def get(self, request):
        service = ContentService.objects.get(name='watcha')
        watcha_contents = ContentAvailableService.objects.filter(content_service_id=service.id)
        watcha_content_list = [
            {
                'id'             : watcha_content.content.id,
                'title_korean'   : watcha_content.content.title_korean,
                'title_original' : watcha_content.content.movieoverview_set.get().title_original,
                'category'       : watcha_content.content.category.name,
                'main_image_url' : watcha_content.content.main_image_url,
            } for watcha_content in watcha_contents
        ]

        results = [
            {
                'service_id'   : service.id,
                'service_name' : service.name,
                'contents'     : watcha_content_list,
            }
        ]
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)


class NetflixContent(View):
    def get(self, request):
        service              = ContentService.objects.get(name='netflix')
        netflix_contents     = ContentAvailableService.objects.filter(content_service_id=service.id)
        netflix_content_list = [
            {
                'id'             : netflix_content.content.id,
                'title_korean'   : netflix_content.content.title_korean,
                'title_original' : netflix_content.content.movieoverview_set.get().title_original,
                'category'       : netflix_content.content.category.name,
                'main_image_url' : netflix_content.content.main_image_url,
            } for netflix_content in netflix_contents
        ]

        results = [
            {
                'service_id'   : service.id,
                'service_name' : service.name,
                'contents'     : netflix_content_list,
            }
        ]
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)


class ContentGallery(View):
    def get(self, request, content_id):
        try:
            content            = Content.objects.get(id=content_id)
            gallery_photos     = ContentPhoto.objects.filter(content_id=content_id)
            gallery_photo_list = [gallery_photo.photo_url for gallery_photo in gallery_photos]

            results = [
                {
                'content_id'           : content.id,
                'content_title_korean' : content.title_korean,
                'galleris_image'       : gallery_photo_list,
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENT_ID'}, status=400)





