from django.urls import path

from archive.views import RatingView

urlpatterns = [
    path('/rating', RatingView.as_view()),
]
