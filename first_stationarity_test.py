import numpy as np
import math
import os
#base class for time series
import watlevpy.time_series as wal 
#for plotting
import watlevpy.plot.plot as wplot
import matplotlib.pyplot as plt
#datetime default library
import datetime
#for stats testing
from scipy import stats
#for ARIMA and autocorrelations
import statsmodels.graphics.tsaplots as smgt
import statsmodels.tsa.arima_model as smta

#reading csv file
WL=wal.TSReader.from_csvfile(
    csvfile="./data_files/DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
wplot.plotTS(WL);

#years with at least 20 days every month

#y2000=wal.TS.sub_TS(WL,datetime.date(2000,1,1), datetime.date(2000,12,31));
#wplot.plotTS(y2000);

miss=wal.TSFilter.num_missing_dates(WL, datetime.date(1878,1,1), datetime.date(1878,1,31));

x=wal.TSFilter.years_from_TS(
    WL,
    years=range(WL.first_date.year,WL.last_date.year+1),
    checkid=2,
    miss_day_tol=27);
wplot.plotTS(x);

longest_run=wal.TSFilter.longest_continuous_run(x);