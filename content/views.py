import json

from django.http    import JsonResponse
from django.views   import View

<<<<<<< HEAD
from content.models import ContentPeople, ContentGenre, ContentTag, ContentService, Content, People, Genre, Tag, ContentAvailableService

# Create your views here.
=======
from content.models import ContentPeople, ContentGenre, ContentTag

# Create your views here.

>>>>>>> 873941224ba16b7348479fd65f7c3d3e8b02a5d6
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
<<<<<<< HEAD
            results = [
=======

            for content in content_list:
                content_list = dict(tuple(content.items()))

            results      = [
>>>>>>> 873941224ba16b7348479fd65f7c3d3e8b02a5d6
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
<<<<<<< HEAD
            return JsonResponse({'MESSAGE' : 'INVALID_PEOPLE_ID'}, status=400)

=======
            return JsonResponse({'ERROR' : 'INVALID_PEOPLE_ID'}, status=400)
>>>>>>> 873941224ba16b7348479fd65f7c3d3e8b02a5d6

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
<<<<<<< HEAD
            results = [
=======

            for content in content_list:
                content_list = dict(tuple(content.items()))

            results      = [
>>>>>>> 873941224ba16b7348479fd65f7c3d3e8b02a5d6
                {
                    'genre_id'   : genre.id,
                    'genre_name' : genre.name,
                    'contents'   : content_list,
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Genre.DoesNotExist:
<<<<<<< HEAD
            return JsonResponse({'MESSAGE' : 'INAVLID_GENRE_ID'}, status=400)

=======
            return JsonResponse({'ERROR' : 'INVALID_GENRE_ID'}, status=400)
>>>>>>> 873941224ba16b7348479fd65f7c3d3e8b02a5d6

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
<<<<<<< HEAD
            results = [
=======

            for content in content_list:
                content_list = dict(tuple(content.items()))

            results      = [
>>>>>>> 873941224ba16b7348479fd65f7c3d3e8b02a5d6
                {
                    'tag_id'   : tag.id,
                    'tag_name' : tag.name,
                    'contents' : content_list,
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Tag.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_TAG_ID'}, status=400)
<<<<<<< HEAD


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


class ContentCast(View):
    def get(self, request, content_id):
        try:
            content         = Content.objects.get(id=content_id)
            director        = content.contentpeople_set.get(role_name='감독').people
            main_actors     = content.contentpeople_set.filter(role_name='주연')
            main_actor_list = []

            for main_actor in main_actors:
                main_actor_list.append(
                    {
                        'id'            : main_actor.people_id,
                        'name'          : main_actor.people.name,
                        'profile_image' : main_actor.people.profile_image_url,
                    }
                )

            supporting_actors     = content.contentpeople_set.filter(role_name='조연')
            supporting_actor_list = []

            for supporting_actor in supporting_actors:
                supporting_actor_list.append(
                    {
                        'id'            : supporting_actor.people_id,
                        'name'          : supporting_actor.people.name,
                        'profile_image' : supporting_actor.people.profile_image_url,
                    }
                )

            results = [
                {
                    'director' :
                    {
                        'id'            : director.id,
                        'name'          : director.name,
                        'profile_image' : director.profile_image_url,
                    },
                    'main_actor'       : main_actor_list,
                    'supporting_actor' : supporting_actor_list,
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


class WatchaContent(View):
    def get(self, request):
        service = ContentService.objects.get(name='watcha')
        watcha_contents = ContentAvailableService.objects.filter(content_service_id=service.id)
        watcha_content_list = []
        results      = [
            {
                'service_id'   : service.id,
                'service_name' : service.name,
                'contents'     : watcha_content_list,
            }
        ]

        for watcha_content in watcha_contents:
            watcha_content_list.append(
                {
                    'id'             : watcha_content.content.id,
                    'title_korean'   : watcha_content.content.title_korean,
                    'title_original' : watcha_content.content.movieoverview_set.get().title_original,
                    'category'       : watcha_content.content.category.name,
                    'main_image_url' : watcha_content.content.main_image_url,
                }
            )
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)


class NetflixContent(View):
    def get(self, request):
        service             = ContentService.objects.get(name='netflix')
        watcha_contents     = ContentAvailableService.objects.filter(content_service_id=service.id)
        watcha_content_list = []
        results             = [
            {
                'service_id'   : service.id,
                'service_name' : service.name,
                'contents'     : watcha_content_list,
            }
        ]

        for watcha_content in watcha_contents:
            watcha_content_list.append(
                {
                    'id'             : watcha_content.content.id,
                    'title_korean'   : watcha_content.content.title_korean,
                    'title_original' : watcha_content.content.movieoverview_set.get().title_original,
                    'category'       : watcha_content.content.category.name,
                    'main_image_url' : watcha_content.content.main_image_url,
                }
            )
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)


class ContentGallery(View):
    def get(self, request, content_id):
        try:
            content            = Content.objects.get(id=content_id)
            gallery_photos     = ContentPhoto.objects.filter(content_id=content_id)
            gallery_photo_list = []

            for gallery_photo in gallery_photos:
                gallery_photo_list.append(
                    {
                    'photo_url' : gallery_photo.photo_url,
                    }
                )

            results = [
                {
                'content_id'           : content.id,
                'content_title_korean' : content.title_korean,
                'galleris'             : gallery_photo_list,
                }
            ]
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results}, status=200)
        except Content.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_CONTENT_ID'}, status=400)
=======
>>>>>>> 873941224ba16b7348479fd65f7c3d3e8b02a5d6

