import os
import arcpy

from collections import Counter

import pandas as pd

#Create a Pandas DataFrame out of a ArcGIS feature class table - must have env set to dir containing feature class to convert.
FCtoDF = lambda x: pd.DataFrame([r for r in arcpy.da.SearchCursor(x,'*')],columns=[f.name for f in arcpy.ListFields(x)])

#Find all of the files in a directory (fp) if they contain a string of interest (soi) - works recursively
findFiles = lambda fp,soi: [os.path.join(r,f) for r,_,fs in os.walk(fp) for f in fs if soi in f]

#Convert a DMS string seperated by spaces e.g. 51 43 19.533N to a DD value e.g. 51.722093
DMStoDD = lambda row: sum([x/y for x, y in zip([float(x) for x in row[:-1].split(' ')], [1, 60, 3600])]) * (-1 if row[-1] in ('S', 'W') else 1)

#Get the number of occurences for each of the values found in 'field' in the feature class 'fc'.
fieldValCounter = lambda fc,field: dict(Counter([str(row[0]).encode('ascii') for row in arcpy.da.SearchCursor(fc,field)])


#Highlight specific values in a pandas dataframe using the style attribute and apply method.]
highVal = lambda data,value:['background-color:red;font-weight:bold' if row==value else '' for row in data]
#Usage: styledDF = df.style.apply(highVal,value='VALUE_TO_HIGHLIGHT',subset=['col1','col2','col3'])                                       

                                        
#More to come...
