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
        if "accession" in nameCheck:
            df.columns = df.columns.str.replace(name, "Accession")
        if any(colName in nameCheck for colName in helixMatches):
            df.columns = df.columns.str.replace(name, "Alpha")
        elif any(colName in nameCheck for colName in betaMatches):
            df.columns = df.columns.str.replace(name, "Beta")
        elif any(colName in nameCheck for colName in turnMatches):
            df.columns = df.columns.str.replace(name, "Turn")
        elif "known" in nameCheck and "unknown" not in nameCheck:
            df.columns = df.columns.str.replace(name, "Known")
        elif "unknown" in nameCheck:
            df.columns = df.columns.str.replace(name, "Unknown")
        elif "length" in nameCheck:
            df.columns = df.columns.str.replace(name, "Length")
    return df
