# File: models.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/23/2025
# Description:
#   Database models for the TerrierBnB subletting marketplace.
#   Includes user profiles, listings, listing photos, and interest requests.
#
#   Notes:
#   - Each Django User has exactly one UserProfile.
#   - Listings store geocoded latitude/longitude for Google Maps.
#   - Interest Requests allow subletters to message hosts and express interest.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    """
    Extends the built-in Django User model with additional fields
    used for the subletting marketplace.

    Each profile includes:
    - display name
    - role (host or subletter)
    - contact info
    - short bio
    - profile photo
    """

    ROLE_CHOICES = [
        ('host', 'Host'),
        ('subletter', 'Subletter (Looking)'),
    ]

    # Link to Django's built-in User login system
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    display_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)


    def __str__(self):
        return self.display_name

    # Helper: all listings created by this user
    def get_listings(self):
        return Listing.objects.filter(lister=self)

    # Helper: all interest requests made by this user
    def get_interest_requests(self):
        return InterestRequest.objects.filter(requester=self)
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None


class Listing(models.Model):
    """
    Represents a sublet posted by a host.

    - Title, description, price
    - Address + geocoded latitude/longitude for Google Maps markers
    - Area (West Campus, Mid, Fenway, Allston…)
    - Availability dates
    - Optional photos (stored separately in ListingPhoto)
    """

    # Expanded area choices 
    AREA_CHOICES = [
        ('west', 'West Campus'),
        ('mid', 'Mid Campus'),
        ('east', 'East Campus'),
        ('south', 'South Campus'),
        ('fenway', 'Fenway'),
        ('kenmore', 'Kenmore'),
        ('backbay', 'Back Bay'),
        ('brookline', 'Brookline'),
        ('cambridge', 'Cambridge'),
        ('allston', 'Allston'),
        ('brighton', 'Brighton'),
        ('somerville', 'Somerville'),
        ('medford', 'Medford'),
        ('seaport', 'Seaport'),
        ('downtown', 'Downtown Boston'),
    ]

    # Grouped choices for cleaner dropdown sections
    AREA_GROUPED_CHOICES = [
        ("BU Campus", [
            ('west', 'West Campus'),
            ('mid', 'Mid Campus'),
            ('east', 'East Campus'),
            ('south', 'South Campus'),
            ('kenmore', 'Kenmore'),
        ]),
        ("Nearby Neighborhoods", [
            ('allston', 'Allston'),
            ('brighton', 'Brighton'),
            ('fenway', 'Fenway'),
            ('brookline', 'Brookline'),
            ('cambridge', 'Cambridge'),
        ]),
        ("Greater Boston", [
            ('backbay', 'Back Bay'),
            ('downtown', 'Downtown Boston'),
            ('seaport', 'Seaport'),
            ('somerville', 'Somerville'),
            ('medford', 'Medford'),
        ])
    ]

    # Who owns this listing? (foreign key to UserProfile)
    lister = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # Basic fields
    title = models.CharField(max_length=120)
    description = models.TextField()
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)

    # Address used to geocode location for Google Maps
    address = models.CharField(max_length=255)

    # When the sublet starts/ends
    start_date = models.DateField()
    end_date = models.DateField()

    # Area identifier (used for filtering)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)

    # Number of roommates at the sublet location
    number_of_roommates = models.IntegerField(default=0)

    # Google Maps marker coordinates (geocoded automatically)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Automatically set to False when the listing is accepted by someone
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # Helper: all photos attached to this listing
    def get_photos(self):
        return ListingPhoto.objects.filter(listing=self)

    # Helper: all interest requests for this listing
    def get_interest_requests(self):
        return InterestRequest.objects.filter(listing=self)
    
    def get_absolute_url(self):
        return reverse("listing", args=[self.pk])



class ListingPhoto(models.Model):
    """
    Stores photos for a listing.

    Supports:
    - Uploaded images (image_file)
    - External URLs (e.g., links to images)
    """

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    # Upload to: media/listing_photos/
    image_file = models.ImageField(upload_to="listing_photos/", blank=True, null=True)

    # Optional external URL instead of uploading
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"Photo for {self.listing.title}"


class InterestRequest(models.Model):
    """
    Allows a subletter to send a message to a host expressing interest.

    Fields:
    - listing: the listing being requested
    - requester: user sending the request
    - message: message content
    - timestamp: automatically added
    - status: pending, accepted, declined
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )

    def __str__(self):
        return f"{self.requester} {self.listing} ({self.status})"



