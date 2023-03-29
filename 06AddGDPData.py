""" --------------------------------------------------------------------------------------------------------
File:		Sumarize CLosing Data
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-27
Descr		The purpose of this script is merge the main dataset with the GDP dataset.
            
            Steps
            1) Read in the main data set from file "closingData.csv"
            2) Read in the GDP data set from the file "GDP.CSV". Note we only import the 
               columns "Time", "LOCATION", "Value", "VARIABLE".
            3) Check the values in the "VARIABLE" and "LOCATION"
            4) Create a new dataframe for the USA GDP including only the Year on year 
               tracking data by slicing the data with LOCATION = "USA" and 
               VARIABLE = "TRACKER_YOY".
            5) Create a date range of days based on the starting and ending date of the 
               main dataset
            6) Reindex the data frame across all the days using the "nearest" method to 
               assign missing values.
            7) Interpolate the value column to fill in the missing values.
            8) Merge the data into the main dataset (closing dataset) and rename the 
               column to USA_GDP.
            
            8) Repeat steps 4-8 with LOCATION = "GBR" to create a dataframe for the
               UK GDP renaming the column as GBR_GDP
            9) store the data in a file called "closingDataGDP.csv"

""" 

# import the Python Libraries
import pandas as pd	              # library for pandas

# Read in the data from the closingData file
closingOnlyDF = pd.read_csv  ('../Data/closingData.csv', parse_dates=(['Time']), index_col=['Time'] )
closingOnlyDF.info()
closingOnlyDF.head(20)

# Read in teh GDP database and check that the data is okay. This analysis is only interested in four fields, 
# Time, LOCATION, Value and Variable and the remainder are ignored. The Time field is used as the Index
GDPDF = pd.read_csv ('../Data/GDP.csv', parse_dates=(['Time']), usecols=['Time','LOCATION','Value','VARIABLE'], index_col=['Time'])
GDPDF.info()
GDPDF.isna().any()
GDPDF.head(10)

# Check the 'VARIABLE' field
GDPDF.groupby('VARIABLE').count()

# Check the 'LOCATION' field
GDPDF.groupby('LOCATION').count()

#
#   USA GDP
#
# Create a new dataframe only containing data from 'USA' and only containing the Tracker_YOY values.
GDPDF_USA = pd.DataFrame(GDPDF[(GDPDF['LOCATION']=='USA') & (GDPDF['VARIABLE']=='TRACKER_YOY')]['Value']).sort_index()

# ensure we have rows for all dates in the time range by reindexing the data.
days = pd.date_range (freq="D", start=closingOnlyDF.index.min(), end=closingOnlyDF.index.max())
GDPDF_USA = pd.DataFrame(GDPDF_USA.reindex(days, method="nearest"))

# use the interpolate function to "fill in the blanks". Assumption (again) is that there are no significant fluctuations 
# in the missing data.
GDPDF_USA = GDPDF_USA.interpolate(method='linear')
GDPDF_USA.sort_index(ascending=False).head(10)

# Merge the data with the closingOnlyDF dataframe calling the resulting new field "USA_GDP"
closingOnlyDF = pd.merge ( closingOnlyDF, GDPDF_USA, left_index=True, right_index=True, how="left" )
closingOnlyDF.rename(columns={'Value': 'USA_GDP'}, inplace=True)
closingOnlyDF.info()

# Check how many blanks there are.
closingOnlyDF[closingOnlyDF['USA_GDP'].notna()].head(10)

#
#   GBR GDP
#
# Create a new dataframe only containing data from 'GBR' and only containing the Tracker_YOY values.
GDPDF_GB = pd.DataFrame(GDPDF[(GDPDF['LOCATION']=='GBR') & (GDPDF['VARIABLE']=='TRACKER_YOY')]['Value']).sort_index()

# ensure we have rows for all dates in the time range by reindexing the data.
GDPDF_GB = pd.DataFrame(GDPDF_GB.reindex(days, method="nearest"))

# use the interpolate function to "fill in the blanks". Assumption (again) is that there are no significant fluctuations 
# in the missing data.
GDPDF_GB = GDPDF_GB.interpolate(method='linear')
GDPDF_GB.sort_index(ascending=False).head(10)

# Merge the data with the closingOnlyDF dataframe calling the resulting new field "USA_GDP"
closingOnlyDF = pd.merge ( closingOnlyDF, GDPDF_GB, left_index=True, right_index=True, how="left" )
closingOnlyDF.rename(columns={'Value': 'GBR_GDP'}, inplace=True)
closingOnlyDF.info()

# Check how many blanks there are.
closingOnlyDF[closingOnlyDF['GBR_GDP'].notna()].head(10)

# Store the closing dataframe as a CSV (this is a break point)
closingOnlyDF.info()
closingOnlyDF.to_csv('../Data/closingDataGDP.csv', encoding='utf-8')
