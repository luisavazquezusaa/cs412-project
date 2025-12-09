# File: views.py 
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 09/19/2025
# Description: Views for the app restaurant

from django.shortcuts import render
import random
import time
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.

specials = [
    'Enchiladas', 
    'Flautas', 
    'Pozole',
    'Enfrijoladas', 
    'Torta', 
]


def order_page(request): 
    '''Respond to URL', delegate work to a template'''
    template_name = 'restaurant/order.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        "Special": random.choice(specials),
        
    }

    return render(request, template_name, context) 

def main(request): 

    template_name = 'restaurant/main.html'

    return render(request, template_name, )

def submit (request): 
    "Process the form submission, and generate a result"

    template_name = "restaurant/confirmation.html"

    prices = {
        "Tacos Carnitas": 10.5,
        "Tacos Chicken": 10.5,
        "Burrito": 12,
        "Quesadilla": 11,
        "Bowl": 13,
        "Special": 12,
    }

    total = 0

    print(request.POST)

    if request.POST:
        order = []
        total = 0

        order = [
            'Tacos Carnitas' if 'Carnitas' in request.POST else None,
            'Tacos Chicken' if 'Chicken' in request.POST else None,
            'Burrito' if 'Burrito' in request.POST else None,
            'Quesadilla' if 'Quesadilla' in request.POST else None,
            'Bowl' if 'Bowl' in request.POST else None,
            request.POST['special'] if 'special' in request.POST else None,
        ]   

        order = [item for item in order if item]


        for item in order:
            if item in prices:  
                total += prices[item]
            elif 'special' in request.POST:   
                total += prices["Special"]

        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_request = request.POST['special_request'] if 'special_request' in request.POST else ""
       
        minutes_add = random.randint(30, 60) 
        order_timeX = time.time() + minutes_add * 60 
        order_time = time.strftime("%I:%M %p on %b %d, %Y", time.localtime(order_timeX))

        context = {
            'order' : order,
            'total' : total,
            'name': name,
            'phone': phone,
            'email': email,
            'special_request' : special_request,
            'order_time': order_time
        }

    return render(request, template_name, context)