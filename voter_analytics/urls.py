
# File: urls.py 
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 10/28/2025
# Description: Urls for the app voter_analytics 

from django.urls import path
from .views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', VoterListView.as_view(), name="voters"),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name="voter"),
    path('graphs/', VoterGraphsView.as_view(), name="graphs"),
    
]