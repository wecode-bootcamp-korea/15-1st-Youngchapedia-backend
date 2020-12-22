from django.urls import path

from archive.views import RatingView, ArchiveView, UserArchiveView, UserRatingView, ContentRatingView

urlpatterns = [
    path('/content/<int:content_pk>', ArchiveView.as_view()),
    path('/rating/content/<int:content_pk>', RatingView.as_view()), 
    path('/user/<int:user_pk>', UserArchiveView.as_view()),
    path('/rating/user/<int:user_pk>', UserRatingView.as_view()),
    path('/rating/list/content/<int:content_pk>', ContentRatingView.as_view()),
]
