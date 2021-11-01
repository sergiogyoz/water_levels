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
import statsmodels.tsa.stattools as smttools


datapath="./data_files/Mississippi_River/";
#c's are critical values, p's are p-values
filenames=[];
N=[];
M=[];
for file_ in os.listdir(datapath):
    if file_.endswith(".csv"):
        #reading csv file
        WL=wal.TSReader.from_csvfile(
            csvfile=datapath+file_,headers=True,dateformat="%m/%d/%Y %H:%M");
        #years with at least a few days every month
        fullyaver=wal.TSFilter.averages_from_TS(WL, "yearly");
        if fullyaver.n<50:
            pass;
        else:
            M.append(fullyaver.n);
            filenames.append(file_);
            
            wplot.plotTS(fullyaver,gtype=3,dataname=file_[0:len(file_)-5]);
            
            goodyears=wal.TSFilter.years_from_TS(
                WL,
                years=range(WL.first_date.year,WL.last_date.year+1),
                checkid=2,
                miss_day_tol=25);
            #averages of those years
            yaver=wal.TSFilter.averages_from_TS(goodyears, "yearly");
            #wplot.plotTS(yaver,gtype=2);
            #extract longest continuous run
            lrun,cruns=wal.TSFilter.longest_continuous_run(yaver,True);
            final=yaver.get_time_window(lrun[0],lrun[1]);
            N.append(len(final));
    
    
    
