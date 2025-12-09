from django.shortcuts import render
from django.shortcuts import render

def images_view(request):
    return render(request, 'images/images.html')
