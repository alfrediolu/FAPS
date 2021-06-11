import pandas as pd
import re
from itertools import chain

def accessionGrabber(csv):
    readCSV = pd.read_csv(csv, delimiter = ',')
    if 'Accession' in readCSV.columns:
        accessionList = readCSV['Accession']
        print(accessionList)
