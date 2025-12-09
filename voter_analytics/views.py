# File: views.py
# Author: Luisa Vazquez Usabiaga (lvu@bu.edu), 10/29/2025
# Description: this file is my views for voter_analytics

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models.functions import ExtractYear
from django.db.models import Count, Q


## new imports: for the plotly library
import plotly
import plotly.graph_objs as go

# Create your views here.

class VoterListView (ListView):
    ''' Define a view class to display all voters'''

    model = Voter 
    template_name = "voter_analytics/show_all_voters.html" 
    context_object_name = "voters"
    paginate_by = 100 #how many records per page

    def get_queryset(self):

        #ordered alphabetically
        voter = super().get_queryset().order_by('last_name', 'first_name')

        party = self.request.GET.get('party', '').strip()
        min_year = self.request.GET.get('min_year', '')
        max_year = self.request.GET.get('max_year', '')
        voter_score = self.request.GET.get('voter_score', '')
        elections = self.request.GET.getlist('elections')  # list for checkboxes

        if party:
            voter = voter.filter(party__iexact=party)
        if min_year:
            voter = voter.filter(date_birth__year__gte=min_year)
        if max_year:
            voter = voter.filter(date_birth__year__lte=max_year)
        if voter_score:
            voter= voter.filter(voter_score=voter_score)

        for election in elections:
            field = f"v{election}"
            if hasattr(Voter, field):
                voter = voter.filter(**{f"{field}": 1})

        return voter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_list'] = (
            Voter.objects.values_list('party', flat=True)
            .exclude(party__isnull=True)
            .distinct()
            .order_by('party')
        )
        context['year_list'] = (
            Voter.objects.annotate(year=ExtractYear('date_birth'))
            .values_list('year', flat=True)
            .exclude(year__isnull=True)
            .distinct()
            .order_by('year')
        )
        context['score_list'] = (
            Voter.objects.values_list('voter_score', flat=True)
            .exclude(voter_score__isnull=True)
            .distinct()
            .order_by('voter_score')
        )
        
        context['election_list'] = ["20state", "21town", "21primary", "22general", "23town"]
        context['selected_elections'] = self.request.GET.getlist('elections')

        return context
    
class VoterDetailView(DetailView):
    """information about a Voter"""
    model = Voter
    template_name = "voter_analytics/show_voter.html"
    context_object_name = "voter"

    def get_context_data(self, **kwargs):
        '''Provide context variables for use in the template'''
        context =  super().get_context_data(**kwargs)
        return context

class VoterGraphsView(ListView):
    '''display graphs of voter data'''
    
    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        ## for the histogram
        voters_by_year = (
            Voter.objects
            .annotate(year=ExtractYear('date_birth'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        years = [v['year'] for v in voters_by_year if v['year']]
        counts = [v['count'] for v in voters_by_year if v['year']]

        fig_year = go.Bar(x=years, y=counts, marker_color='blue')
        graph_div_birth = plotly.offline.plot(
            {"data": [fig_year],
             "layout": go.Layout(
                 title=f"Voter distribution by Year of Birth (n={sum(counts)})",
                 xaxis_title="Year of Birth",
                 yaxis_title="Number of Voters"
             )},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_birth'] = graph_div_birth


         ## for the pie chart
        party_counts = (
            Voter.objects
            .values('party')
            .annotate(count=Count('id'))
            .exclude(party__isnull=True)
            .order_by('party')
        )

        party_labels = [p['party'] for p in party_counts]
        party_values = [p['count'] for p in party_counts]

        fig_party = go.Pie(labels=party_labels, values=party_values, hole=0)
        graph_div_party = plotly.offline.plot(
            {"data": [fig_party],
             "layout": go.Layout(
                 title=f"Voter distribution by Party Affiliation (n={sum(party_values)})"
             )},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_party'] = graph_div_party


        ## for the bar chart
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = []

        for field in election_fields:
            count = Voter.objects.filter(**{f"{field}": 1}).count()
            election_counts.append(count)

        fig_elections = go.Bar(x=election_fields, y=election_counts, marker_color='purple')
        graph_div_elections = plotly.offline.plot(
            {"data": [fig_elections],
             "layout": go.Layout(
                 title=f"Vote Count by Election (n={Voter.objects.count()})",
                 xaxis_title="Election",
                 yaxis_title="Voters Who Participated"
             )},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_elections'] = graph_div_elections

        return context





# Create your views here.
# class ResultsListView(ListView):
#     '''View to display marathon results'''
 
#     template_name = 'marathon_analytics/results.html'
#     model = Result
#     context_object_name = 'results'
#     paginate_by = 25 #how many records per page
 
#     def get_queryset(self):
        
#         results = super().get_queryset()
#         #return qs[:25]  # #limit results to first 25 records 

#         party = self.request.GET.get('party', '').strip()
#         min_year = self.request.GET.get('min_year', '')
#         max_year = self.request.GET.get('max_year', '')
#         voter_score = self.request.GET.get('voter_score', '')
#         elections = self.request.GET.getlist('elections')

#         if 'city' in self.request.GET:
#             city = self.request.GET['city']

#             if city: 
#                 results = results.filter(city=city)
        
#         return results
