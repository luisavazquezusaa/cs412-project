# File: utils.py
# Author: Luisa Vazquez Usabiaga. 12/08/2025
# Description: Utility functions for geocoding addresses using Google Maps.

import requests
from django.conf import settings

def geocode_address(address):
    """
    Takes a human-readable street address and returns (latitude, longitude).
    Returns (None, None) if the API fails or no result is found.
    """

    if not address:
        return None, None

    api_key = settings.GOOGLE_MAPS_API_KEY
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None, None

    data = response.json()

    if data["status"] != "OK":
        return None, None

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
