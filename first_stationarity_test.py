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
Ts1=[];
c1=[];
p1=[];
Ts2=[];
c2=[];
p2=[];
Ts3=[];
c3=[];
p3=[];
Ts4=[];
c4=[];
p4=[];
filenames=[];
N=[];
for file_ in os.listdir(datapath):
    if file_.endswith(".csv"):
        #reading csv file
        WL=wal.TSReader.from_csvfile(
            csvfile=datapath+file_,headers=True,dateformat="%m/%d/%Y %H:%M");
        filenames.append(file_);
        #years with at least a few days every month
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
        #augmented Dickie Fuller test
        adf=smttools.adfuller(final,regression="c");
        Ts1.append(adf[0]);
        c1.append(adf[4]);
        p1.append(adf[1]);
        adf=smttools.adfuller(final,regression="ct");
        Ts2.append(adf[0]);
        c2.append(adf[4]);
        p2.append(adf[1]);
        kpss=smttools.kpss(final,regression="c", nlags="auto");
<<<<<<< Updated upstream
        Ts3.append(kpss[0]);
        c3.append(kpss[3]);
        p3.append(kpss[1]);
        kpss=smttools.kpss(final,regression="ct", nlags="auto");
        Ts4.append(kpss[0]);
        c4.append(kpss[3]);
        p4.append(kpss[1]);
=======
        p2.append(kpss[1]);
        kpsst=smttools.kpss(final,regression="ct", nlags="auto");
        p3.append(kpsst[1]);

bplotdata=[p1,p2,p3]
fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)
 
# Creating axes instance
bp = ax.boxplot(bplotdata, patch_artist = True, sym="b+",
                notch =False, vert = 0)
 
colors = ['#ef9a9a', '#9fa8da', '#fff59d']
 
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
 
# changing color and linewidth of
# whiskers
for whisker in bp['whiskers']:
    whisker.set(color ='#bcbcbc',
                linewidth = 1,
                linestyle =":")
 
# changing color and linewidth of
# caps
for cap in bp['caps']:
    cap.set(color ='#f57f17',
            linewidth = 2)
 
# changing color and linewidth of
# medians
for median in bp['medians']:
    median.set(color ='#616161',
               linewidth = 2, linestyle=":")
 
# changing style of fliers
for flier in bp['fliers']:
    flier.set(marker ='D',
              color ='#e7298a',
              alpha = 0.5)
     
# x-axis labels
ax.set_yticklabels(['ADFuller', 'KPSS c',
                    'KPSS ct'])
 
# Adding title
plt.title("P values of stationarity test");
 
# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
     
# show plot
plt.show()
>>>>>>> Stashed changes
