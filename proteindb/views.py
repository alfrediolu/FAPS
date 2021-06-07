from typing import ChainMap
from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from itertools import chain

class index(TemplateView):
    template_name = "index.html"

class searchResults(ListView):
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        uniList = uniProtein.objects.filter(Q(accession__icontains = query))
        simList = simProtein.objects.filter(Q(accession__icontains = query))
        protein_list = chain(uniList, simList)
        return protein_list