import numpy as np
import math
import os
import csv
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
#c's are critical values, p's are p-values, T are the test statistic
T=[[],[],[],[]];
c=[[],[],[],[]];
p=[[],[],[],[]];
p_MK=[];
filenames=[];
N=[];

for file_ in os.listdir(datapath):
    if file_.endswith(".csv"):
        #reading csv file
        WL=wal.TSReader.from_csvfile(
            csvfile=datapath+file_,headers=True,dateformat="%m/%d/%Y %H:%M");
        #years with at least a few days every month
        goodyears=wal.TSFilter.years_from_TS(
            WL,
            years=range(1941,WL.last_date.year+1),
            checkid=2,
            miss_day_tol=25);
        #averages of those years
        yaver=wal.TSFilter.averages_from_TS(goodyears, "yearly");
        if not wal.TS.isEmpty(yaver) and yaver.n>30: #only data with over 30 years
            filenames.append(file_[0:len(file_)-4]);
            #plot
            wplot.plotTS(yaver,gtype=3,dataname=file_[0:len(file_)-4]); 
            #extract longest continuous run
            lrun,cruns=wal.TSFilter.longest_continuous_run(yaver,True);
            final=yaver.get_time_window(lrun[0],lrun[1]);
            N.append(len(final));

            #Mann-Kendall test
            t=list(range(len(final)));
            tau, p_tau= stats.kendalltau(t, final,variant="c");
            p_MK.append(p_tau);
            
            reg=["c","ct"];
            #augmented Dickie Fuller test
            for i in range(1+1):
                adf=smttools.adfuller(final,regression=reg[i%2]);
                T[i].append(adf[0]);
                c[i].append(adf[4]);
                p[i].append(adf[1]);
            #kpss test   
            for i in range(2,3+1):
                kpss=smttools.kpss(final,regression=reg[i%2],nlags="auto");
                T[i].append(kpss[0]);
                c[i].append(kpss[3]);
                p[i].append(kpss[1]);        
            

#write csv file for table of p values at each location
with open('p_values_at_locations.csv',newline='',mode='w') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(["name","N","MK","ADFuller c","KPSS c","ADFuller ct","KPSS ct", "trend", "stationarity supported by"]);
    for i in range(len(N)):
        trend="c";
        if p_MK[i]<0.05: #if we reject trend is not constant
            trend="ct"; #we assume linear for further testing
        
        support=0;
        ind=0; # 0 and 2 constant
        if trend=="ct":
            ind=1; #1 and 3 linear
        reject_unit_root=(p[ind][i]<=0.05);
        stationarity=(p[ind+2][i]>=0.05);
        support=int(reject_unit_root)+int(stationarity);
        
        
        row=[filenames[i],N[i],p_MK[i],p[0][i],p[2][i],p[1][i],p[3][i],trend,support];
        writer.writerow(row);
        

#Transforming the test values for better representation
nT=[[],[],[],[]];
c1percent=[];
def linear5to10(TestStat,n,i):
    """linear transformation using 5% and 10% as the fix points"""
    x=((TestStat-c[n][i]["5%"]) / (c[n][i]["10%"]-c[n][i]["5%"]));
    return x;
for n in range(4):
    for i in range(len(T[n])):
        x=linear5to10(T[n][i], n, i);
        c1percent.append( linear5to10(c[n][i]["1%"], n, i) );
        nT[n].append(x);

def myboxplot(bplotdata,xticks,xtickslabels,vertline,xlimits=[],title=""):
    """my custom boxplot function for p values or transformed T statistics"""
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
     
    # Creating axes instance
    bp = ax.boxplot(bplotdata, patch_artist = True, sym="b+",
                    notch =False, vert = 0)
     
    colors = ['#ef9a9a50', '#9fa8da50', '#fff59d50',"#81c78450"]
     
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color);
        patch.set_linestyle("None");
         
    # changing color and linewidth of
    # whiskers
    for whisker in bp['whiskers']:
        whisker.set(color ='#bcbcbc',
                    linewidth = 1,
                    linestyle =":");
     
    # changing color and linewidth of
    # caps
    for cap in bp['caps']:
        cap.set(color ='#f57f17',
                linewidth = 2);
     
    # changing color and linewidth of
    # medians
    for median in bp['medians']:
        median.set(color ='#616161',
                   linewidth = 2, linestyle=":");
     
    # changing style of fliers (outliers)
    for flier in bp['fliers']:
        flier.set(marker ='',
                  color ='#e7298a',
                  alpha = 0.5);
        
    # x,y-axis labels
    ax.set_xticks(xticks);
    ax.set_xticklabels(xtickslabels);
    ax.set_yticklabels(['ADFuller c','ADFuller ct', 
                        'KPSS c','KPSS ct']);
    
    #adding the points to make it more friendly
    yticks=ax.get_yticks(); 
    for i in range(len(nT)):
        x = bplotdata[i];
        y = np.random.normal(yticks[i], 0.06, size=len(x));
        plt.plot(x, y, 'bo', alpha=0.5);
    
    #adding vertical lines for critical values
    for val in vertline:
        plt.axvline(x=val);
    # Adding title
    plt.title(title);
     
    # Removing top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    #x axis display limits
    if xlimits:
        ax.set_xlim(xlimits);
    # show plot
    plt.show()
    return fig, ax;

fig1,ax1=myboxplot(nT,
          [sum(c1percent)/len(c1percent),0.0,1.0],
          ["~1%" ,"5%","10%"],
          [0,1,sum(c1percent)/len(c1percent)],
          [],
          "Transformed test statistic values at "+str(len(nT[0]))+" locations");

ax1.set_xlabel("p-values");
ax1.set_ylabel("different tests");

"""myboxplot(p,
          [0,0.01,0.05,0.1],
          ["0%","1%","5%","10%"],
          [],
          [-0.015,0.115],
          "p values");"""



