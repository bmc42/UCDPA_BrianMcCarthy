""" --------------------------------------------------------------------------------------------------------

File:		Create report on All Stock Exchange data for NYSE and the GDP for comparison
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-27
Descr		The purpose of this script is to report on the four stock exchange values
            from the new york stock exchange and to show the USA GDP figures for comparison

""" 

# import the Python Libraries
import pandas as pd	              # library for pandas
import matplotlib.pyplot as plt   # library for plotting
import matplotlib.dates as mdates # library for dates 

# Read in the data from the WeeklyClosingData file
ClosingOnlyWeeksPCDF = pd.read_csv  ('../Data/weeklyClosingDataMonday.csv', parse_dates=(['Time']), index_col=['Time'] )
ClosingOnlyWeeksPCDF.info()
ClosingOnlyWeeksPCDF.head(20)

# setup a date format of year and week number
xfmt = mdates.DateFormatter('W%V')

# Create a dataframe containing the new york data only
DFForPlotting = ClosingOnlyWeeksPCDF[NYSE]
DFForPlotting.head(10)

# create a series of plots (5) 
fig, ax = plt.subplots(6, 1, sharey=False)

# Iterate through the stocks symbols
for (index, columnName) in enumerate (DFForPlotting):

    ax[index].plot(DFForPlotting.index, DFForPlotting[columnName], color="blue", label="Stock Values")
    ax[index].plot(ClosingOnlyWeeksPCDF.index, ClosingOnlyWeeksPCDF['NYSE'], color="red", label="Average Values", linestyle='--')

    # set the title of the subplot as the name of column which is the stock ticker symbol
    ax[index].set_title ( columnName )
    
    # set the Y axis title as "percentage change"
    ax[index].set_ylabel("Percentage Change")

    # set the date format for the xaxis and the rotation 
    ax[index].xaxis.set_major_formatter(xfmt)
    ax[index].xaxis.set_tick_params(rotation=45)
    
    # set the legend
    ax[index].legend()

# include the average graph as number 4 
ax[4].plot(ClosingOnlyWeeksPCDF.index, ClosingOnlyWeeksPCDF['NYSE'], color="blue", label="GDP")
ax[4].set_title ('Average (NYSE)')
ax[4].set_ylabel("Percentage Change")
ax[4].xaxis.set_major_formatter(xfmt)
ax[4].xaxis.set_tick_params(rotation=45)
ax[4].legend()

# include the GDP graph as number 5
ax[5].plot(ClosingOnlyWeeksPCDF.index, ClosingOnlyWeeksPCDF['USA_GDP'], color="blue", label="GDP")
ax[5].set_title ('GDP')
ax[5].set_ylabel("Percentage Change")
ax[5].xaxis.set_major_formatter(xfmt)
ax[5].xaxis.set_tick_params(rotation=45)
ax[5].legend()
   
    
# set the title
fig.suptitle ("Graph of individual NYSE weekly stock values ( based on 'monday' of week )")
    
# Specify that we use a tight layout and reduce the area slightly to have a better fit
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the figure
fig.savefig('../image/report3.png', facecolor='white')
plt.show()
