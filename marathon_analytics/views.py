from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Result

# Create your views here.
class ResultsListView(ListView):
    '''View to display marathon results'''
 
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 25 #how many records per page
 
    def get_queryset(self):
        
        results = super().get_queryset()
        #return qs[:25]  # #limit results to first 25 records 

        if 'city' in self.request.GET:
            city = self.request.GET['city']

            if city: 
                results = results.filter(city=city)
        
        return results

