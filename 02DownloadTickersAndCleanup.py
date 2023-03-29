""" --------------------------------------------------------------------------------------------------------
File:		extract and store tickers
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-12
Descr		The purpose of this script is extract the list of tickers,. The 
            script will manipulate the tickers by
            
            1) Removing all tickers for which there are no intra-Day data
               and only EOD data
            2) Extract the Stock Exchange symbol from the 'stock_exchange' 
               column and add it as a new column called 'acronym'
            3) Update the blanks in the 'acronym' column which are present due
               to "over the counter" transactions.
            4) Extract the 'country' column from the 'stock_exchange' column  
               and update the existing 'country' column
            5) Extract the 'country_code' column from the 'stock_exchange'
               column and add to a new column called 'country_code'
            6) Extract the 'city' column from the 'stock_exchange' column and 
               add to a new column called 'city'
            7) Drop the column 'stock_exchange' 
               
            Finally, the data frame will be stored as 'tickers.csv'

"""

# import the Python Libraries
import requests          # library for the HTTP connection for the API call
import pandas as pd	     # library for Pandas
import json		         # library for the JSON string processing. 


# Call to the marketstack API to get the list of tickers. The URL for the API 
# is made up of the following pieces
#	Website:	http://api.marketstack.com/v1/
#	Service:	tickers
#	access_key:	Access key for accessing the API
#	limit:		The number of records. The value was set to 204799 but the API 
#               only return 10000 records.	

URLbase = 'http://api.marketstack.com/v1/tickers'
access_key = 'access_key=e4e46efde92ca49b01d6df5955a48c6d'
limit = '&limit=204799'

# create the URL for the API
URL = URLbase+"?"+access_key+limit

# Make the API call. This returns a JSON object
tickersResponseFromAPI = requests.get('http://api.marketstack.com/v1/tickers?access_key=e4e46efde92ca49b01d6df5955a48c6d&limit=204799')
#print (response_API.text)

# Process the JSON output text from the API and convert to a Dictionary. There 
# are two main parts in the JSON structure: Pagination (overall detail of 
# response) and Data.
tickersDICT = json.loads(tickersResponseFromAPI.text)
print ( tickersDICT.keys() )

# Convert the dictionary into a dataframe and examine the data.
tickersDF = pd.DataFrame.from_dict( tickersDICT['data'] )
tickersDF.info()
tickersDF.shape
tickersDF.head()

# Output the data to a CSV file called 'tickers.csv' in the Data folder
#dataDF.to_csv('../Data/tickers.csv', encoding='utf-8')

# The data has two fields which characterise the type of stock data available.
#   has_intraDay    indicates (when true) the if stock data information is recorded 
#                   during the day
#   has_eod         indicates (when true) the if stock data information is recorded 
#                   at the end of the day
#
# Foe the analysis, we will concentrate only on the has_eod==true and the 
# has_intraday == false
   
print ("Examing 'has_intraday'")
print ('Has_intraday==false shape is : '+str(tickersDF[tickersDF['has_intraday'] == False].shape))
print ('Has_intraday==true shape is : '+str(tickersDF[tickersDF['has_intraday'] == True].shape))

print ("Examing 'has_eod'")
print ('Has_eod==false shape is : '+str(tickersDF[tickersDF['has_eod'] == False].shape))
print ('Has_eod==false shape is : '+str(tickersDF[tickersDF['has_eod'] == True].shape))

# include the records noted above
tickersDF = tickersDF[(tickersDF['has_intraday'] == False) & (tickersDF['has_eod'] == True)]

# Create a field called 'acronym' and set the value to the 'acronym' in the 
# data dictionary in 'stock_exchange'
tickersDF['acronym'] = [ d.get('acronym') for d in tickersDF['stock_exchange']]

# fix the blanks in 'acronym' where the OTC (over the counter) values are left
# blank.
tickersDF.loc[tickersDF['acronym']=='','acronym'] = 'OTC'

# Update the field called 'country' and set the value to the 'country' in the 
# data dictionary in 'stock_exchange'
tickersDF['country'] = [ d.get('country') for d in tickersDF['stock_exchange']]

# Create a field called 'country_code' and set the value to the 'countryCode' in the 
# data dictionary in 'stock_exchange'
tickersDF['country_code'] = [ d.get('country_code') for d in tickersDF['stock_exchange']]

# Create a field called 'city' and set the value to the 'countryCode' in the 
# data dictionary in 'stock_exchange'
tickersDF['city'] = [ d.get('city') for d in tickersDF['stock_exchange']]

print ( tickersDF.head() )

# drop the 'stock_exchange' columns
tickersDF = tickersDF.drop('stock_exchange', axis=1)

print (tickersDF.info())
print (tickersDF.head())

# Write the dataframe to the tickers2.csv
tickersDF.to_csv( '../Data/Tickers.csv', encoding='utf-8' )