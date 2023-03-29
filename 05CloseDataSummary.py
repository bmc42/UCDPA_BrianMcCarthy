""" --------------------------------------------------------------------------------------------------------
File:		Summarise CLosing Data
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-27
Descr		The purpose of this script is to load the combined master dataset, slice the
            data to only include the (non-adjusted) closing price, determine the averages
            for each exchange, make sure there are no missing data (and correct if there
            are) and store the data
            
            Steps
            1) setup some arrays for the NYSE and LSE stocks
            2) Read in the overall data file and examine. The overall data is loaded with
               two index columns.
            3) Slice the data and keep the Close column containing the non-adjusted cloing
               prices. Store the data in a dataframe.
            4) Unstack the dataframe so that the dates are the remaining index and there are
               columns for each stock type.
            5) Update the index and change it to the date of the index value. This changes
               the value from a format of "yyyy-MM-dd hh:mm:ss" to "yyyy-MM-dd". This change 
               is needed to allow merging with other datasets.
            6) Reindex the data frame across all the days from the starting date to the 
               ending date. This ensures we have records for missing values for weekends
               and holidays.
            7) Interpolate the columns to fill in the missing values.
            8) Create a new column for the mean of the New York stock exchange data and 
               calculate this value. 
            9) Create a new column for the mean of the London stock exchange data and 
               calculate this value. 
            10)Calculate the first quartile (0.25) on the data for both stock exchanges
            11)Calculate the third quartile (0.75) on the data for both stock exchanges
            12)Give the index a name and store the data in a file called 
               "closeingData.csv"

""" 

# import the Python Libraries
import pandas as pd	              # library for pandas

# List of NYSE stock exchange symbols (note one symbol is missing )
NYSE = ['AA','CAT','FDX','WMT']

# List of LSD stock exchange symbols 
LSE = ['BATS.XLON','BP.XLON','DGE.XLON','HSBA.XLON','ULVR.XLON']

# Read the data in from the CSV file and check the input
masterDF = pd.read_csv ('../Data/masterData.csv', parse_dates=(['date']), index_col=['date','symbol'])
masterDF.info()
masterDF.head()
masterDF.isna().any()

# examine the main data variables 
masterDF[['open','close','high', 'low']].head(20)

#concentrate on the closing prices for each day
closingOnlyDF = masterDF['close']

# reshape the data using unstack. this creates individual closing value columns for each symbol
closingOnlyDF = closingOnlyDF.unstack()
closingOnlyDF.info()

#make sure we do not have a time zone issue
closingOnlyDF.index = closingOnlyDF.index.date
closingOnlyDF.head()

# Cleanup the data and deal with the missing entries (NAN) by interpolating the data. the missing entries 
# relate to when the stock exchange is closed
closingOnlyDF = closingOnlyDF.reindex(pd.date_range(start=closingOnlyDF.index.min(), end=closingOnlyDF.index.max(),freq='1D'))
closingOnlyDF.sort_index(ascending=False).head(10)

# Use the pandas interpolation function to estimate the missing values. Use the "linear" method as it is not expected
# there would be much fluctuations in data over weekends and holidays,
closingOnlyDF = closingOnlyDF.interpolate(method='linear')
closingOnlyDF.info()
closingOnlyDF.head(10)

# create a new column for the NYSE and LSE containing the average value
# of the chosen stocks from those exchanges
closingOnlyDF['NYSE'] = closingOnlyDF[NYSE].mean(axis=1)
closingOnlyDF['LSE'] = closingOnlyDF[LSE].mean(axis=1)
closingOnlyDF.head()

# Add a column for the first quartile for the NYSE and LSE
closingOnlyDF['NYSEQ1'] = closingOnlyDF[NYSE].quantile(0.25, axis=1)
closingOnlyDF['LSEQ1'] = closingOnlyDF[LSE].quantile(0.25, axis=1)

# Add a column for the third quartile for the NYSE and LSE
closingOnlyDF['NYSEQ3'] = closingOnlyDF[NYSE].quantile(0.75, axis=1)
closingOnlyDF['LSEQ3'] = closingOnlyDF[LSE].quantile(0.75, axis=1)

closingOnlyDF.info()
closingOnlyDF.head()

# Store the closing dataframe as a CSV (this is a break point)
closingOnlyDF.index.name = 'Time'
closingOnlyDF.info()
closingOnlyDF.to_csv('../Data/closingData.csv', encoding='utf-8')

