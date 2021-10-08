import numpy as np
import watlevpy.time_series as wal #base class for time series
from scipy import stats #for stats testing

#--------------Kendall testing
kdata=wal.TSReader.from_csvfile(csvfile="./KendalldataNotrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    
#kdata=wal.TSReader.from_csvfile(csvfile="./KendalldataTrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    
#kdata=wal.TSReader.from_csvfile(csvfile="./myyeardata.csv",headers=True,dateformat="%Y-%m-%d");    

t=list(range(kdata.n));
tau, kp_val= stats.kendalltau(t, kdata.wl);
try:
    n=kdata.n;
    s=0;
    for i in range(0,n-1):
        for j in range(i+1,n):
            s=s+np.sign(kdata.wl[j]-kdata.wl[i]);
    
    tp=[0]*20;
    for val in kdata.wl:
        tp[int(val)]=tp[int(val)]+1;
        
    kvar=n*(n-1)*(2*n+5);
    for t in tp:
        kvar=kvar-t*(t-1)*(2*t+5);
    kvar=kvar/18;
    
    #Z= (s-1)/np.sqrt(kvar) if s>0 else (s+1)/np.sqrt(kvar);
    Z=s/np.sqrt(kvar);
    
    mykp_val=2*(1-stats.norm.cdf(Z));
except:
    pass;
#--------------------

