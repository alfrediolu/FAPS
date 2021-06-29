from django.views.decorators import csrf
from django.views.generic.base import View
from . models import uniProtein, simProtein, csvAccession, masterProtein
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from . handlers import accessionGrabber
from itertools import chain
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
        simResults = []
        masterResults = masterProtein.masterManage.search(query).order_by('accession')
        for master in masterResults:
            masterSims = master.sim.all().order_by('accession')
            simResults = chain(simResults, masterSims)
        context['sim_list'] = simResults
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        uniResults = []
        masterResults = masterProtein.masterManage.search(query).order_by('accession')
        for master in masterResults:
            masterUnis = master.uni.all().order_by('accession')
            uniResults = chain(uniResults, masterUnis)
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
                if 'Accession' in readCSV:
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
        masterResults = []
        savedAccessions = csvAccession.objects.all().order_by('accession')

        for csvEntry in savedAccessions:
            currentAccession = csvEntry.accession
            csvResults = masterProtein.masterManage.search(currentAccession).order_by('accession')
            masterResults = chain(masterResults, csvResults)
        for master in masterResults:
            masterUnis = master.sim.all().order_by('accession')
            simResults = chain(simResults, masterUnis)
        context['csvsim_list'] = simResults

        csvAccession.objects.all().delete()
        return context

    def get_queryset(self):
        savedAccessions = csvAccession.objects.all().order_by('accession')
        uniResults = []
        masterResults = []

        for csvEntry in savedAccessions:
            currentAccession = csvEntry.accession
            csvResults = masterProtein.masterManage.search(currentAccession).order_by('accession')
            masterResults = chain(masterResults, csvResults)
        for master in masterResults:
            print(master.accession)
            masterUnis = master.uni.all().order_by('accession')
            uniResults = chain(uniResults, masterUnis)

        return uniResults

# Receives data from HPC in the form of a JSON file. Saves it to database.
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        try:
            data = pd.read_json(request.body)
            print(data)
            if 'Data Type' in data:
                if data[data['Data Type'] == "UNI"]:
                    print("Data is UNI.")
                else:
                    print("Data is simulated.")
            else:
                print("Did not contain a dataType key, no data added.")
        except:
            return HttpResponse("Error")
        return HttpResponse("Data read successfully")
    return HttpResponse("Error")