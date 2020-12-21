from django.urls import path

from content.views import PeopleContent, GenreContent, TagContent, WatchaContent, NetflixContent, ContentGallery, ContentOverview, ContentCast, ContentDetail

urlpatterns = [
    path('/<int:content_id>', ContentDetail.as_view()),
]
