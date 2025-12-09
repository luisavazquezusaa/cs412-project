# dadjokes/serializers.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/11/2025
# Description: Serializers convert our django data models to a 
# text-representaiton suitable to transmit over HTTP

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''Serializer for the Joke model.'''
    class Meta:
        model = Joke
        fields = ['id', 'joke', 'author', 'published']


class PictureSerializer(serializers.ModelSerializer):
    '''Serializer for the Picture model.'''
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'author', 'published']