from django.urls import path

from review.views import ReviewView

urlpatterns = [
    path('', ReviewView.as_view())
]
