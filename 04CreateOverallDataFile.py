""" --------------------------------------------------------------------------------------------------------
File:		Create Overall Data file
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-19
Descr		The purpose of this script is to create the overall data file. This
            is done by opening each of the individual stock files and 
            concatenating the data into a single data frame. This later 
            dataframe is then outputted as '../Data/MasterData.csv'

"""

# import the Python Libraries
import pandas as pd	     # library for Pandas

# Read in the list of tickers from 'masterFIleList.csv'
colNames = ['index','filename']
fileListDF = pd.read_csv('../Data/MasterFileList.csv', names=colNames)
print ( fileListDF.info() )
print ( fileListDF.head(10) )

# load the first datafile into the dataframe.
print (fileListDF.loc[0,'filename'])
masterDF = pd.read_csv (fileListDF.loc[0,'filename'], parse_dates=(['date']), index_col=['symbol','date'])
print ( masterDF.info() )
print ( masterDF.head(10) )

# now remove the first record from the fileListDF so that we do not use it 
# again
fileListDF = fileListDF.loc[1:,'filename']

# iterate through the remaining files, loading each one, one at a time. Once 
# the file is loaded, it is concatenated on to master DF
for filename in fileListDF:
    
    currentDF = pd.read_csv (filename, parse_dates=(['date']), index_col=['symbol','date'])
    masterDF = pd.concat ([masterDF, currentDF])

#Examine 
print (masterDF.shape)
print ( masterDF.info() )

masterDF.to_csv ('../Data/masterData.csv', encoding='utf-8' )