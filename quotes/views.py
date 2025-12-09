#file: quotes/views.py 

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random

# Create your views here.

# List quotes and images

quotes = [
    "Because I'm pregnant! And this girl's about to beat my ass! Hello?",
    "They're wigs! - When asked by the opposing counsel if her changing hairstyles were real",
    "She is security-heavy", 
    "I was calling her a bitch",

]

images = [
    
    "https://img.pastemagazine.com/wp-content/juploads/2025/08/cardi-lg.jpg",
    "https://i.dailymail.co.uk/1s/2025/09/03/20/101811373-15063149-Cardi_B_has_announced_a_new_courtroom_edition_of_her_latest_albu-a-3_1756928639061.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/f/f1/Cardi_B_Photo_by_Chris_Allmeid_%28cropped%29.jpg", 

]

def home(request):
    '''Define a view to handle the 'home' request.'''
    response_text = '''
    <html>
    <h1>Cardi B Quote Of The Day</h1>
    </html>'''
    
    return HttpResponse(response_text)

def quote_page(request): 
    '''Respond to URL', delegate work to a template'''
    template_name = 'quotes/quote.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        "letter1": chr(random.randint(65,90),),
        "number": chr(random.randint(0x1F600, 0x1F64F)), 
        "quote": random.choice(quotes),
        "image": random.choice(images), 
        
    }

    return render(request, template_name, context) 

def about(request): 
    '''Respond to URL 'about', delegate work to a template'''
    template_name = 'quotes/about.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        "letter1": chr(random.randint(65,90),),
        "number": chr(random.randint(0x1F600, 0x1F64F)),
        
    }

    return render(request, template_name, context) 

def show_all(request):
    template_name = 'quotes/show_all.html'
    context = {
        "quotes": quotes,   
        "images": images, 
        "number": chr(random.randint(0x1F600, 0x1F64F)),   
    }
    return render(request, template_name, context)





