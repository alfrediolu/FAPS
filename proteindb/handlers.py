from mmap import ACCESS_COPY
import pandas as pd

def accessionGrabber(csv):
    if 'Accession' in csv.columns:
        accessionList = csv['Accession']
        return accessionList

def accessionColumnChecker(csv):
    if 'Accession' in csv:
        return True
    else:
        return False
