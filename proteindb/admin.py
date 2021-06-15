from django.contrib import admin
from . import models

# Regsiters the protein models on the admin page of the app, such that they can be added/edited manually and viewed for errors.
admin.site.register(models.simProtein)
admin.site.register(models.uniProtein)
admin.site.register(models.csvAccession)