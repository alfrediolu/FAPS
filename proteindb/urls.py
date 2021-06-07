from django.urls import path
from django.views.generic import TemplateView
from . import views
from . views import index, simSearchResults, uniSearchResults

urlpatterns = [
    path('', index.as_view(), name = "index"),
    path('search/', simSearchResults.as_view(), name = "searchresults"),
    path('search/', uniSearchResults.as_view(), name = "searchresults"),
]
