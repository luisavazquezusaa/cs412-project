# File: urls.py 
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 09/25/2025
# Description: Urls for the app mini_insta

from django.urls import path
# from .views import ShowAllView, RandomArticleView, ArticleView, --> from example
from .views import * 
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views 

urlpatterns = [

    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('show_all_profiles/', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view() , name='show_following'),
    path('profile/feed',  PostFeedListView.as_view(), name="show_feed"),
    path('profile/search', SearchView.as_view(), name='search'),

    # Authorization-related URLs (A7): 
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logged_out/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    path('register/', UserRegistrationView.as_view(), name='register'), 
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/follow/', FollowProfileView.as_view(), name='follow_profile'),
    path('profile/<int:pk>/delete_follow/', UnfollowProfileView.as_view(), name='unfollow_profile'),
    path('post/<int:pk>/like/', AddLikeView.as_view(), name='like_post'),
    path('post/<int:pk>/delete_like/', RemoveLikeView.as_view(), name='unlike_post'),

    #############################
    #API Views: 
    # path(r'api/articles/', ArticlesSerializers.as_view(), name='article_list_api'),


    #examples assigment 4: 
    # path('profile/create', CreateArticleView.as_view(), name="create_article"),
    # path('create_comment', CreateCommentView.as_view(), name="create_comment"),

    #from example: 
    # path('', RandomArticleView.as_view(), name="random"),
    # path('show_all/', ShowAllView.as_view(), name="show_all"),
    # path('article/<int:pk>', ArticleView.as_view(), name='article')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)