from django.views.generic.base import View
from . models import uniProtein, simProtein, csvAccession
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from . handlers import accessionColumnChecker, accessionGrabber
from itertools import chain
import pandas as pd

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
# Redirects the user to a page for an invalid lookup if the file is not a .csv, does not contain an 'Accession' column, or if no file was uploaded.
class csvSearch(View):
    template_name = "csvSearch.html"

    def post(self, request):
        if request.POST and request.FILES:
            uploadedCSV = request.FILES['uploadedCSV']
            if uploadedCSV.name.endswith('.csv'):
                readCSV = pd.read_csv(uploadedCSV, delimiter = ',')
                if accessionColumnChecker(readCSV):
                    accessionList = accessionGrabber(readCSV)
                    for entry in accessionList:
                        lookup = csvAccession(accession = entry)
                        lookup.save()
                    return redirect('/csvsearch/results')
                else:
                    return redirect('/csvsearch/invalid')
            else:
                return redirect('/csvsearch/invalid')
        else:
            return redirect('/csvsearch/invalid')

# Takes the model created above and allows the HTML file to read it and format it for the tables. Deletes it after use so it's not saved in the database.
class csvSearchResults(ListView):
    template_name = "csvSearch.html"
    context_object_name = "csvuni_list"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        simResults = []
        savedAccessions = csvAccession.objects.all().order_by('accession')

        for csvEntry in savedAccessions:
            currentAccession = csvEntry.accession
            results = simProtein.simManage.search(currentAccession).order_by('accession')
            simResults = chain(simResults, results)

        context['csvsim_list'] = simResults
        csvAccession.objects.all().delete()
        return context

    def get_queryset(self):
        savedAccessions = csvAccession.objects.all().order_by('accession')
        uniResults = []

        for csvEntry in savedAccessions:
            currentAccession = csvEntry.accession
            print(currentAccession)
            results = uniProtein.uniManage.search(currentAccession).order_by('accession')
            uniResults = chain(uniResults, results)

        return uniResults