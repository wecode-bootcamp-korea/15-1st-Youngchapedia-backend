path('/<int:content_id>', ContentDetail.as_view()),
path('/cast/<int:content_id>', ContentCast.as_view()),
path('/<int:content_id>/overview', ContentOverview.as_view()),
path('/gallery/<int:content_id>', ContentGallery.as_view()),
path('/netflix', NetflixContent.as_view()),
path('/watcha', WatchaContent.as_view()),


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
