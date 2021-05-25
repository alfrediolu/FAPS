from django.db import models

class protein(models.Model):
    accession = models.CharField(max_length = 10)
    dataType = models.CharField(max_length = 3, default = "")   #Represents the data source, either UNI for Uniprot or SIM from simulations.
    alpha = models.FloatField(default = 0)
    beta = models.FloatField(default = 0)
    turn = models.FloatField(default = 0)
    unknown = models.FloatField(default = 1)
    length = models.IntegerField()
    slug = models.SlugField(max_length = 255)   #Protein's URL slug. Shouldn't be applicable to user.

    def __str__(self):  #The protein model refers to itself by it's accession code when called.
        return self.accession
