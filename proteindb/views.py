from django.views.generic.base import View
from . models import uniProtein, simProtein, csvAccession, masterProtein
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from . handlers import accessionGrabber, columnRename
from itertools import chain
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
import requests
import json
import traceback

# Functions as the index of the web app, housing all searches and buttons. See index.html for more detail.
class index(ListView):
    template_name = "index.html"
    context_object_name = 'db_size'

    def get_queryset(self):
        size = []
        masterResults = masterProtein.masterManage.search('')
        size.append(str(len(masterResults)))
        return size

# Instructions on how to use this webpage
class helps(TemplateView):
    template_name = "help.html"


# Takes the search input from index.html and runs a query with it for one protein (or any matches to the entry).
# Search results are reorganized into a list to display in the way Dr. Sun wanted. Also calculates overall percents.
# If no sim entry exists, it won't show up in the search - if no Uniprot entry exists, it defaults to a 0 vector with 100% unknown.
class searchResults(ListView):
    template_name = "searchResults.html"
    context_object_name = 'prot_list'

    def get_queryset(self):
        query = self.request.GET.get('id') # change q to id to be more readable. 
        finalResults = []
        if query == '':
            return finalResults
        masterResults = masterProtein.masterManage.search(query).order_by('accession')

        for master in masterResults:
            masterUnis = master.uni.all().order_by('accession')
            protein_name = fetchProteinName(master.accession)
            if masterUnis.count() == 0:
                uniData = [0,0,0,0,100,0]
            else:
                masterUni = masterUnis.first()
                uniData = [masterUni.alpha, masterUni.beta, masterUni.turn, masterUni.known, masterUni.unknown, masterUni.length]
            masterSims = master.sim.all().order_by('simType')

            for sim in masterSims:
                simData = [sim.accession, sim.simType, sim.alpha, sim.beta, sim.turn, sim.length]
                dataList = list(chain(simData, uniData))
                overallAlpha = (simData[2]*uniData[4] + uniData[0]*uniData[3])/100
                overallBeta = (simData[3]*uniData[4] + uniData[1]*uniData[3])/100
                overallTurn = (simData[4]*uniData[4] + uniData[2]*uniData[3])/100
                overallOther = 100 - (overallAlpha+overallBeta+overallTurn)
                dataList.append(overallAlpha)
                dataList.append(overallBeta)
                dataList.append(overallTurn)
                dataList.append(overallOther)
                dataList.append(protein_name)
                finalResults.append(dataList)
        return finalResults

def fetchProteinName(accession):
    """ Retreive the protein name based on the accession code of the protein.
    Arguments:
        accession: accession code of protein
    Returns:
        String represents the protein name otherwise, empty.
    """
    name=""
    response = requests.get(f"https://rest.uniprot.org/uniprotkb/{accession}")
    if(response):
        accession_data = json.loads(response.text)
        try:
            name = accession_data["proteinDescription"]["recommendedName"]["fullName"]["value"]
        except:
            name=accession
    return name

class chartResults(ListView):
    """ The details page representing a list of protein properties with chart for alpha, beta and turn values. 
    It takes the id from the search input in homepage.
    Paramaters: 
        id: represent the accession code of protein
    """
    template_name = "chartResult.html"
    context_object_name = 'prot_list'

    def get_queryset(self):
        query = self.request.GET.get('id')
        finalResults = []
        if query == '':
            return finalResults
        query = query.split(',')
        masterResults = masterProtein.masterManage.filter(
            accession__in=query).order_by('accession')

        for master in masterResults:
            masterUnis = master.uni.all().order_by('accession')
            protein_name = fetchProteinName(master.accession)
            if masterUnis.count() == 0:
                uniData = [0, 0, 0, 0, 100, 0]
            else:
                masterUni = masterUnis.first()
                uniData = [masterUni.alpha, masterUni.beta, masterUni.turn,
                           masterUni.known, masterUni.unknown, masterUni.length]
            masterSims = master.sim.all().order_by('simType')

            for sim in masterSims:
                simData = [sim.accession, sim.simType,
                           sim.alpha, sim.beta, sim.turn, sim.length]
                dataList = list(chain(simData, uniData))
                overallAlpha = (simData[2]*uniData[4] +
                                uniData[0]*uniData[3])/100
                overallBeta = (simData[3]*uniData[4] +
                               uniData[1]*uniData[3])/100
                overallTurn = (simData[4]*uniData[4] +
                               uniData[2]*uniData[3])/100
                overallOther = 100 - (overallAlpha+overallBeta+overallTurn)
                dataList.append(overallAlpha)
                dataList.append(overallBeta)
                dataList.append(overallTurn)
                dataList.append(overallOther)
                dataList.append(protein_name)
                finalResults.append(dataList)
        return finalResults

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

