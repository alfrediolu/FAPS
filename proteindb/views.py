from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView
from itertools import chain

class index(TemplateView):
    template_name = "index.html"

class searchResults(ListView):
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        uniResults = uniProtein.objects.search(query)
        simResults = simProtein.objects.search(query)
        qs_combined = chain(uniResults, simResults)
        qs = sorted(qs_combined)
        return qs