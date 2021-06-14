from django.db import models
from django.db.models import Q

#Use model managers for queries, define search function that filters based on q input.

class accessionLookup(models.Model):
    list = models.TextField(null = True)

class uniProteinManager(models.Manager):
    def search(self, query):
        qs = self.get_queryset()
        set = Q(accession__icontains = query)
        qs = qs.filter(set).distinct()

        return qs

class simProteinManager(models.Manager):
    def search(self, query):
        qs = self.get_queryset()
        set = Q(accession__icontains = query)
        qs = qs.filter(set).distinct()

        return qs

class uniProtein(models.Model):
    accession = models.CharField(max_length = 10, primary_key = True)
    alpha = models.FloatField(default = 0)
    beta = models.FloatField(default = 0)
    turn = models.FloatField(default = 0)
    unknown = models.FloatField(default = 1)
    known = models.FloatField(default = 0)
    length = models.IntegerField()

    uniManage = uniProteinManager()

    def __str__(self):
        return self.accession

class simProtein(models.Model):
    accession = models.CharField(max_length = 20)
    simType = models.CharField(max_length = 4, default = '')
    alpha = models.FloatField(default = 0)
    beta = models.FloatField(default = 0)
    turn = models.FloatField(default = 0)
    length = models.IntegerField()

    simManage = simProteinManager()

    def __str__(self):
        return self.accession