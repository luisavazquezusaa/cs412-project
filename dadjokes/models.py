# File: dadjokes/models.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/11/2025
# Description: Models for dadjokes app.

from django.db import models
from django.urls import reverse

class Joke(models.Model):
    joke = models.TextField()
    author = models.CharField(max_length=100)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.joke[:50]}, added by {self.author}: "

    def get_absolute_url(self):
        return reverse('joke', kwargs={'pk': self.pk})


class Picture(models.Model):
    image_url = models.URLField()
    author = models.CharField(max_length=100)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture by {self.author}"

    def get_absolute_url(self):
        return reverse('picture_detail', kwargs={'pk': self.pk})

