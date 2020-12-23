from django.urls import path

from content.views import PeopleContent, GenreContent, TagContent, ContentDetail, ContentOverview
from content.views import ContentCast, WatchaContent, NetflixContent, ContentGallery, ContentSearch

urlpatterns = [
    path('/<int:content_id>', ContentDetail.as_view()),
    path('/people/<int:people_id>', PeopleContent.as_view()),
    path('/genre/<int:genre_id>', GenreContent.as_view()),
    path('/tag/<int:tag_id>', TagContent.as_view()),
    path('/watcha', WatchaContent.as_view()),
    path('/netflix', NetflixContent.as_view()),
    path('/gallery/<int:content_id>', ContentGallery.as_view()),
    path('/<int:content_id>/overview', ContentOverview.as_view()),
    path('/cast/<int:content_id>', ContentCast.as_view()),
    path('/search', ContentSearch.as_view()),
]