# Takes the model created above and allows the HTML file to read it and format it for the table. Deletes it after use so it's not saved in the database.
class csvSearchResults(ListView):
    template_name = "searchResults.html"
    context_object_name = "prot_list"

    def get_queryset(self):
        savedAccessions = csvAccession.objects.all().order_by('accession')
        finalResults = []

        for csvEntry in savedAccessions:
            currentAccession = csvEntry.accession
            masterResults = masterProtein.masterManage.search(currentAccession).order_by('accession')

            for master in masterResults:
                print(master.accession)
                masterUnis = master.uni.all().order_by('accession')
                protein_name = fetchProteinName(master.accession)
                if masterUnis.count() == 0:
                    uniData = [0,0,0,0,100,0]
                else:
                    masterUni = masterUnis.first()
                    uniData = [masterUni.alpha, masterUni.beta, masterUni.turn, masterUni.known, masterUni.unknown, masterUni.length]
                masterSims = master.sim.all().order_by('simType')

                for sim in masterSims:
                    simData = [sim.accession, sim.simType, sim.alpha, sim.beta, sim.turn, sim.length]
                    dataList = list(chain(simData, uniData))
                    overallAlpha = (simData[2]*uniData[4] + uniData[0]*uniData[3])/100
                    overallBeta = (simData[3]*uniData[4] + uniData[1]*uniData[3])/100
                    overallTurn = (simData[4]*uniData[4] + uniData[2]*uniData[3])/100
                    
                    overallOther = 100 - (overallAlpha+overallBeta+overallTurn)
                    dataList.append(overallAlpha)
                    dataList.append(overallBeta)
                    dataList.append(overallTurn)
                    dataList.append(overallOther)
                    dataList.append(protein_name)
                    finalResults.append(dataList)
        csvAccession.objects.all().delete()
        return finalResults

# Allows the upload script to authenticate a user, such that database edits are not open to anyone.
@csrf_exempt
def uploadLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            print("User logged in with upload credentials.")
            return HttpResponse("Logged in successfully.")
        else:
            print("User attempted to login to upload; invalid credentials.")
            return HttpResponse("Login failed.")

# Receives data from HPC in the form of a JSON file. Saves it to database. Requires login to access for security purposes, and logs the user out after POST.
@csrf_exempt
def upload(request):
    failedUploads = []
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

                        if masterCount == 1:
                            print("Master protein found, checking if Uniprot entry already exists...")
                            masterProt = masterList.first()
                            uniCount = masterProt.uni.all().count()

                            if uniCount == 1:
                                print("Uniprot entry already exists for this protein, skipped.")
                                failedUploads.append(currentAccession)

                            elif uniCount == 0:
                                print("Uniprot entry not found for master, linking...")
                                uniData = uniProtein(accession = currentAccession, alpha = row.Alpha, beta = row.Beta,
                                turn = row.Turn, unknown = row.Unknown, known = row.Known, length = row.Length, master = masterProt)
                                uniData.save()

                            else:
                                print("Multiple Uniprot entries found, cannot create entry. Contact database administrator ASAP.")
                                failedUploads.append(currentAccession)

                        elif  masterCount == 0:
                            print("No master protein found, creating and linking...")
                            masterProt = masterProtein(accession = currentAccession)
                            masterProt.save()
                            uniData = uniProtein(accession = currentAccession, alpha = row.Alpha, beta = row.Beta,
                            turn = row.Turn, unknown = row.Unknown, known = row.Known, length = row.Length, master = masterProt)
                            uniData.save()

                        else:
                            print("Multiple master proteins found, cannot create entry. Contact database administrator ASAP.")
                            failedUploads.append(currentAccession)         
                else:
                    print("Data is simulated.")
                    for row in data.itertuples(index = False, name = 'protein'):
                        currentAccession = row.Accession
                        print(currentAccession)
                        masterList = masterProtein.masterManage.search(currentAccession)
                        masterCount = masterList.count()

                        if masterCount == 1:
                            print("Master protein found, checking if simProtein of same simType exists...")
                            masterProt = masterList.first()
                            existingSims = masterProt.sim.all()
                            simTypeMatch = False
                            for sim in existingSims:
                                if sim.simType == row.Type:
                                    print("dataType match, cannot create entry; skipped.")
                                    simTypeMatch = True
                                    failedUploads.append(currentAccession)
                            if not simTypeMatch:
                                print("Master has no sim with matching dataType, adding...")
                                protLength = row.Alpha + row.Beta + row.Turn + row.Unknown
                                if protLength == 0:
                                    continue
                                if row.Type == 'SWI':
                                    simData = simProtein(accession = currentAccession, alpha = row.Alpha/protLength*100, beta = row.Beta/protLength*100,
                                    turn = row.Turn/protLength*100, simType = row.Type, length = protLength, master = masterProt)
                                    simData.save()
                                else:
                                    simData = simProtein(accession = currentAccession, alpha = row.Alpha/row.Length*100, beta = row.Beta/row.Length*100,
                                    turn = row.Turn/row.Length*100, simType = row.Type, length = row.Length, master = masterProt)
                                    simData.save()

                        elif  masterCount == 0:
                            print("No master protein found, creating and linking...")
                            masterProt = masterProtein(accession = currentAccession)
                            masterProt.save()
                            protLength = row.Alpha + row.Beta + row.Turn + row.Unknown
                            if protLength == 0:
                                continue
                            if row.Type == 'SWI':
                                simData = simProtein(accession = currentAccession, alpha = row.Alpha/protLength*100, beta = row.Beta/protLength*100,
                                turn = row.Turn/protLength*100, simType = row.Type/protLength, length = protLength, master = masterProt)
                                simData.save()
                            else:
                                simData = simProtein(accession = currentAccession, alpha = row.Alpha/row.Length*100, beta = row.Beta/row.Length*100,
                                turn = row.Turn/row.Length*100, simType = row.Type, length = row.Length, master = masterProt)
                                simData.save()

                        else:
                            print("Multiple master proteins found, cannot create entry. Contact database administrator ASAP.")
                            failedUploads.append(currentAccession)
            else:
                print("Did not contain a Type key, no data added.")
        except Exception as e:
            traceback.print_exc()
            logout(request)
            return HttpResponse("Error during upload/file read.")
        logout(request)
        return JsonResponse(failedUploads, safe = False)
    logout(request)
    return HttpResponse("Error, invalid access.")
