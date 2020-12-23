from django.urls import path

from archive.views import RatingView, ArchiveView, UserArchiveView, UserRatingView, ContentRatingView, UserMainView

urlpatterns = [
    path('/content/<int:content_pk>', ArchiveView.as_view()),
    path('/rating/content/<int:content_pk>', RatingView.as_view()), 
    path('/user', UserArchiveView.as_view()),
    path('/rating/user', UserRatingView.as_view()),
    path('/rating/list/content/<int:content_pk>', ContentRatingView.as_view()),
    path('/user/main', UserMainView.as_view()),
]
