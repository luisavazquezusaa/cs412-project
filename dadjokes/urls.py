# File: urls.py 
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/11/2025
# Description: Urls for the app dadjokes

from django.urls import path
from .views import * 
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views 

urlpatterns = [

    path('', RandomView.as_view(), name='random'),
    path('random/', RandomView.as_view(), name='random'),
    path('jokes/', JokeListView.as_view(), name='show_all_jokes'),
    path('joke/<int:pk>/', JokeDetailView.as_view(), name='show_joke'),
    path('pictures/', PictureListView.as_view(), name='show_all_pictures'),
    path('picture/<int:pk>/', PictureDetailView.as_view(), name='show_picture'),

    #API
    path('api/', RandomJokeAPIView.as_view(), name='api_home'),
    path('api/random/', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/jokes/', JokeListCreateAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>/', JokeDetailAPIView.as_view(), name='api_joke'),
    path('api/pictures/', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>/', PictureDetailAPIView.as_view(), name='api_picture'),
    path('api/random_picture/', RandomPictureAPIView.as_view(), name='api_random_picture'),

]