from typing import ChainMap
from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView
from django.db.models import Q

class index(TemplateView):
    template_name = "index.html"

class uniSearchResults(ListView):
    model = uniProtein
    context_object_name = 'uniList'
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        uniList = uniProtein.objects.filter(Q(accession__icontains = query))
        return uniList

class simSearchResults(ListView):
    model = simProtein
    context_object_name = 'simList'
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        simList = simProtein.objects.filter(Q(accession__icontains = query))
        return simList