from django.urls import path

from content.views import *

urlpatterns = [
#    path('', MainContent.as_view()),
    path('/people/<int:people_id>', PeopleContent.as_view()),
    path('/genre/<int:genre_id>', GenreContent.as_view()),
    path('/tag/<int:tag_id>', TagContent.as_view()),
]
