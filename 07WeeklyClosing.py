""" --------------------------------------------------------------------------------------------------------
File:		Create Weekly index
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-27
Descr		The purpose of this script is to take the existing daily data and 
            downsample to a weekly dataset by 1) using the monday value and 
            2) using an average value.
            
            Steps
            1) Load the daily data from the CSV file
            2) setup a week date range to cover the daily dates. Choose the dates
               based on the monday of the week
            3) Reindex the data using the monday date range.
            4) Calculate the percentage change between the current measure and the 
               previous measurement.
            5) Use the resample function to downsample to weekly data using the 
               average for the week
            6) Set the name of the index as "Time" for both data frames
            7) Calculate the percentage change between the current measure and the 
               previous measurement.
            8) Write both data frames as separate files called "weeklyClosingDataMonday.csv"
               and "weeklyClosingDataAverage.csv"

""" 

# import the Python Libraries
import pandas as pd	     # library for Pandas

# Read in the data from the closingData file
closingOnlyDF = pd.read_csv  ('../Data/closingDataGDP.csv', parse_dates=(['Time']), index_col=['Time'] )
closingOnlyDF.info()
closingOnlyDF.head(20)

# create a weekly date range for the time frame using Monday as the day in the week
weeks = pd.date_range (freq="W-MON", start=closingOnlyDF.index.min(), end=closingOnlyDF.index.max())

# Downsample the data from the daily data by reindexing using the weeklydates. 
ClosingOnlyWeeksMDF = pd.DataFrame(closingOnlyDF.reindex(weeks))
ClosingOnlyWeeksMDF.info()
ClosingOnlyWeeksMDF.head()

# determine the percentage change for each measurement compared to the following measurement (and multiply by 100)
# Note a NAN appears for the first value as there is no previous measurement.
ClosingOnlyWeeksMPCDF = ClosingOnlyWeeksMDF.pct_change().mul(100)
ClosingOnlyWeeksMPCDF.head()

# downsample the data from the daily data using the resample function and generate weekly data based on the mean
ClosingOnlyWeeksAvgDF = closingOnlyDF.resample("W").mean()
ClosingOnlyWeeksAvgDF.info()
ClosingOnlyWeeksAvgDF.head()

# determine the percentage change for each average measurement compared to the following measurement (and multiply by 100)
# Note a NAN appears for the first value as there is non previous measurement.
ClosingOnlyWeeksAvgPCDF = ClosingOnlyWeeksAvgDF.pct_change().mul(100)
ClosingOnlyWeeksAvgPCDF.head()

# Store the closing dataframe (based on Mondays) as a CSV (this is a break point)
ClosingOnlyWeeksMPCDF.index.name = 'Time'
ClosingOnlyWeeksMPCDF.info()
ClosingOnlyWeeksMPCDF.to_csv('../Data/weeklyClosingDataMonday.csv', encoding='utf-8')

# Store the closing dataframe (based on averages) as a CSV (this is a break point)
ClosingOnlyWeeksAvgPCDF.index.name = 'Time'
ClosingOnlyWeeksAvgPCDF.info()
ClosingOnlyWeeksAvgPCDF.to_csv('../Data/weeklyClosingDataAverage.csv', encoding='utf-8')