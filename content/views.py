import json

from django.http  import JsonResponse
from django.views import View

from content.models import *

# Create your views here.

class ContentDetail(View):
    def get(self, request, content_id):
        try:
            content   = Content.objects.get(id=content_id)
            genres    = content.contentgenre_set.all()
            countries = content.contentcountry_set.all()

            result = [
                {
                    'content_id'     : content.id,
                    'title_korean'   : content.title_korean,
                    'main_image_url' : content.main_image_url,
                    'release_year'   : content.release_year,
                    'genre'          : [genre.genre.name for genre in genres],
                    'country'        : [country.country.name for country in countries],
                }
            ]
            return JsonResponse({'RESULT' : result}, status=200)
        except KeyError:
            return JsonResponse({'ERROR' : 'ERROR'}, status=400)


class ContentCast(View):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)
            director = content.contentpeople_set.get(role_name='감독').people
            main_actors = content.contentpeople_set.filter(role_name='주연')
            main_actor_list = []
            for main_actor in main_actors:
                main_actor_list.append(
                    {
                        'id' : main_actor.people_id,
                        'name' : main_actor.people.name,
                        'profile_image' : main_actor.people.profile_image_url,
                    }
                )

            supporting_actors = content.contentpeople_set.filter(role_name='조연')
            supporting_actor_list = []
            for supporting_actor in supporting_actors:
                supporting_actor_list.append(
                    {
                        'id' : supporting_actor.people_id,
                        'name' : supporting_actor.people.name,
                        'profile_image' : supporting_actor.people.profile_image_url,
                    }
                )

            result = [
                {
                    'director' :
                    {
                        'id' : director.id,
                        'name' : director.name,
                        'profile_image' : director.profile_image_url,
                    },
                    'main_actor' : main_actor_list,
                    'supporting_actor' : supporting_actor_list,
#                    'main_actor' : [main_actor.people.name for main_actor in main_actors],
#                    'support_actor' : [supporting_actor.people.name for supporting_actor in supporting_actors],
                }
            ]

            return JsonResponse({'RESULT' : result}, status=200)

        except KeyError:
            return JsonResponse({'ERROR' : 'ERROR'}, status=400)


class ContentOverview(View):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)
            content_overview = content.movieoverview_set.get()
            genres    = content.contentgenre_set.all()

            result = [
                {
                    'content_id'     : content.id,
                    'title_original' : content_overview.title_original,
                    'release_year'   : content.release_year,
                    'genre'          : [genre.genre.name for genre in genres],
                    'runtime' : content_overview.runtime,
                    'description' : content_overview.description,
                }
            ]
            return JsonResponse({'MESSAGE' : result}, status=200)
        except KeyError:
            return JsonResponse({'ERROR' : 'ERROR'}, status=400)


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
            content_list = [dict(new_content) for new_content in {tuple(content.items()) for content in content_list}]
            results      = [
                {
                    'id'                : people.id,
                    'name'              : people.name,
                    'title'             : job_list,
                    'profile_image_url' : people.profile_image_url,
                    'contents'          : content_list,
                }
            ]

            return JsonResponse({'RESULT' : results}, status=200)

        except People.DoesNotExist:
            return JsonResponse({'ERROR' : 'PEOPLE_ERROR'}, status=400)

        except Exception as e:
            return JsonResponse({'ERROR' : e}, status=400)


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
            content_list = [dict(new_content) for new_content in {tuple(content.items()) for content in content_list}]
            results      = [
                {
                    'genre_id'   : genre.id,
                    'genre_name' : genre.name,
                    'contents'   : content_list,
                }
            ]
            return JsonResponse({'MESSAGE' : results}, status=200)

        except Genre.DoesNotExist:
            return JsonResponse({'ERROR' : 'GENRE_ERROR'}, status=400)

        except Exception as e:
            return JsonResponse({'ERROR' : e}, stauts=400)


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
            content_list = [dict(new_content) for new_content in {tuple(content.items()) for content in content_list}]
            results      = [
                {
                    'tag_id'   : tag.id,
                    'tag_name' : tag.name,
                    'contents' : content_list,
                }
            ]
            return JsonResponse({'RESULT' : results}, status=200)

        except Tag.DoesNotExist:
            return JsonResponse({'ERROR' : 'TAG_ERROR'}, status=400)

        except Exception as e:
            return JsonResponse({'ERROR' : e}, status=400)


class WatchaContent(View):
    def get(self, request):
        try:
            service = ContentService.objects.get(name='watcha')
            watcha_contents = ContentAvailableService.objects.filter(content_service_id=service.id)
            watcha_content_list = []
            results      = [
                {
                    'service_id'   : service.id,
                    'service_name' : service.name,
                    'contents' : watcha_content_list,
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
            return JsonResponse({'RESULT' : results}, status=200)
        except KeyError:
            return JsonResponse({'ERROR' : 'TAG_ERROR'}, status=400)


class NetflixContent(View):
    def get(self, request):
        try:
            service = ContentService.objects.get(name='netflix')
            watcha_contents = ContentAvailableService.objects.filter(content_service_id=service.id)
            watcha_content_list = []
            results      = [
                {
                    'service_id'   : service.id,
                    'service_name' : service.name,
                    'contents' : watcha_content_list,
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
            return JsonResponse({'RESULT' : results}, status=200)
        except KeyError:
            return JsonResponse({'ERROR' : 'TAG_ERROR'}, status=400)


class ContentGallery(View):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)
            gallery_photos = ContentPhoto.objects.filter(content_id=content_id)
            gallery_photo_list = []

            for gallery_photo in gallery_photos:
                gallery_photo_list.append(
                    {
                    'photo_url' : gallery_photo.photo_url,
                    }
                )

            results = [
                {
                'content_id' : content.id,
                'content_title_korean' : content.title_korean,
                'galleris' : gallery_photo_list,
                }
            ]

            return JsonResponse({'RESULT' : results}, status=200)

        except Content.DoesNotExist:
            return JsonResponse({'ERROR' : 'ERROR'}, status=400)

