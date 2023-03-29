""" --------------------------------------------------------------------------------------------------------

File:		Create report on All Stock Exchange data for LSE and the GDP for comparison
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-27
Descr		The purpose of this script is to report on the five stock exchange values
            from the London stock exchange and to show the adjusted UK GDP figures for 
            comparison. The adjustment of the GDP is deal with significant outliers.

""" 

# import the Python Libraries
import pandas as pd	              # library for pandas
import matplotlib.pyplot as plt   # library for plotting
import matplotlib.dates as mdates # library for dates 

# Read in the data from the WeeklyClosingDataMonday file
ClosingOnlyWeeksPCDF = pd.read_csv  ('../Data/weeklyClosingDataMonday.csv', parse_dates=(['Time']), index_col=['Time'] )
ClosingOnlyWeeksPCDF.info()
ClosingOnlyWeeksPCDF.head(20)

# setup a date format of year and week number
xfmt = mdates.DateFormatter('W%V')

# Create a dataframe containing the london data only
DFForPlotting = ClosingOnlyWeeksPCDF[LSE]
DFForPlotting.head(10)

# create a series of plots (7)
fig, ax = plt.subplots(7, 1, sharey=False)

# Iterate through the stocks symbols
for (index, columnName) in enumerate (DFForPlotting):

    ax[index].plot(DFForPlotting.index, DFForPlotting[columnName], color="blue", label="Stock Values")
    ax[index].plot(ClosingOnlyWeeksPCDF.index, ClosingOnlyWeeksPCDF['LSE'], color="red", label="Average Values", linestyle='--')

    # set the title of the subplot as the name of column which is the stock ticker symbol
    ax[index].set_title ( columnName )
    
    # set the Y axis title as "percentage change"
    ax[index].set_ylabel("Percentage Change")

    # set the date format for the xaxis and the rotation 
    ax[index].xaxis.set_major_formatter(xfmt)
    ax[index].xaxis.set_tick_params(rotation=45)
    
    # set the legend
    ax[index].legend()
    
# include the average graph as number 5 
ax[5].plot(ClosingOnlyWeeksPCDF.index, ClosingOnlyWeeksPCDF['LSE'], color="blue", label="GDP")
ax[5].set_title ('Average (LSE)')
ax[5].set_ylabel("Percentage Change")
ax[5].xaxis.set_major_formatter(xfmt)
ax[5].xaxis.set_tick_params(rotation=45)
ax[5].legend()

# Display all records which are outside the range of -100 to 100
print (ClosingOnlyWeeksPCDF[(ClosingOnlyWeeksPCDF['GBR_GDP'] < -100) | (ClosingOnlyWeeksPCDF['GBR_GDP'] > 100)]['GBR_GDP'].head(20))

# remove outliers which are outside the range of -300 to +300
DFForPlotting = ClosingOnlyWeeksPCDF[(ClosingOnlyWeeksPCDF['GBR_GDP'] > -300) & (ClosingOnlyWeeksPCDF['GBR_GDP'] < 300)]
weeks = pd.date_range (freq="W-MON", start=closingOnlyDF.index.min(), end=closingOnlyDF.index.max())
DFForPlotting = pd.DataFrame(DFForPlotting.reindex(weeks))
DFForPlotting = DFForPlotting.interpolate(method='linear')

# include the revised GDP graph as number 6 
ax[6].plot(DFForPlotting.index, DFForPlotting['GBR_GDP'], color="blue", label="GDP")
ax[6].set_title ('GDP')
ax[6].set_ylabel("Percentage Change")
ax[6].xaxis.set_major_formatter(xfmt)
ax[6].xaxis.set_tick_params(rotation=45)
ax[6].legend()
    
# set the title
fig.suptitle ("Graph of individual LSE weekly stock values ( based on 'monday' of week )")
    
# Specify that we use a tight layout and reduce the area slightly to have a better fit
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the figure
fig.savefig('../image/report5.png', facecolor='white')
plt.show()
