from django.shortcuts import render
from . models import protein
from django.views.generic import TemplateView, ListView
from django.db.models import Q

class index(TemplateView):
    template_name = "index.html"

class searchResults(ListView):
    model = protein
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = protein.objects.filter(Q(accession__icontains=query))
        return object_list