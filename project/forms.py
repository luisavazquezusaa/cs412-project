# File: forms.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/23/2025
# Description: Forms for user registration, profiles, listings, and interest requests
# in the subletting marketplace web application.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class RegisterUserForm(UserCreationForm):
    """
    Includes the email field, because all users in the project are expected to provide a contact email.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    """
    Collects or updates the user's profile information, such as display name,
    role (host or subletter), phone, bio, and profile photo. This form is used
    immediately after registration and in profile updates.
    """

    class Meta:
        model = UserProfile
        fields = [
            "display_name",
            "role",
            "email",
            "phone",
            "bio",
            "image",
        ]

        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class ListingForm(forms.ModelForm):
    """
    Listing creation / update form.
    Latitude & longitude stay hidden and are filled by Google Maps autocomplete.
    """
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price_per_month",
            "address",
            "area",
            "start_date",
            "end_date",
            "number_of_roommates",
            "latitude",
            "longitude",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "latitude": forms.HiddenInput(),   
            "longitude": forms.HiddenInput(),  
        }


class InterestRequestForm(forms.ModelForm):
    """
    Allows a user to send an interest request to a listing owner. Only the
    message field is shown to the user; the listing and sender are assigned
    in the view.
    """

    class Meta:
        model = InterestRequest
        fields = ["message"]

        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }

class InterestRequestStatusForm(forms.ModelForm):
    """
    Simple form allowing hosts to update the status of an interest request.
    """
    class Meta:
        model = InterestRequest
        fields = ["status"]

