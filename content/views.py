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

class ContentSearch(View):
    def get(self, request):
        search_keyword    = request.GET.get('keyword', None)
        contents          = Content.objects.all()
        searches_korean   = contents.filter(title_korean__contains=search_keyword)
        searches_original = MovieOverview.objects.filter(title_original__contains=search_keyword)
        movie_list        = []

        if searches_korean.count() > 0:
            [movie_list.append(movie_korean) for movie_korean in searches_korean]
        if searches_original.count() > 0:
            [movie_list.append(movie_original) for movie_original in searches_original]

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)
"""
            result = [
                {
                    'movies' : [
                        {
                            'moive_title_korean' : movie.content.title_korean,
                            'movie'
                        } for movie in movie_list
                    ]
                }
            ]
"""


#            [
#                {'movie_title_korean' : movie.content.title_korean,
#                 'movie_title_original' : movie.title_original,
#            for movie in movie_list]
#        }

#        movie_original_list = [movie_original for movie_original in MovieOverview.objects.filter(title_original__contains=search_keyword)]

"""
#        search_movie_list =
#        search_movie_list.append(
#
#        )
#        movies          = []
#        searched_movies = contents.filter(title_korean__contains=search_keyword) + MovieOverview.objects.filter(title_original__contains=search_keyword)
#        searched_users  = User.objects.filter(username__contains=search_keyword)
        print()
        print()
        print('========search_keyword=============')
        print(search_keyword)
        print('========search_kyword==============')
        print()
        print()
        print('========searched_movies============')
        results = [{
            'movie_id' : movie.id,
            'movie_title_korean' : movie.title_korean,
            'movie_release_year' : movie.release_year,
            'movie_main_image_url' : movie.main_image_url,
            'movie_content_country' : [movie_content_country.country.name for movie_content_country in movie.contentcountry_set.all()]
        } for movie in searched_movies]
        print('========searched_movies============')
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : results})
        movie_overview_list = []

        for movie_overview in movie_overviews:
            movie_overview_list.append(
                {
                    'id' : movie_overview.id,
                    'title_korean' : movie_overview.title_korean,
                    'main_image_url' : movie_overview.main_image_url,
                    'release_year' : movie_overview.release_year,
                    'country' : [movie_overview.country.name for movie_overview in movie_overview.contentcountry_set.all()],
                }
            )
"""

