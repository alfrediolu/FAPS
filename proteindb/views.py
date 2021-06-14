from django.views.generic.base import View
from . models import uniProtein, simProtein, csvAccession
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from . handlers import accessionGrabber
from itertools import chain

# Functions as the index of the web app, no interaction outside of the HTML tags.
class index(TemplateView):
    template_name = "index.html"

# Takes the search input from index.html and runs a query with it for one protein.
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

# Functions as the redirect page if the .csv upload in invalid.
class csvSearchInvalid(TemplateView):
    template_name = "csvInvalid.html"

# Deals with the POST request from uploading a .csv and creates a temporary model for it to be retrieved later.
class csvSearch(View):
    template_name = "csvSearch.html"

    def post(self, request):
        if request.POST and request.FILES:
            uploadedCSV = request.FILES['uploadedCSV']
            if uploadedCSV.name.endswith('.csv'):
                accessionList = accessionGrabber(uploadedCSV)
                for entry in accessionList:
                    lookup = csvAccession(accession = entry)
                    lookup.save()
                return redirect('/csvsearch/results')
            else:
                return redirect('/csvsearch/invalid')
        else:
            return redirect('/csvsearch/invalid')

# Takes the model created above and allows the HTML file to read it and format it for the tables.
class csvSearchResults(ListView):
    template_name = "csvSearch.html"
    context_object_name = "csvuni_list"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['csvsim_list'] = []
        accessionList = list(csvAccession.objects.all())
        for entry in accessionList:
            results = simProtein.simManage.search(entry).order_by('accession')
            context['csvsim_list'] = chain(context['csvsim_list'], results)
        return context

    def get_queryset(self):
        savedAccessions = csvAccession.objects.all()
        accessionList = list(savedAccessions)
        for entry in accessionList:
            results = uniProtein.uniManage.search(entry).order_by('accession')
            uniResults = chain(uniResults, results)
        savedAccessions.delete()
        return uniResults