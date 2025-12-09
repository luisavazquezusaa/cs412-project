# File: admin.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 10/02/2025
# Description: this file is my admin for mini insta 

from django.contrib import admin

# Register your models here.
#from .models import Article from example, commented it out
#admin.site.register(Article)

from .models import Profile, Post, Photo, Follow, Comment, Like #registering the comment 
admin.site.register(Profile)
# admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)

