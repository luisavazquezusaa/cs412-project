# File: views.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/23/2025
# Description: Views for the subletting marketplace. Handles user registration,
# profile creation, listings, interest requests, and main application workflows.

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from .forms import *



class RegisterUserView(CreateView):
    """
    Creates a new Django user account. After registration the user is logged in
    automatically and redirected to create their profile, since every user needs
    profile details before interacting with the app.
    """
    form_class = RegisterUserForm
    template_name = "project/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        # If this user already has a profile, skip create_profile
        if UserProfile.objects.filter(user=user).exists():
            return redirect("update_profile")

        # Otherwise, send to create profile
        return redirect("create_profile")


class CreateUserProfileView(LoginRequiredMixin, CreateView):
    """
    After a user account is created, this view collects profile information such
    as display name, role, phone number, image, and bio.
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = "project/create_profile.html"
    success_url = reverse_lazy("show_all_listings")

    def dispatch(self, request, *args, **kwargs):
        # If profile exists redirect to update_profile instead
        if UserProfile.objects.filter(user=request.user).exists():
            return redirect("update_profile")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return super().form_valid(form)



class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    """
    Allows a logged-in user to update their profile information at any time.
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = "project/update_profile_form.html"
    success_url = reverse_lazy("show_all_listings")

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class UserProfileListView(ListView):
    """
    Shows all user profiles, with optional filtering by role (host/subletter).
    """
    model = UserProfile
    template_name = "project/show_all_profiles.html"
    context_object_name = "profiles"
    

    def get_queryset(self):
        """
        Returns the appropriate list of profiles depending on the 'role' passed
        in the querystring.
        """ 
        queryset = UserProfile.objects.all()
        role = self.request.GET.get("role")

        if role == "host":
            queryset = queryset.filter(role="host")
        elif role == "subletter":
            queryset = queryset.filter(role="subletter")

        return queryset



class UserProfileDetailView(DetailView):
    """
    Shows a user's profile and (if applicable) their listings or interest requests.
    """
    model = UserProfile
    template_name = "project/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_object()   # Profile being viewed

        # Listings created by this profile (if they are a host)
        context["listings"] = Listing.objects.filter(lister=profile)

        # If the logged-in user is viewing their own profile,
        # and they are a subletter, show their submitted interest requests
        if self.request.user.is_authenticated and self.request.user == profile.user:
            context["submitted_interest_requests"] = InterestRequest.objects.filter(
                requester=profile
            )
        else:
            context["submitted_interest_requests"] = []

        return context



class ListingListView(ListView):
    """
    Shows every listing in the marketplace. The map template reads latitude and
    longitude from each listing and places pins accordingly.
    """
    model = Listing
    template_name = "project/show_all_listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        qs = Listing.objects.all()

        # Filters 
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        area = self.request.GET.get("area")

        # Apply filters 
        if min_price:
            qs = qs.filter(price_per_month__gte=min_price)

        if max_price:
            qs = qs.filter(price_per_month__lte=max_price)

        if start_date:
            qs = qs.filter(start_date__lte=start_date)

        if end_date:
            qs = qs.filter(end_date__gte=end_date)

        if area:
            qs = qs.filter(area=area)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["min_price"] = self.request.GET.get("min_price", "")
        context["max_price"] = self.request.GET.get("max_price", "")
        context["start_date"] = self.request.GET.get("start_date", "")
        context["end_date"] = self.request.GET.get("end_date", "")
        context["area_selected"] = self.request.GET.get("area", "")

        # Send grouped area choices
        context["area_choices_grouped"] = Listing.AREA_GROUPED_CHOICES

        return context



class ListingDetailView(DetailView):
    """
    Displays a specific listing with full details and shows interest request
    controls depending on whether the viewer is a host or a subletter.
    """
    model = Listing
    template_name = "project/show_listing.html"
    context_object_name = "listing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add interest request form for subletters
        context["interest_form"] = InterestRequestForm()

        return context



