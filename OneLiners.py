import os
import arcpy

import pandas as pd

#Create a Pandas DataFrame out of a ArcGIS feature class - must have env set to dir containing feature class to convert.
FCtoDF = lambda x: pd.DataFrame([r for r in arcpy.da.SearchCursor(x,'*')],columns=[f.name for f in arcpy.ListFields(x)])

#Find all of the files in a directory (fp) if they contain a string of interest (soi) - works recursively
findFiles = lambda fp,soi: [os.path.join(r,f) for r,_,fs in os.walk(fp) for f in fs if soi in f]

#Convert a DMS string seperated by spaces e.g. 51 43 19.533 to a DD value e.g. 51.722093
DMStoDD = lambda row: sum([x/y for x, y in zip([float(x) for x in row[:-1].split(' ')], [1, 60, 3600])]) * (-1 if row[-1] in ('S', 'W') else 1)

#More to come...
