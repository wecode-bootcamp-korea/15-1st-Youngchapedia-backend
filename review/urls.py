from django.urls import path

from review.views import ReviewView, ReviewLikeView

urlpatterns = [
    path('/content/<int:content_pk>', ReviewView.as_view()),
    path('/<int:review_pk>/like', ReviewLikeView.as_view()),
]
