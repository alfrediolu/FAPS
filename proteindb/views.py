from . models import uniProtein, simProtein
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
import pandas as pd
from . handlers import accessionGrabber


class index(TemplateView):
    template_name = "index.html"

class searchResults(ListView):
    template_name = "searchResults.html"
    context_object_name = 'uni_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['sim_list'] = simProtein.simManage.search(query).order_by('accession')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        uniResults = uniProtein.uniManage.search(query).order_by('accession')
        return uniResults

class csvSearchResults(ListView):
    template_name = "csvSearch.html"
    context_object_name = 'uni_list'

    def post(self, request):
        if request.POST and request.FILES:
            uploadedCSV = request.FILES['uploadedCSV']
            if uploadedCSV.name.endswith('.csv'):
                accessionList = accessionGrabber(uploadedCSV)
                return redirect('csvsearch/')
            else:
                return redirect('invalid/')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['sim_list'] = simProtein.simManage.search(query).order_by('accession')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        uniResults = uniProtein.uniManage.search(query).order_by('accession')
        return uniResults

class csvSearchInvalid(TemplateView):
    template_name = "csvInvalid.html"