class CreateListingView(LoginRequiredMixin, CreateView):
    """
    Allows a host to create a new listing. The current user is automatically
    assigned as the owner of the listing. Coordinates may be generated from
    address if geocoding is added later.
    """
    model = Listing
    form_class = ListingForm
    template_name = "project/create_listing.html"

    def form_valid(self, form):
        listing = form.save(commit=False)

        # Assign the lister = current user's profile
        listing.lister = self.request.user.userprofile  

        # Save with the assigned lister
        listing.save()

        # Save uploaded photos
        for file in self.request.FILES.getlist("image_files"):
            ListingPhoto.objects.create(listing=listing, image_file=file)

        return super().form_valid(form)


class UpdateListingView(LoginRequiredMixin, UpdateView):
    """
    Allows the host who owns the listing to update its information.
    """
    model = Listing
    form_class = ListingForm
    template_name = "project/update_listing.html"
    success_url = reverse_lazy("show_all_listings")

    def get_queryset(self):
        return Listing.objects.filter(lister=self.request.user.userprofile)



class DeleteListingView(LoginRequiredMixin, DeleteView):
    """
    Allows the listing’s owner to delete their listing.
    """
    model = Listing
    template_name = "project/delete_listing.html"
    success_url = reverse_lazy("show_all_listings")

    def get_queryset(self):
        # Only allow deleting listings that belong to the logged-in user
        return Listing.objects.filter(lister=self.request.user.userprofile)



class CreateInterestRequestView(LoginRequiredMixin, CreateView):
    """
    Allows a subletter to send an interest request to the host of a listing.
    """
    model = InterestRequest
    form_class = InterestRequestForm
    template_name = "project/create_interest_request.html"

    def form_valid(self, form):
        request_obj = form.save(commit=False)
        request_obj.listing = Listing.objects.get(pk=self.kwargs["pk"])
        request_obj.requester = self.request.user.userprofile
        request_obj.save()
        return redirect("my_interest_requests")


class MyInterestRequestsView(LoginRequiredMixin, ListView):
    """
    Shows all interest requests that the current user has sent to hosts.
    """
    model = InterestRequest
    template_name = "project/my_interest_requests.html"
    context_object_name = "requests"

    def get_queryset(self):
        return InterestRequest.objects.filter(requester=self.request.user.userprofile)



class ManageInterestRequestsView(LoginRequiredMixin, ListView):
    """
    Host view to manage interest requests submitted to their listings.
    """
    model = InterestRequest
    template_name = "project/manage_interest_requests.html"
    context_object_name = "interest_requests"

    def get_queryset(self):
        # Only requests for listings owned by the logged-in host
        return InterestRequest.objects.filter(
            listing__lister=self.request.user.userprofile
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        listing_id = self.kwargs.get("pk")
        context["listing"] = Listing.objects.get(pk=listing_id)

        # form used in template
        context["status_form"] = InterestRequestStatusForm()

        return context


class YourListingsView(LoginRequiredMixin, ListView):
    """
    Displays all listings created by the currently logged-in host.
    """
    model = Listing
    template_name = "project/your_listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)
    

class HostListView(ListView):
    model = UserProfile
    template_name = "project/show_all_profiles.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return UserProfile.objects.filter(role="host")

class SubletterListView(ListView):
    model = UserProfile
    template_name = "project/show_all_profiles.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return UserProfile.objects.filter(role="subletter")



def update_interest_request_status(request, pk):
    """
    Updates host decision on an interest request.
    - If ACCEPTED → delete listing + all its interest requests
    - If DECLINED → delete only this request
    """
    req = get_object_or_404(InterestRequest, pk=pk)
    listing = req.listing

    if request.method == "POST":
        status = request.POST.get("status")

        if status == "accepted":
            # Delete all requests for this listing
            InterestRequest.objects.filter(listing=listing).delete()
            # Delete the listing
            listing.delete()
            return redirect("show_all_listings")

        elif status == "declined":
            # delete only this request
            req.delete()
            return redirect("manage_interest_requests", pk=listing.pk)

    # fallback
    return redirect("manage_interest_requests", pk=listing.pk)