## blog/seria;izers.py
## Serializers convert our django data models to a 
## text-representaiton suitable to transmit over HTTP

# from rest_framework import serializers
# from .models import *

# class ArticlesSerializers(serializers.ModelSerializer):
#     '''A serializer for the Artivel model
#     Specify which model/fields to send in the API.'''

#     class Meta:
#         model: Article
#         fields = ['id', 'title', 'author', 'text', 'image_file'] ##image file returns a url 
    
#     def create(self):
#         '''
#         Override the superclass method that handles object creationm 
#         '''
#         print(f'ArtcileSerializer.create, validated_data={validated_data}.')

        # ##create an Artcile object
        # article = Article(**validated_data)
        # ##attach a FK for the User
        # article.user = User.objects.first()
        # ##save  the iobject to the database
        # article.save()
        # ##return an ibject isntance
        # return article
    
        ##a simplified way:
        ##attached a FK for the User
        # validated_data['user'] = User.objects.first()
        # ##do the create and save all at once
        # return Article.objects.create(**validated_data)

    ## add methods to customizer the Create/Read/Update/Delet operations
    ## need to create a serializer for each model 

###################################
