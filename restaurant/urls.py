# File: urls.py 
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 09/19/2025
# Description: Urls for the app restaurant

from django.urls import path
from django.conf import settings
from . import views

#URL patterns specific to the restaurant app: 

urlpatterns = [
    path(r"", views.main, name="main"), 
    path(r"order/", views.order_page, name="order_page"),    
    path(r"submit/", views.submit, name="submit"),     
]
