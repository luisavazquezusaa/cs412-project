# File: admin.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 12/2025
# Description: Registers all project models in the Django admin interface.

from django.contrib import admin
from .models import UserProfile, Listing, ListingPhoto, InterestRequest

# Registering the main models for the subletting marketplace
admin.site.register(UserProfile)
admin.site.register(Listing)
admin.site.register(ListingPhoto)
admin.site.register(InterestRequest)
