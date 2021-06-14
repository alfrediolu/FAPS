from . models import uniProtein, simProtein, csvList
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
import simplejson as json
from . handlers import accessionGrabber
from itertools import chain


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

class csvSearchInvalid(TemplateView):
    template_name = "csvInvalid.html"

class csvSearch(ListView):
    template_name = "csvSearch.html"

    def post(self, request):
        if request.POST and request.FILES:
            uploadedCSV = request.FILES['uploadedCSV']
            if uploadedCSV.name.endswith('.csv'):
                accession = accessionGrabber(uploadedCSV)
                queryList = csvList()
                queryList.list = accession
                queryList.save()
                return redirect('/csvsearch/results')
            else:
                return redirect('/csvsearch/invalid')
        else:
            return redirect('/csvsearch/invalid')

class csvSearchResults(ListView):
    template_name = "csvSearch.html"
    context_object_name = "csvuni_list"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryList = csvList.objects.all
        query = queryList[0]
        jsonDec = json.decoder.JSONDECODER()
        accession = jsonDec.decode(query.list)
        context['csvsim_list'] = []
        for entry in accession:
            results = uniProtein.uniManage.search(entry).order_by('accession')
            context['csvsim_list'] = chain(context['csvsim_list'], results)
        return context

    def get_queryset(self):
        queryList = csvList.objects.all
        query = queryList[0]
        jsonDec = json.decoder.JSONDECODER()
        accession = jsonDec.decode(query.list)
        uniResults = []
        for entry in accession:
            results = uniProtein.uniManage.search(entry).order_by('accession')
            uniResults = chain(uniResults, results)
        queryList.delete()
        return uniResults