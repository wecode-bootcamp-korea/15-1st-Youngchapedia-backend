from django.urls import path

from review.views import ReviewView, UserReviewView

urlpatterns = [
    path('/<int:content_pk>', ReviewView.as_view()),
    path('/<int:content_pk>/<int:user_pk>', UserReviewView.as_view()),
]
