import json

from django.http  import JsonResponse
from django.views import View

from content.models import *

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
            content_list = [dict(new_content) for new_content in {tuple(content.items()) for content in content_list}]
            results      = [
                {
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





# 작업 중단한 코드
#class MainContent(View):
#    def get(self, request):
#        contents = Content.objects.all()
#        results  = []
#
#        for content in contents:
#            genres    = ContentGenre.objects.filter(content_id = content.id)
#            tags      = ContentTag.objects.filter(content_id = content.id)
#            countries = ContentCountry.objects.filter(content_id = content.id)
#            results.append(
#                {
#                    'title_korean'   : content.title_korean,
#                    'title_original' : content.movieoverview_set.get().title_original,
#                    'id'             : content.id,
#                    'main_image_url' : content.main_image_url,
#                    'release_year'   : content.release_year,
#                    'runtime'        : content.movieoverview_set.get().runtime,
#                    'description'    : content.movieoverview_set.get().description,
#                    'genre'          : [genre.genre.name for genre in genres],
#                    'tag'            : [tag.tag.name for tag in tags],
#                }
#            )
#        return JsonResponse({'RESULT': results}, status=200)


