from django.contrib import admin
from . import models

# Regsiters the protein models on the admin page of the app, such that they can be added/edited manually and viewed for errors.
# Deleting masterProteins from the AdminCP should cascade and delete all affiliated sims and unis as well.
# csvAccessions are deleted after creation, so there should be none saved in the CP at any given time.
admin.site.register(models.masterProtein)
admin.site.register(models.simProtein)
admin.site.register(models.uniProtein)
admin.site.register(models.csvAccession)
