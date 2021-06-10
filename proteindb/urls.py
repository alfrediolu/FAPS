from django.urls import path
from django.views.generic import TemplateView
from . import views
from . views import index, searchResults, csvUploader

urlpatterns = [
    path('', index.as_view(), name = "index"),
    path('search/', searchResults.as_view(), name = "searchresults"),
    path('csvsearch/', csvUploader.as_view(), name = "csvsearch")
]
