from django.urls import path

from archive.views import RatingView

urlpatterns = [
    path('/rating/<int:content_pk>', RatingView.as_view()),
]
