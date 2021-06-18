from mmap import ACCESS_COPY
import pandas as pd

# Grabs a list of accession codes from the uploaded .csv file. Pandas is required for this, because .columns is a function of a pandas dataframe.
def accessionGrabber(csv):
    if 'Accession' in csv.columns:
        accessionList = csv['Accession']
        return accessionList