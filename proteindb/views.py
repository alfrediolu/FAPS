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
        context['query'], query = self.request.GET.get('q')
        context['sim_list'] = simProtein.simManage.search(query).order_by('accession')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        uniResults = uniProtein.uniManage.search(query).order_by('accession')
        simResults = simProtein.simManage.search(query).order_by('accession')
        if len(simResults) == 0 and len(uniResults) == 0:
            qs = None
            return qs
        qs = list(chain(uniResults, simResults))
        return qs