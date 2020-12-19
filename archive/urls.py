from django.urls import path

from archive.views import RatingView

urlpatterns = [
    path('/content/<int:content_pk>/rating', RatingView.as_view()),
]
