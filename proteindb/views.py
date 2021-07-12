from django.views.generic.base import View
from . models import uniProtein, simProtein, csvAccession, masterProtein
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from . handlers import accessionGrabber, columnRename
from itertools import chain
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login

# Functions as the index of the web app, housing all searches and buttons. See index.html for more detail.
class index(TemplateView):
    template_name = "index.html"

# Takes the search input from index.html and runs a query with it for one protein. Showcases all results in table(s).
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

# Allows the upload script to authenticate a user, such that database edits are not open to anyone.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            print("User logged in with upload credentials.")
            return HttpResponse("Logged in successfully.")
        else:
            return HttpResponse("Login failed.")

# Receives data from HPC in the form of a JSON file. Saves it to database. Requires login to access for security purposes, and logs the user out after POST.
@csrf_exempt
def upload(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized.")
    if request.method == 'POST':
        try:
            data = pd.read_json(request.body)
            data = columnRename(data)
            data = data.fillna(0)

            if 'Type' in data.columns:
                if data['Type'].str.contains("UNI").any():
                    for row in data.itertuples(index = False, name = 'protein'):
                        currentAccession = row.Accession
                        print(currentAccession)
                        masterList = masterProtein.masterManage.search(currentAccession)
                        masterCount = masterList.count()

                        if masterCount != 1 and masterCount != 0:
                            print("Multiple master proteins found, cannot create entry. Contact database administrator ASAP.")

                        elif  masterCount == 0:
                            print("No master protein found, creating and linking...")
                            masterProt = masterProtein(accession = currentAccession)
                            masterProt.save()
                            uniData = uniProtein(accession = currentAccession, alpha = row.Alpha, beta = row.Beta,
                            turn = row.Turn, unknown = row.Unknown, known = row.Known, length = row.Length, master = masterProt)
                            uniData.save()

                        else:
                            print("Master protein found, checking if Uniprot entry already exists...")
                            masterProt = masterList.first()
                            uniCount = masterProt.uni.all().count()

                            if uniCount == 1:
                                print("Uniprot entry already exists for this protein, contact database administrator to edit.")

                            elif uniCount == 0:
                                print("Uniprot entry not found for master, linking...")
                                uniData = uniProtein(accession = currentAccession, alpha = row.Alpha, beta = row.Beta,
                                turn = row.Turn, unknown = row.Unknown, known = row.Known, length = row.Length, master = masterProt)
                                uniData.save()

                            else:
                                print("Multiple Uniprot entries found, cannot create entry. Contact database administrator ASAP.")
                else:
                    print("Data is simulated.")
            else:
                print("Did not contain a dataType key, no data added.")
        except:
            logout(request)
            return HttpResponse("Error")
        logout(request)
        return HttpResponse("Data read successfully")
    logout(request)
    return HttpResponse("Error")