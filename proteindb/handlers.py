from mmap import ACCESS_COPY
import pandas as pd

def accessionGrabber(csv):
    readCSV = pd.read_csv(csv, delimiter = ',')
    if 'Accession' in readCSV.columns:
        accessionList = readCSV['Accession']
        return accessionList
