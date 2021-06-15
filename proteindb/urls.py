from django.urls import path
from . views import index, searchResults, csvSearchResults, csvSearchInvalid, csvSearch

# Defines URLs for the page.
# - index houses all the original input/search forms.
# - search houses the search results for single-protein inputs.
# - csvsearch acts as an intermediate between others and should not be accessed by itself.
# - csvsearch/invalid is a redirect page if a .csv upload is invalid or not correct.
# - csvsearch/results renders the results of the .csv-based search.
urlpatterns = [
    path('', index.as_view(), name = "index"),
    path('search/', searchResults.as_view(), name = "searchresults"),
    path('csvsearch/', csvSearch.as_view(), name = "csvsearch"),
    path('csvsearch/invalid', csvSearchInvalid.as_view(), name = "csvsearchinvalid"),
    path('csvsearch/results', csvSearchResults.as_view(), name = "csvsearchresults")
]
