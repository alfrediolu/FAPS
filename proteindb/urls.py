from django.urls import path
from django.views.generic import TemplateView
from . views import index, searchResults, csvSearchResults, csvSearchInvalid, csvSearch

urlpatterns = [
    path('', index.as_view(), name = "index"),
    path('search/', searchResults.as_view(), name = "searchresults"),
    path('csvsearch/', csvSearch.as_view(), name = "csvsearch"),
    path('csvsearch/invalid', csvSearchInvalid.as_view(), name = "csvsearchinvalid"),
    path('csvsearch/results', csvSearchResults.as_view(), name = "csvsearchresults")
]
