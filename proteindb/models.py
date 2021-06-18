from django.db import models
from django.db.models import Q

# Provides custom lookup function for the master model.
class masterProteinManager(models.Manager):
    def search(self, query):
        qs = self.get_queryset()
        set = Q(accession__icontains = query)
        qs = qs.filter(set).distinct()
        return qs

# Master protein used for querying both models at same time.
class masterProtein(models.Model):
    accession = models.CharField(max_length = 20, primary_key = True)
    name = models.CharField(max_length = 50, default = '')

    masterManage = masterProteinManager()

    def __str__(self):
        return self.accession

# Provides a custom lookup function for the unis.
class uniProteinManager(models.Manager):
    def search(self, query):
        qs = self.get_queryset()
        set = Q(accession__icontains = query)
        qs = qs.filter(set).distinct()
        return qs

# Provides a custom lookup function for the sims.
class simProteinManager(models.Manager):
    def search(self, query):
        qs = self.get_queryset()
        set = Q(accession__icontains = query)
        qs = qs.filter(set).distinct()
        return qs

# Represents the bioinformatics/Uniprot proteins.
class uniProtein(models.Model):
    accession = models.CharField(max_length = 10, primary_key = True)
    alpha = models.FloatField(default = 0)
    beta = models.FloatField(default = 0)
    turn = models.FloatField(default = 0)
    unknown = models.FloatField(default = 1)
    known = models.FloatField(default = 0)
    length = models.IntegerField()
    master = models.ForeignKey(to = masterProtein, default = None, on_delete = models.CASCADE, unique = True, related_name = 'uni')

    uniManage = uniProteinManager()

    def __str__(self):
        return self.accession

# Represents the simulated proteins.
class simProtein(models.Model):
    accession = models.CharField(max_length = 20)
    simType = models.CharField(max_length = 4, default = '')
    alpha = models.FloatField(default = 0)
    beta = models.FloatField(default = 0)
    turn = models.FloatField(default = 0)
    length = models.IntegerField()
    master = models.ForeignKey(to = masterProtein, default = None, on_delete = models.CASCADE, related_name = 'sim')

    simManage = simProteinManager()

    def __str__(self):
        return self.accession

# Temporary storage of a list of accessions from a .csv upload. Deleted after use, so there should never be any of these actively stored in the database.
class csvAccession(models.Model):
    accession = models.CharField(max_length = 20)
