from django.db import models
from django.db.models.fields import IntegerField

class protein(models.Model):
    accession = models.CharField(max_length = 10, primary_key = True)

    def __str__(self):
        return self.accession

class uniProtein(models.Model):
    accession = models.CharField(max_length = 10, primary_key = True)
    alpha = models.FloatField(default = 0)
    beta = models.FloatField(default = 0)
    turn = models.FloatField(default = 0)
    unknown = models.FloatField(default = 1)
    known = models.FloatField(default = 0)
    length = models.IntegerField()

    def __str__(self):
        return self.accession

class simProtein(models.Model):
    simID = IntegerField(primary_key = True)
    accession = models.CharField(max_length = 10)
    simType = models.CharField(max_length = 3)
    alpha = models.FloatField(default = 0)
    beta = models.FloatField(default = 0)
    turn = models.FloatField(default = 0)
    length = models.IntegerField()

    def __str__(self):
        return self.simID