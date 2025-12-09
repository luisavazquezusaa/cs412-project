
# File: views.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 09/25/2025
# Description: this file is my views for mini insta 

from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
# from .models import Article --> from example
from .models import Profile, Post, Photo
import random
from django.contrib.auth.mixins import LoginRequiredMixin # for authentication
from django.contrib.auth.forms import UserCreationForm  # for new Users 
from django.contrib.auth.models import User  #Django user model 
from .forms import *      #CreateArticleForm, CreateCommentForm    from example Assignment 4
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login

class ProfileListView(ListView): 
    ''' Define a view class to display all users'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

    def dispatch(self, request,  *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ProfileListView.dispatch(): request.user={request.user}')
        else: 
            print(f'ProfileListView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            context["is_followed"] = profile.is_followed_by(user)
        else:
            context["is_followed"] = False

        return context


class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post 
    template_name = "mini_insta/show_post.html"
    context_object_name = "post" #Note singular variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            context["is_liked"] = post.is_liked_by(user)
        else:
            context["is_liked"] = False

        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Post on a Profile'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_login_url(self):
        '''Return the URL for the login page.'''
        return reverse('login')

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Post'''
        # After creating, go to the new Post detail page
        return reverse('post', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Handle form submission and save the new Post & Photo'''
        profile = Profile.objects.get(user=self.request.user)

        # attach this Profile to the Post
        form.instance.profile = profile

        # delegate the saving of Post to the superclass
        response = super().form_valid(form)

        # handle image files 
        image_files = self.request.FILES.getlist('image_files')
        for file in image_files:
            Photo.objects.create(post=self.object, image_file=file)

        return response
    
    ## from A7 examples dor def form_valid:
    # def form_valid(self, form):

    #     #find the login user
    #     user = self.request.user 
    #     print(f'CreatePostView.form_valid(): {user}')
    #     #attach that user to the form instance (to the POST object)
    #     form.instance.user = user
    #     #delegate work to the superclass to do the rest: 
    #     return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to update an Post and save it to the database. '''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_login_url(self):
        '''Return the URL for the login page.'''
        return reverse('login')

    def get_object(self, queryset=None):
        ''' Get the object to be updated. find the profile associated with the logged-in user'''
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''A view to update an existing Post'''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_login_url(self):
        '''Return the URL for the login page.'''
        return reverse('login')

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

class DeletePostView (DeleteView):
    '''A view class to delet a post in a Profile'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Provide context data for the delete confirmation template"""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["post"] = post
        context["profile"] = post.profile
        return context

    def get_success_url(self):
        """Return URL to redirect to after a successful delete"""
        post = self.get_object()
        profile = post.profile
        return reverse("profile", kwargs={"pk": profile.pk})
    
# Assignment 6 
    
class ShowFollowersDetailView(DetailView):
    """display followers for a Profile."""
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        context['followers'] = profile.get_followers()
        context['num_followers'] = profile.get_num_followers()
        return context


class ShowFollowingDetailView(DetailView):
    """display Profiles (subscribed) that this Profile follows."""
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        context['following_profiles'] = profile.get_following()
        context['num_following'] = profile.get_num_following()
        return context
        

class PostFeedListView(LoginRequiredMixin, ListView):
    '''display all of the Posts in the feed'''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Return the posts made by the profiles this user follows.'''
        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    

class SearchView(LoginRequiredMixin, ListView):
    '''search across Profiles and Posts.'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        query = self.request.GET.get('q', None)
        if not query:
            profile = Profile.objects.get(user=self.request.user)
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return Posts that match the query in their caption text.'''
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(caption__icontains=query)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        context['query'] = query

        if query:
            username_matches = Profile.objects.filter(username__icontains=query)
            display_matches = Profile.objects.filter(display_name__icontains=query)
            bio_matches = Profile.objects.filter(bio_text__icontains=query)
            context['profiles'] = (username_matches | display_matches | bio_matches).distinct()
        else:
            context['profiles'] = Profile.objects.none()

        return context
    
class UserRegistrationView(CreateView):
    '''show/process form for account registration form to create a new User'''

    template_name = 'mini_insta/register.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        '''url to redirect to after creating a new user'''
        return reverse('login')


class CreateProfileView(CreateView):
    '''handles new user registration'''

    form_class = CreateProfileForm
    model = Profile
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

class LogoutConfirmationView(TemplateView):
    '''display the logout confirmation page'''
    template_name = "mini_insta/logged_out.html"

class AddLikeView(LoginRequiredMixin, View):
    """add a like to a post."""
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        liker_profile = request.user.profile_set.first()
        Like.objects.get_or_create(post=post, profile=liker_profile)

        return redirect('post', pk=post.pk)

class RemoveLikeView(LoginRequiredMixin, View):
    """remove a like from a Post"""
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        liker_profile = request.user.profile_set.first()
        Like.objects.filter(post=post, profile=liker_profile).delete()

        return redirect('post', pk=post.pk)

class FollowProfileView(LoginRequiredMixin, View):
    """follow a Profile"""
    def post(self, request, pk):
        profile_to_follow = Profile.objects.get(pk=pk)
        follower_profile = request.user.profile_set.first()
        Follow.objects.get_or_create(profile=profile_to_follow, follower_profile=follower_profile)
        
        return redirect('profile', pk=profile_to_follow.pk)

class UnfollowProfileView(LoginRequiredMixin, View):
    """unfollow a Profile"""
    def post(self, request, pk):
        profile_to_unfollow = Profile.objects.get(pk=pk)
        follower_profile = request.user.profile_set.first()
        Follow.objects.filter(profile=profile_to_unfollow, follower_profile=follower_profile).delete()
        
        return redirect('profile', pk=profile_to_unfollow.pk)

#####################################################################

#Rest API:

# from rest_framework import generics
# from .serializers import * 

# class ArticleListAPIView(generics.ListCreateAPIView): 
#     '''
#     An API view to return a listing of Articles 
#     and to create an Article
#     '''

#     queryset = Article.objects.all()
#     serializer_class = ArticlesSerializers


  







#examples assigment 4: 

        # class CreateArticleView(CreateView):
        #     '''a view to handles creation of a new article
        #     (1) disaply the HTML form to the user (GET)
        #     (2) process the form submission and store the new Profile object (POST)
        #     '''

        #     form_class = CreateArticleForm 
        #     template_name = "mini_insta/create_article_form.html"

            # def form_valid(self, form): 
            #     '''Handle the form submission to create a new Article object.'''
            #     print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

        # class CreateCommentView(CreateView): 
        #     '''a view to handle creation of a new Comment on a Profile'''

        #     form_class = CreateCommentForm
        #     template_name = "mini_insta/create_comment_form.html"

        #     def get_success_url(self):
        #         '''Provide a URL to redirect to after creating a new Comments'''

        #         #Create and return a URL: 
        #         return reverse('show_all_profiles')  #not ideal

            #     #retrive PK from the URL pattern 
            #     pk = self.kwargs['pk']

            #     #call reverseto generate the URL for this Profile
            #     return reverse('profile', kwargs={'pk':pk})  
                  
            # def get_context_data(self):
            #     '''Return the dictionary of context variables for use in the template.'''
        
            #     # calling the superclass method
            #     context = super().get_context_data()
        
        
            #     # find/add the article to the context data
            #     # retrieve the PK from the URL pattern
            #     pk = self.kwargs['pk']
            #     article = Article.objects.get(pk=pk)
        
        
            #     # add this article into the context dictionary:
            #     context['article'] = article
            #     return context

            # def form_valid(self, form): 
            #     '''This method handles the form submission and saves the 
            #     new object to the Django database.
            #     We need to add the foreign key (of the Article) to the Comment
            #     object before saving it to the database.
            #     '''
            #     #retrive PK from the URL pattern 
            #     pk = self.kwargs['pk']
            #     profile = Profile.objects.get(pk-pk)
            #     #attach this Profile to the comment 
            #     form.instance.profile = profile #set the FK

            #     #deleagte the work to the superclass method form_valid: 
            #     return super().form_valid(form)



    # method

    # def get_object(self):
    #     '''return one instance of the article object selected at random'''

    #     all_articles = Article.objects.all()
    #     article = random.choice(all_articles)
    #     return article 



# Create your views here.
# class ShowAllView(ListView): 
#     ''' Define a view class to display all blog Articles'''
#     model = Article
#     template_name = "mini_insta/show_all.html"
#     context_object_name = "articles"

# class ArticleView(DetailView):

#     model = Article
#     template_name = "mini_insta/article.html"
#     context_object_name = "article" #Note singular variable name

# class RandomArticleView(DetailView):
#     '''Display' a single article'''

#     model = Article
#     template_name = "mini_insta/article.html"
#     context_object_name = "article"

#     # method

#     def get_object(self):
#         '''return one instance of the article object selected at random'''

#         all_articles = Article.objects.all()
#         article = random.choice(all_articles)
#         return article 




