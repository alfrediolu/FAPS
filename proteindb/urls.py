from django.urls import path
from . views import index, searchResults, csvSearchResults, csvSearchInvalid

# Defines URLs for the page.
# - index houses all the original input/search forms.
# - search houses the search results for single-protein inputs.
urlpatterns = [
    path('', index.as_view(), name = "index"),
    path('search/', searchResults.as_view(), name = "searchresults"),
    path('csvsearch/invalid', csvSearchInvalid.as_view(), name = "csvsearchinvalid"),
    path('csvsearch/results', csvSearchResults.as_view(), name = "csvsearchresults")
]
