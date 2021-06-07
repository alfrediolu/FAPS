from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView
from django.db.models import Q

class index(TemplateView):
    template_name = "index.html"

class searchResults(ListView):
    model = simProtein, uniProtein
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        simList = simProtein.objects.filter(Q(accession__icontains = query))
        uniList = uniProtein.objects.filter(Q(accession__icontains = query))
        return simList, uniList