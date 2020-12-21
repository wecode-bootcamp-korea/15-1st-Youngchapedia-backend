from django.urls import path

from content.views import PeopleContent, GenreContent, TagContent, WatchaContent, NetflixContent, ContentGallery, ContentOverview, ContentCast, ContentDetail

urlpatterns = [
    path('/<int:content_id>', ContentDetail.as_view()),
    path('/people/<int:people_id>', PeopleContent.as_view()),
    path('/genre/<int:genre_id>', GenreContent.as_view()),
    path('/tag/<int:tag_id>', TagContent.as_view()),
]
