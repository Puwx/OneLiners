import os
import arcpy
import pandas as pd
from collections import Counter

#Create a Pandas DataFrame out of a ArcGIS feature class table - must have env set to dir containing feature class to convert.
FCtoDF = lambda x: pd.DataFrame([r for r in arcpy.da.SearchCursor(x,'*')],columns=[f.name for f in arcpy.ListFields(x)])

#Find all of the files in a directory (fp) if they contain a string of interest (soi) - works recursively
findFiles = lambda fp,soi: [os.path.join(r,f) for r,_,fs in os.walk(fp) for f in fs if soi in f]

#Convert a DMS string seperated by spaces e.g. 51 43 19.533N to a DD value e.g. 51.722093
DMStoDD = lambda row: sum([x/y for x, y in zip([float(x) for x in row[:-1].split()], [1, 60, 3600])]) * (-1 if row[-1] in ('S', 'W') else 1)

#Get the number of occurences for each of the values found in 'field' in the feature class 'fc'.
fieldValCounter = lambda fc,field: dict(Counter([str(row[0]).encode('ascii') for row in arcpy.da.SearchCursor(fc,field)])

#Highlight specific values in a pandas dataframe using the style attribute and apply method.]
highVal = lambda data,value:['background-color:red;font-weight:bold' if row==value else '' for row in data]
#Usage: styledDF = df.style.apply(highVal,value='VALUE_TO_HIGHLIGHT',subset=['col1','col2','col3'])                                       

#Converts and IntervalTree object to a Pandas DataFrame - keeps the data *Assumes no rows in df have same begin and end values
it_to_df = lambda it: pd.DataFrame([[*i] for i in sorted(it)],columns=["BEGIN","END","DATA"]) 
                                        
#Converts a DataFrame to an IntervalTree object - df = DataFrame, b = Begin column name, e = end column name, d = data column name
df_to_it = lambda df,b,e,d: IntervalTree([Interval(x[b],x[e],x[d]) for i,x in df.iterrows()])
                                        
#Create a grouped id column in pandas - ids with go from 0 to N-1 (N = number of items in each group) for each of the groups.
df["ID"] = df.groupby("GROUPS").apply(lambda x: list(range(0,len(x)))).explode().values # -> Reviewing this - unexpected results recently.                                                                 

#Create a dictionary of all the fields in an feature class and the associated attributes
fs = {f.name:{a:getattr(f,a) for a in dir(arcpy.Field()) if not a.startswith("_")} for f in arcpy.ListFields(fc)}
#Example of the out from function above:
"""
"{'REV':{'aliasName': 'REV',
'baseName': 'REV',
'defaultValue': None,
'domain': '',
'editable': True,
'isNullable': True,
'length': 254,
'name': 'REV',
'precision': 0,
'required': False,
'scale': 0,
'type': 'String'}}
"""
#Creates an arcpy Polyline from grouped arcpy points using a Pandas groupby object - meant to be used with arcgis python api SpatialDataFrames
groupPtsToLine = lambda d,g: d.groupby(g).agg({"SHAPE":lambda pts: arcpy.Polyline(arcpy.Array([arcpy.Point(*p) for p in pts]))})                                  
# d = DataFrame containing a column ("SHAPE") that has arcpy Point objects, g = field used to group the objects

#More to come...
