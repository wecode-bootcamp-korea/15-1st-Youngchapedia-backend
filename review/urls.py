from django.urls import path

from review.views import ReviewView, ContentReviewView

urlpatterns = [
    path('/content/<int:content_pk>', ReviewView.as_view()),
    path('/list/content/<int:content_pk>', ContentReviewView.as_view()),
]
