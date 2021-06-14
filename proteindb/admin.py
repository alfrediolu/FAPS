from django.contrib import admin
from . import models

admin.site.register(models.simProtein)
admin.site.register(models.uniProtein)
admin.site.register(models.csvAccession)