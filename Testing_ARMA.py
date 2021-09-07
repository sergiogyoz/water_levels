import numpy as np
import watlevpy.time_series as wal #base class for time series
from scipy import stats #for stats testing

#--------------Kendall testing
kdata=wal.TSReader.from_csvfile(csvfile="./KendalldataNotrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    
#kdata=wal.TSReader.from_csvfile(csvfile="./KendalldataTrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    
#kdata=wal.TSReader.from_csvfile(csvfile="./myyeardata.csv",headers=True,dateformat="%Y-%m-%d");    


#--------------------

