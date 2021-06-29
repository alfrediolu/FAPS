import pandas as pd

# This file serves as handlers to simplify the code found in views. The names should tell you what each one does from views.py, but more documentation has been added here.


# Grabs a list of accession codes from the uploaded .csv file. Pandas is required for this, because .columns is a function of a pandas dataframe.
def accessionGrabber(csv):
    if 'Accession' in csv.columns:
        accessionList = csv['Accession']
    return accessionList

# Standardizes the column names of the uploaded .csv file so they can be indexed without having to search by potential matches while adding data to the db.
def columnRename(df):
    colNames = df.columns
    helixMatches = ["helix", "alpha", "a-helix"]
    betaMatches = ["beta", "sheet", "b-sheet"]
    turnMatches = ["turn", "random", "coil"]

    for name in colNames:
        nameCheck = name.lower()
        if any(colName in nameCheck for colName in helixMatches):
            df = df.rename({name: 'a-Helix'}, axis = 'columns', inplace = True)
        elif any(colName in nameCheck for colName in betaMatches):
            df = df.rename({name: 'b-Sheet'}, axis = 'columns', inplace = True)
        elif any(colName in nameCheck for colName in turnMatches):
            df = df.rename({name: 'Turn'}, axis = 'columns', inplace = True)
    print(df)
    return df
