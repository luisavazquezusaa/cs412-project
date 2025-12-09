# File: context_processors.py
# Author: Luisa Vazquez Usabiaga
# Last updated: 12/09/2025
# Description:
#   Exposes the Google Maps API key to all Django templates. 
#   This allows templates to access {{ GOOGLE_MAPS_API_KEY }} without needing 
#   to manually pass it from every view.

from django.conf import settings

def google_api_key(request):
    """
    Returns the Google Maps API key so that it is available as a global
    template variable across the entire project.
    """
    return {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
    }

