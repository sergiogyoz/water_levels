import numpy as np
import math
import watlevpy.time_series as wal #base class for time series
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

datapath="./data_files/";

WL=wal.TSReader.from_csvfile(csvfile="./data_files/DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
#foryearplot=wal.TS.sub_TS(WL, datetime.date(WL.first_date.year+1,1,1), datetime.date(WL.last_date.year-1,12,31));
#foryearplot=wal.TS.sub_TS(WL, datetime.date(1950,1,1), datetime.date(WL.last_date.year-1,12,31));
#USGS_TS=wal.TSReader.from_USGS("./data_files/dv",dateformat="%Y-/%m-/%d", units="ft");

somedata=wal.TS.sub_TS(WL, datetime.date(1950,1,1) , datetime.date(1970,1,1));
wplot.plotTS(somedata);
maximum=wal.TS.scalarFuction(somedata,stats.describe);
logsomedata=wal.TS.applyFunction(somedata,math.log10);
wplot.plotTS(logsomedata);

#yaver=wal.TSFilter.averages_from_TS(foryearplot, "monthly");
#ypeaks=wal.TSFilter.POT_from_TS(WL, 604);
#wal.TS.save_to_csv(yaver,"myyeardata");

#fig1,axs1,fig2,axs2 =wplot.plotTS(yaver,gtype=2,dataname="water levels");


#ypeaks=wal.TSFilter.peaks_from_TS(WL, "monthly");
#wplot.plotTS(ypeaks,gtype=1);

#donttrashme=wplot.YearEvol.animate(foryearplot);

Januaries=wal.TSFilter.month_of_years_from_TS(WL,1,range(1900,1930));
#averages=[];
#maxs=[];
#for year in Januaries:
#    averages.append( 
#        wal.TSFilter.averages_from_TS(Januaries[year], "monthly"));
#    averages.append(
#        wal.TSFilter.peaks_from_TS(Januaries[year], "monthly"));
    
#wplot.YearEvol.months(WL,1960,2020,[1,2,11,12]);


"""

#-----Let's do some testing

def autocorr(x, maxlag=10):
    aut=[];
    m=len(x)-maxlag;
    for t in range(maxlag+1):
        aut.append(np.corrcoef(x[0:m], x[t:m+t])[0][1]);
    return aut;


plt.figure();
rho=autocorr(yaver.wl,maxlag=30);
plt.plot(rho);

smgt.plot_acf(yaver.wl,lags=30);
smgt.plot_pacf(yaver.wl,lags=30);

arimastuff=smta.ARIMA(yaver.wl, order=(1,0,0));
arimafit=arimastuff.fit(disp=0)
print(arimafit.summary())



arimafit.plot_predict(dynamic=False);
plt.show();

"""







