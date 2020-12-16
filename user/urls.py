from django.urls import path
from user.views import SignUpView, SignInView

urlpatterns = [
    path('signup', views.SignUpView.as_view()),
    path('signin', views.SignInView.as_view()),
]
