from django.urls import path

from content.views import *

urlpatterns = [
#    path('', MainContent.as_view()),
    path('/people/<int:people_id>', PeopleContent.as_view()),
]
