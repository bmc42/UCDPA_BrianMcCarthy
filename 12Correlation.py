""" --------------------------------------------------------------------------------------------------------

File:		Determine correlation between NYSE and LSE and equivalent GDP
Author:		Brian McCarthy (brian.mccarthy@hpo.ie)
Create:		2023-03-27
Descr		The purpose of this script is to determine the correlation
			between the different columns for NYSE and LSE

""" 

# import the Python Libraries
import pandas as pd	              # library for pandas

# Read in the data from the closingData file
closingOnlyDF = pd.read_csv  ('../Data/closingDataGDP.csv', parse_dates=(['Time']), index_col=['Time'] )

# List of NYSE stock exchange symbols (note one symbol is missing )
NYSE = ['AA','CAT','FDX','WMT']

NYSE.append('NYSE')
NYSE.append('USA_GDP')
closingOnlyDF[NYSE].corr()

# List of LSE stock exchange symbols 
LSE = ['BATS.XLON','BP.XLON','DGE.XLON','HSBA.XLON','ULVR.XLON']

LSE.append('LSE')
LSE.append('GBR_GDP')
closingOnlyDF[LSE].corr()
