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
#wplot.plotTS(WL);

#going crazy about a function
smallWL=wal.TS.sub_TS(WL, datetime.date(1931,1,1), datetime.date(1935,12,21));
"""y=wal.TSFilter.years_from_TS(
    smallWL,
    years=range(smallWL.first_date.year,smallWL.last_date.year+1),
    checkid=2,
    miss_day_tol=1);
ylonrun=wal.TSFilter.longest_continuous_run(y);
"""
#years with at least 20 days every month

x=wal.TSFilter.years_from_TS(
    WL,
    years=range(WL.first_date.year,WL.last_date.year+1),
    checkid=2,
    miss_day_tol=20);

xaver=wal.TSFilter.averages_from_TS(x, "yearly");
wplot.plotTS(xaver);

longest_run,cruns=wal.TSFilter.longest_continuous_run(xaver,True);