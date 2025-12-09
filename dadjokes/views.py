# File: dadjokes/views.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/11/2025
# Description: Views for dadjokes app.

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from .serializers import *
import random
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


class RandomView(TemplateView):
    template_name = "dadjokes/random.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["joke"] = random.choice(Joke.objects.all())
        context["picture"] = random.choice(Picture.objects.all())
        return context


class JokeListView(ListView):
    model = Joke
    template_name = "dadjokes/show_all_jokes.html"
    context_object_name = "jokes"


class JokeDetailView(DetailView):
    model = Joke
    template_name = "dadjokes/show_joke.html"
    context_object_name = "joke"


class PictureListView(ListView):
    model = Picture
    template_name = "dadjokes/show_all_pictures.html"
    context_object_name = "pictures"


class PictureDetailView(DetailView):
    model = Picture
    template_name = "dadjokes/show_picture.html"
    context_object_name = "picture"


############################################################
#APIs

class RandomJokeAPIView(APIView):
    '''Return one random joke.'''
    def get(self, request, *args, **kwargs):
        jokes = Joke.objects.all()
        if not jokes:
            return Response({"error": "No jokes found."})
        joke = random.choice(jokes)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)


class JokeListCreateAPIView(generics.ListCreateAPIView):
    '''list all jokes and create a new joke'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    '''Return one joke by primary key.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
    

class PictureListAPIView(generics.ListAPIView):
    '''Return all pictures.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    '''Return one Picture by primary key.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(APIView):
    '''Return one random picture.'''
    def get(self, request, *args, **kwargs):
        pictures = Picture.objects.all()
        if not pictures:
            return Response({"error": "No pictures found."})
        picture = random.choice(pictures)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)