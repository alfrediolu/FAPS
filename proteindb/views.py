from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView
from itertools import chain
import csv, re
from django.contrib import messages

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

def csvUpload(request):
    if request.method == 'POST':
           uploadedCSV = request.FILES['uploadedCSV']
    return render(request, 'csvSearch.html')


# def csvUpload(request):
#     if request.method == 'POST':
#         uploadedCSV = request.FILES['uploadedCSV']
#         accessionList = []

#         if not uploadedCSV.name.endswith('.csv'):
#             print("Invalid file uploaded")
#             return

#         else:
#             dataSet = uploadedCSV.read().decode('UTF-8')
#             csvReader = csv.reader(dataSet, delimiter = ',')
#             headers = []
#             for row in csvReader:
#                 headers.append(row)
#                 break

#             accessionCol = 0
#             validCSV = False

#             for colName in headers:
#                 colName = str(colName)
#                 if re.search('accession', colName, re.IGNORECASE):
#                     validCSV = True
#                 else:
#                     accessionCol += 1

#         if not validCSV:
#             print("Invalid CSV uploaded")
#             return

#         for rows in csvReader:
#             currentAccession = csvReader[accessionCol]
#             accessionList.append(currentAccession)

#         print(accessionList)
            
#     return render(request, 'csvSearch.html')
