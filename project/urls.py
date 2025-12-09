# File: project/urls.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 11/23/2025
# Description: URL routes for the subletting marketplace app.

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # Home (listings page)
    path('', ListingListView.as_view(), name="show_all_listings"),

    # Profiles
    path('profiles/', UserProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile'),
    path('profile/update/', UpdateUserProfileView.as_view(), name='update_profile'),

    # User registration + profile creation
    path('register/', RegisterUserView.as_view(), name='register'),
    path('create_profile/', CreateUserProfileView.as_view(), name='create_profile'),

    # Listings
    path('listings/', ListingListView.as_view(), name='show_all_listings'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing'),
    path('listing/create/', CreateListingView.as_view(), name='create_listing'),
    path('listing/<int:pk>/update/', UpdateListingView.as_view(), name='update_listing'),
    path('listing/<int:pk>/delete/', DeleteListingView.as_view(), name='delete_listing'),

    # Interest requests
    path('listing/<int:pk>/interest/create/', CreateInterestRequestView.as_view(), name='create_interest_request'),
    path('listing/<int:pk>/manage_requests/', ManageInterestRequestsView.as_view(), name='manage_interest_requests'),
    path("interest_request/<int:pk>/update_status/", update_interest_request_status, name="update_interest_request_status"),


    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_listings'), name='logout'),

    # Dashboard views
    path('your_listings/', YourListingsView.as_view(), name='your_listings'),
    path('my_interest_requests/', MyInterestRequestsView.as_view(), name='my_interest_requests'),

    #tabs for hosts and subletter
    path('hosts/', HostListView.as_view(), name="show_hosts"),
    path('subletters/', SubletterListView.as_view(), name="show_subletters"),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

