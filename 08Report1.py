""" --------------------------------------------------------------------------------------------------------

File:		Create report on All Stock Exchange data downsized using the monday value
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-27
Descr		The purpose of this script is to report on all nine stock exchange data sets
            to allow easy comparison. The Average stock exchange values for the data sets
            are also plotted

""" 

# import the Python Libraries
import pandas as pd	              # library for pandas
import matplotlib.pyplot as plt   # library for plotting
import matplotlib.dates as mdates # library for dates 

# Read in the data from the WeeklyClosingData file
ClosingOnlyWeeksPCDF = pd.read_csv  ('../Data/weeklyClosingDataMonday.csv', parse_dates=(['Time']), index_col=['Time'] )
ClosingOnlyWeeksPCDF.info()
ClosingOnlyWeeksPCDF.head(20)

# List of NYSE stock exchange symbols (note one symbol is missing )
NYSE = ['AA','CAT','FDX','WMT']

# List of LSD stock exchange symbols 
LSE = ['BATS.XLON','BP.XLON','DGE.XLON','HSBA.XLON','ULVR.XLON']

# setup a date format of year and week number
xfmt = mdates.DateFormatter('W%V')

# Set the canvas size so the plots can be seen
plt.rcParams['figure.figsize'] = [15, 15]

# create a series of nine plots (3x3) containing the normalised data for the stocks over the time period
fig, ax = plt.subplots(3, 3, sharey=True)

# Create a dataframe with the closing data from the two exchanges only
DFForPlotting = pd.merge (ClosingOnlyWeeksPCDF[NYSE], ClosingOnlyWeeksPCDF[LSE], left_index=True, right_index=True )
DFForPlotting.head(10)

# Iterate through the stocks symbols
for (index, columnName) in enumerate (DFForPlotting):

    row = 0
    col = 0
    if ( index <= 2 ):
        
        # row is 0 (first row) and col is the index
        row = 0
        col = index
    elif ( index <=5 ):
        # Row is 1 (second row). Col is reduced by 3 as this is the second row and index 3 -> 0, 
        # index 4 -> 1 and index 5 -> 2 etc.
        row = 1
        col = index - 3
    else:
        # Row is 2 (third row). Col is reduced by 6 as this is the second row and index 6 -> 0, 
        # index 7 -> 1 and index 8 -> 2 etc.
        row = 2
        col = index -6

    # determine the average column, use NYSE for new york stocks and LSE for london stocks
    avgColumn = ''
    if ( columnName in NYSE ): avgColumn = 'NYSE'
    if ( columnName in LSE ):  avgColumn = 'LSE'
        
    # plot the weekly data column in to the row and column of the axis
    ax[row,col].plot(DFForPlotting.index, DFForPlotting[columnName], color="blue", label ='Stock Values')
    
    # If we have an average column
    if ( avgColumn != '' ): ax[row,col].plot(ClosingOnlyWeeksPCDF.index, ClosingOnlyWeeksPCDF[avgColumn], color="green", linestyle='--' , label ='Average Values')
    
    # set the title of the subplot as the name of column which is the stock ticker symbol
    ax[row,col].set_title ( columnName )
    
    # set the Y axis title as "percentage change"
    ax[row,col].set_ylabel("Percentage Change")

    # set the date format for the xaxis and the rotation 
    ax[row,col].xaxis.set_major_formatter(xfmt)
    ax[row,col].xaxis.set_tick_params(rotation=45)
    
    # set the legend
    ax[row,col].legend()

# set the title of the overall plot
fig.suptitle ("Graph of all weekly stock values - Percentage Change ( based on Monday value )")

# Specify that we use a tight layout and reduce the area slightly to have a better fit
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the figure
fig.savefig('../image/report1.png', facecolor='white')
plt.show()