from django.shortcuts import render
from . models import uniProtein, simProtein
from django.views.generic import TemplateView, ListView, FormView, CreateView, View
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

class csvSearchResults(View):
    template_name = "csvSearchResults.html"
    context_object_name = 'uni_list'

    def csvUpload(self,request):
        if request.POST and request.FILES:
            uploadedCSV = request.FILES['uploadedCSV']
            if uploadedCSV.is_valid():
                accessionGrabber(uploadedCSV)
        return render(request, 'csvSearch.html')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sim_list']
        return context

class singleUniprotUploader(CreateView):
    template_name = "protUploader.html"
    model = uniProtein
    fields = ['Accession', 'a-Helix', 'b-Sheet', 'Turn', 'Unknown', 'Known', 'Length']

class singleSimProtUploader(CreateView):
    template_name = "protUploader.html"
    model = uniProtein
    fields = ['Accession', 'simType', 'a-Helix', 'b-Sheet', 'Turn', 'Length']