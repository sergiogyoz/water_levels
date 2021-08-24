import numpy as np
import watlevpy.time_series as wal #base class for time series
#for plotting
import watlevpy.plot.year_evol as yevol
import watlevpy.plot.simple as wplot
#datetime default library
import datetime
#for stats testing
from scipy import stats 

#WL=wal.TSReader.from_csvfile(csvfile="./DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
#foryearplot=wal.TS.sub_wl(WL, datetime.date(WL.first_date.year+1,1,1), datetime.date(WL.last_date.year-1,12,31));

#yaver=wal.TSFilter.averages_from_TS(WL, "yearly");
#wplot.plot(yaver,gtype=2);

#ypeaks=wal.TSFilter.peaks_from_TS(WL, "monthly");
#wplot.plot(ypeaks,gtype=1);

#donttrashme=yevol.animate(foryearplot);
#yevol.months(WL,smooth=2);

#decade=wal.TSFilter.years_from_TS(WL, range(2000,2010+1));

#Februaries=wal.TSFilter.month_from_years_from_TS(WL, month=2);

#wplot.plot(decade);

#-----Let's do some testing

#Kendall testing
kdata=wal.TSReader.from_csvfile(csvfile="./KendalldataNotrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    
#kdata=wal.TSReader.from_csvfile(csvfile="./KendalldataTrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    

t=list(range(kdata.n));
tau, p_val= stats.kendalltau(t, kdata.wl);

n=kdata.n;
s=0;
for i in range(0,n-1):
    for j in range(i+1,n):
        s=s+np.sign(kdata.wl[j]-kdata.wl[i]);

tp=[0]*20;
for val in kdata.wl:
    tp[int(val)]=tp[int(val)]+1;
    
var=n*(n-1)*(2*n+5);
for t in tp:
    var=var-t*(t-1)*(2*t+5);
var=var/18;

#Z= (s-1)/np.sqrt(var) if s>0 else (s+1)/np.sqrt(var);
Z=s/np.sqrt(var);

myp_val=2*stats.norm.cdf(Z);

















