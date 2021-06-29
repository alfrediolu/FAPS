from mmap import ACCESS_COPY
import pandas as pd

# Grabs a list of accession codes from the uploaded .csv file. Pandas is required for this, because .columns is a function of a pandas dataframe.
def accessionGrabber(csv):
    if 'Accession' in csv.columns:
        accessionList = csv['Accession']
        return accessionList

def columnRename(df):
    for i, val in enumerate(df.columns.values):
        currentHeader = val.lower()
        if 'helix' in currentHeader or 'alpha' in currentHeader:
            df.columns[i] = ('a-Helix')
        if 'sheet' in currentHeader or 'beta' in currentHeader:
            df.columns[i] = ('b-Sheet')
        if 'turn' in currentHeader or 'coil' in currentHeader or 'random' in currentHeader:
            df.columns[i] = ('Turn')
        if 'length' in currentHeader:
            df.columns[i] = ('Length')
    return df
