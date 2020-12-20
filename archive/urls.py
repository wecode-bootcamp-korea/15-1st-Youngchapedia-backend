from django.urls import path

from archive.views import RatingView, ArchiveView

urlpatterns = [
    path('/content/<int:content_pk>/rating', RatingView.as_view()),
    path('/content/<int:content_pk>', ArchiveView.as_view()),
]
