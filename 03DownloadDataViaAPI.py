""" --------------------------------------------------------------------------------------------------------
File:		Download Data on individual stocks
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-19
Descr		The purpose of this script is to download specific data for a 
            list of stocks. It does this by downloading the data via the 
            marketplace API from a specified list of stock symbols.
            
            The overall list of stock symbols are stored in a CSV file called
            '../Data/tickers.csv'. The desired list of stocks are listed in a
            CSV file called '../Data/targetStocks.csv'.
            
            Each API call creates a file containing the data which is called
            'stock-data-'+<symbol>+'.csv' where <symbol> is the stock symbol.
            a master file containing the complete list of files is also stored 
            called 'masterFile.csv'

"""

# import the Python Libraries
import pandas as pd	     # library for Pandas
import requests          # library for the HTTP connection for the API call
import json		         # library for the JSON string processing. The API call will return a JSON string

# Read in the list of tickers from 'tickers2.csv'
tickersDF = pd.read_csv('../Data/tickers.csv', index_col='symbol')
print ( tickersDF.info() )
print ( tickersDF.head() )

# Read in the list of targeted stocks from 'targetStocks.csv'. 
# The file does not have columnsNames so the column names will be set as part
# of the import. 
columnNames = ['index', 'stock']
targetStocksDF = pd.read_csv('../Data/targetStocks.csv', names=columnNames, header=None, index_col='index')

# Just use the 'stock' column
targetStocksDF = targetStocksDF.loc[:,['stock']]
print ( targetStocksDF.info() )
print ( targetStocksDF.head(10) )

# create 'targetTickersDF' which will contain the records in 'tickersDF' which
# have a symbol in 'targetStocksDF'. 
targetTickersDF = tickersDF[tickersDF.index.isin(targetStocksDF['stock'])]
print ( targetTickersDF )

# Create an array doe filenames
fileNameListArray = []

# Now need to extract the data via the API. To do this we are going to extract
# the data for each of the targeted tickers.

limit = '&limit=10000'
access_key = 'access_key=e4e46efde92ca49b01d6df5955a48c6d'
URLbase = 'http://api.marketstack.com/v1/eod'


for index, specificTicker in targetTickersDF.iterrows():
    
    # Call to the marketstack API to get the list of tickers. The URL for the 
    # API is made up of the following pieces
    #
    #	Website:	http://api.marketstack.com/v1/
    #	Service:	eod (end of day)
    #	access_key:	Access key for accessing the API
    #   symbols:    The specific symbol (tickers) being downloaded
    #   exchange:   THe exchange where the ticker can be found
    #   date_from:  the start date of the request
    #   date_tp:    The end date of the request 
    #	limit:		The number of records. (set to 10000)
    
    # Create the URL using URLbase
    URLstart = URLbase + "?"+access_key
    URLstart = URLstart + '&symbols='+index
    URLstart = URLstart + '&exchange='+specificTicker.loc['acronym']
    URLstart = URLstart + limit
    URL = URLstart + '&date_from=2019-01-01'
    URL = URL + '&date_to=2022-12-31'

    # Make the API call. This returns a JSON object
    tickers_response_from_API = requests.get(URL)
    
    # turn the JSON object into a dictionary. The Json object has two 
    # significant parts 1) the Pagination which describes information on the 
    # response and the 2) the data which holds the data.
    tickersDataDICT = json.loads(tickers_response_from_API.text)
    #print ( tickersDataDICT.keys() )
    
    # create a dataframe using the data portion of the dictionary
    tickersDataDF = pd.DataFrame.from_dict( tickersDataDICT['data'] )
    
    # create a file with a name in the format <folder>+"tickers-"<symbol>".csv"
    filename = '../Data/stock-data-'+index+".csv"
    #print ( filename )
    tickersDataDF.to_csv(filename, encoding='utf-8')

    #maintain a list of files
    fileNameListArray.append (filename)

# output the list of files into a file called MasterFIleList.csv
print (fileNameListArray)
fileNameListDF = pd.DataFrame (fileNameListArray)
fileNameListDF.to_csv('../Data/MasterFileList.csv', encoding='utf-8', header=False )