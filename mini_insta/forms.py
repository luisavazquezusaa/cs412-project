# File: forms.py 
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 09/02/2025
# Description: forms file for the app mini_insta

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm): 
        '''A form to add a comment about an article'''

        class Meta: 
                '''associate this form with a model from our database'''
                model = Post
                fields = ['caption'] #we dont want the drop down list

class UpdateProfileForm(forms.ModelForm):
        '''A form to handle or update a profile'''
        class Meta:
                '''associate this form with the Post model.'''
                model = Profile
                fields = ['display_name', 'bio_text', 'profile_image_url']  # which fields from model should we use

class UpdatePostForm(forms.ModelForm):
    '''A form to update the caption of an existing Post.'''

    class Meta:
        model = Post
        fields = ['caption']

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile'''

    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']



#Examples Assignment 4:

        # class CreateArticleForm(forms.ModelForm): 
        #     """ a Form to add an article to the """

        #     class Meta:
        #         """associate this from with a model from out data base"""
        #         model = Profile
        #         fields = ['username', 'display_name', 'bio_text', 'profile_image_url']

        # class CreateCommentForm(forms.ModelForm): 
        #     '''A form to add a comment about an article'''

        #     class Meta: 
        #         '''associate this form with a model from our database'''
        #         model = Comment
        #         fields = ['profile', 'username', 'bio_text'] #deleated
        #         fields = ['username', 'bio_text'] #we dont want the drop down list