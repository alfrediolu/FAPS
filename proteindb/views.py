from typing import ChainMap
from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView
from django.db.models import Q

class index(TemplateView):
    template_name = "index.html"

class searchResults(ListView):
    model = uniProtein, simProtein
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        uniprotein_list = uniProtein.objects.filter(Q(accession__icontains = query))
        simprotein_list = simProtein.objects.filter(Q(accession__icontains = query))
        return uniprotein_list, simprotein_list