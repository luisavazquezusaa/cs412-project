
# File: models.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 09/25/2025
# Description: this file is my models for mini insta, assigment 4

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User     # for authentication 

# Create your models here.
    

class Profile(models.Model): 
    '''Model for the user profile '''

    # Define the data atributes

    username = models.TextField(blank = True)
    display_name = models.TextField(blank = True)
    bio_text = models.TextField(blank = True)
    join_date = models.DateTimeField(auto_now = True)
    profile_image_url = models.URLField(blank = True) #url as a string
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Gave a value of 1 for profiles not associated with a user

    def __str__(self): 
        '''return a string representation of the model instance.'''
        return f'{self.username} joined {self.join_date}'
    
    def get_absolute_url(self): 
        '''return a URL to displya one instance of this object.'''
        return reverse('profile', kwargs={'pk': self.pk})
    
    def get_all_posts(self):
        '''Return a QuerySet of Posts about this Profile'''
        #Used the object manager to retrieve comments about this article
        
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_followers(self):
        '''Return a list of Profiles who follow this Profile.'''
        from .models import Follow
        follow_records = Follow.objects.filter(profile=self)
        followers = [follow.follower_profile for follow in follow_records]
        return followers

    def get_num_followers(self):
        '''return the count of followers.'''
        from .models import Follow
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        '''return a list of Profiles this Profile follows.'''
        from .models import Follow
        follow_records = Follow.objects.filter(follower_profile=self)
        following_profiles = [follow.profile for follow in follow_records]
        return following_profiles

    def get_num_following(self):
        '''return the count of Profiles this Profile follows.'''
        from .models import Follow
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        '''  return a list/QuerySet of Posts, specifically for the profiles being followed'''
        from .models import Follow, Post
        following = Follow.objects.filter(follower_profile=self)
        followed_profiles = [f.profile for f in following]
        feed_posts = Post.objects.filter(profile__in=followed_profiles).order_by('-timestamp')

        return feed_posts
    
    def is_followed_by(self, user):
        ''' if profile is followed by the a user'''
        follower_profile = Profile.objects.filter(user=user).first()
        if not follower_profile:
            return False
        return Follow.objects.filter(profile=self, follower_profile=follower_profile).exists()

    
class Post(models.Model): 
    '''Encapsulate the idea of a comment in an Article'''

    # data atributes for the Post:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True) #tells when comment was written 

    def __str__(self):
        '''Return a string representation of this comment'''
        return f'{self.caption}'
    
    def get_all_photos(self):
        """Return a QuerySet of Photos for this Post, ordered by timestamp"""
        photos = Photo.objects.filter(post=self).order_by('-timestamp')
        return photos

    def get_all_comments(self):
        '''Return all comments for a this Post.'''
        from .models import Comment
        comments = Comment.objects.filter(post=self).order_by('-timestamp')
        return comments
    
    def get_likes(self):
        '''get all likes for this Post.'''
        from .models import Like
        likes =  Like.objects.filter(post=self).order_by('-timestamp')
        return likes
    
    def get_num_likes(self):
        '''return the number of likes for this Post.'''
        from .models import Like
        return Like.objects.filter(post=self).count()
    
    def is_liked_by(self, user):
        '''if post is liked by a certain user'''
        liker_profile = Profile.objects.filter(user=user).first()
        if not liker_profile:
            return False
        return Like.objects.filter(post=self, profile=liker_profile).exists()
    

class Photo(models.Model): 
    '''Encapsulate the idea of a comment in an Article'''

    # data atributes for the Photo:
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True) #tells when comment was written 
    image_url = models.URLField(blank = True)
    image_file = models.ImageField(upload_to='photos/', blank=True, null=True) # an actual image. Note: Changed the code from the example bc during deployment the images weren't showing. 

    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        return self.image_url
    
    def __str__(self):
        img = self.get_image_url()
        return f"Photo[{img}]" if img else f"Photo id={self.pk}"

        
class Follow(models.Model):
    '''Represents one Profile following another Profile.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile"  )
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower_profile.username} follows {self.profile.username}"
    

class Comment(models.Model):
    '''Encapsulate the idea of a comment in a Post'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        '''Return a string representation of this comment'''
        return f'{self.profile.username} commented: {self.text}'
    
class Like(models.Model):
    ''' Encapsulates the idea of one Profile providing approval of a Post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self): 
        '''Return a string representation of this like'''
        return f'{self.profile.username}'





    


#from examples, Assingnment 4

        # class Comment(models.Model): 
        #     '''Encapsulate the idea of a comment in an Article'''

        #     # data atributes for the Comment:
        #     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
        #     username = models.TextField(blank=False)
        #     bio_text = models.TextField(blank=False)
        #     published = models.DateTimeField(auto_now=True) #tells when comment was written 

        #     def __str__(self):
        #         '''Return a string representation of this comment'''
        #         return f'{self.text}'



# Code from the example assigment 3: 

            # class Article(models.Model): 
        #     ''' '''

        #     # Define the data atributes

        #     title = models.TextField(blank = True)
        #     author = models.TextField(blank = True)
        #     text = models.TextField(blank = True)
        #     published = models.DateTimeField(auto_now = True) 
        #     image_ulr = models.URLField(blank = True)


        #     def __str__(self): 
        #         '''return a string representation of the model isntance.'''
        #         return f'{self.title} by {self.author}'



