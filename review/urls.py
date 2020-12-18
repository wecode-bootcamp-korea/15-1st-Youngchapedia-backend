from django.urls import path

from review.views import ReviewView, UserReviewView

urlpatterns = [
    path('content/<int:content_pk>', ReviewView.as_view()),
    path('/<int:review_pk>', UserReviewView.as_view()),
]
