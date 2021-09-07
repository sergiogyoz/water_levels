import numpy as np
import watlevpy.time_series as wal #base class for time series
#for plotting
import watlevpy.plot.year_evol as yevol
import watlevpy.plot.simple as wplot
import matplotlib.pyplot as plt
#datetime default library
import datetime
#for stats testing
from scipy import stats
#for ARIMA and autocorrelations
import statsmodels.graphics.tsaplots as smgt
import statsmodels.tsa.arima_model as smta

WL=wal.TSReader.from_csvfile(csvfile="./DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
#foryearplot=wal.TS.sub_TS(WL, datetime.date(WL.first_date.year+1,1,1), datetime.date(WL.last_date.year-1,12,31));
foryearplot=wal.TS.sub_TS(WL, datetime.date(1950,1,1), datetime.date(WL.last_date.year-1,12,31));

yaver=wal.TSFilter.averages_from_TS(foryearplot, "monthly");
ypeaks=wal.TSFilter.POT_from_TS(WL, 604);
#wal.TS.save_to_csv(yaver,"myyeardata");



fig1,axs1,fig2,axs2 =wplot.plot(yaver,gtype=2,dataname="water levels");

#ypeaks=wal.TSFilter.peaks_from_TS(WL, "monthly");
#wplot.plot(ypeaks,gtype=1);

#donttrashme=yevol.animate(foryearplot);
#yevol.months(WL,smooth=2);

#decade=wal.TSFilter.years_from_TS(WL, range(2000,2010+1));

#Februaries=wal.TSFilter.month_from_years_from_TS(WL, month=2);

#wplot.plot(decade);


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







