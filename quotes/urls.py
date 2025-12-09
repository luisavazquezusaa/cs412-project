# file: quotes/urls.py
from django.urls import path
from django.conf import settings
from . import views

#URL patterns specific to the quotes app: 

urlpatterns = [
    path("", views.quote_page, name="quote_page"),          
    path("quote/", views.quote_page, name="quote_page"),
    path("show_all/", views.show_all, name="show_all"),
    path("about/", views.about, name="about_page"),
]


