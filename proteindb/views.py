from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView
from itertools import chain

class index(TemplateView):
    template_name = "index.html"

class searchResults(ListView):
    template_name = "searchResults.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        uniResults = uniProtein.uniManage.search(query)
        simResults = simProtein.simManage.search(query)
        qs_combined = chain(uniResults, simResults)
        qs = sorted(qs_combined)
        return qs