from django.urls import path

from review.views import ReviewView

urlpatterns = [
    path('/content/<int:content_pk>', ReviewView.as_view()),
]
