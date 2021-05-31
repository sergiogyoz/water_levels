import csv
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

import statsmodels as sm
        
class WaterLevels:
    """
    Water level data type for daily measurements and statistical analisys
    
    Attributes
    ----------
    wl : float array
        the daily measurements of the water level
    dates : datetime array
        dates as datetime objects corresponding to the day of the wl measurements
    
    """
    
    def __init__(self,
                 waterlevels=[],
                 datesarray=[],
                 ):
        """
        Use for raw python data, if reading from a file use any of the from_(filetype) constructors
        
        Parameters
        ----------
        waterlevels: float array
            the daily measurements of the water level
        datesarray: datetime array
            dates as datetime objects corresponding to the day of the wl measurements 
        """
        
        self.first_date=datesarray[0];
        self.last_date=datesarray[-1];
        n=len(waterlevels);
        m=len(datesarray);
        if n!=m :
            raise Exception(f"water levels and dates array are not the same size. Sizes are: {n} and {m}")
        self.n=n;
        self.wl=waterlevels;
        self.dates=datesarray;
        self.date_index=dict(zip(datesarray,range(n)));
    
    def getdate(self,i):
        return self.dates[i];
    def setdate(self,i,date):
        self.dates[i]=date;
    def getwl(self,i):
        return self.wl[i];
    def setwl(self, i, value):
        self.wl[i]=value;

    @classmethod
    def from_csvfile(cls,csvfile,headers=True,dateformat="%m/%d/%Y"):
        """
        Creates instance of WaterLevels class from two column csv file
        
        The first column of the csv are the dates and the second one the water levels.
        
        Parameters
        ----------
        csvfile: str
            relative path to the csv file. 
            e.g. "relative/path/user/data.csv"
        headers: bool
            (defaults to True) True if file has headers which are then removed, if only raw data then false.
        dateformat: str
            format of the dates on the data following the format codes for datetime.datetime.strftime. 
            e.g. "%m/%d/%Y %H:%M"
        """
        
        with open(csvfile,newline='') as csvdata:
            mydata=list(csv.reader(csvdata))
            if headers:
                mydata.pop(0);
            m=len(mydata);
            wl=[0]*m;
            dates=[0]*m;
            missingdates=[];
            n=0;
            for i in range(0,m):
                try:
                    wl[n]=float(mydata[i][1]);
                except ValueError:
                    pass;
                except:
                    print("Unexpected error while reading water values");
                    raise;
                else:
                    n=n+1;
                try:
                    x=datetime.datetime.strptime(mydata[i][0],dateformat).date();
                except ValueError:
                    print( f"format on date entry {str(i)} is wrong: {str(mydata[i][0])}" );
                else:
                    dates[n-1]=x;
            if(m-n>0):
                print(f"There are {m-n} wrong format water levels (possibly missing dates)")
            dates=dates[:n];
            wl=wl[:n];
            return WaterLevels(waterlevels=wl,datesarray=dates);

    def dindex(self,date, roundup=False,rounddown=False):
        """
        Index of a given date. If date doesn't exist it throws a key error
        """
        newdate=None;
        if roundup and rounddown:
            raise Exception("Don't mess with me");
        try:
            x=self.date_index[date];
            return x;
        except KeyError:
            print(f"date {date} is missing");
            #brute force solution to rounding up or down
        if roundup and self.last_date>=date:
            delta=datetime.timedelta(days=1);
            newdate=date+delta;
            while newdate not in self.date_index:
                newdate=newdate+delta;
            return self.date_index[newdate];
        if rounddown and self.first_date<=date:
            delta=datetime.timedelta(days=-1);
            newdate=date+delta;
            while newdate not in self.date_index:
                newdate=newdate+delta;
            return self.date_index[newdate];
    
def peaks(WL,fromdate,todate, window_size):
    """
    Returns an array of peak values for disjoint windows of window size from fromdate to todate
    
    Parameters
    ----------
    fromdate: datetime.date
        starting date in the datetime.date class
    todate: datetime.date
        ending date in the datetime.date class
    window_size: int
        size of the window in days for the peaks
    """
    
    s=WL.dindex(fromdate);
    e=WL.dindex(todate);
    num_windows=int(((e-s)+1)/window_size);
    peak_array=[0]*num_windows;
    aux=s;
    for i in range(0,num_windows):
        peak_array[i]=max(WL.wl[aux:(aux+window_size-1) ] );
        aux=aux+window_size;
    return peak_array;
    
def plot(WL,fromdate,todate):
    """
    Line plot of water levels time series and histogram from fromdate to todate
    """
    
    s=WL.dindex(fromdate);
    e=WL.dindex(todate);
    ndays=e-s;
    plt.figure(1);
    axs=plt.subplot(2,1,1);
    plt.plot(WL.dates[s:e], WL.wl[s:e]);
    locator=None;
    if ndays<36:
        locator=mdates.DayLocator(interval=7);
    elif ndays<130:
        locator=mdates.WeekdayLocator(interval=3);
    elif ndays<370:
        locator=mdates.MonthLocator(interval=2);
    else:
        locator=mdates.AutoDateLocator(maxticks=6);
    axs.xaxis.set_major_locator(locator);
    axs.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator));
    plt.subplot(2,1,2);
    plt.hist(WL.wl[s:e]);
        
def is_missing_dates(WL,fromdate,todate, numberofmissingdates=1):
    count=0;
    s=WL.dindex(fromdate);
    e=WL.dindex(todate);
    countdays=0;
    for i in range(s+1,e+1):
        delta=WL.getdate(i)-WL.getdate(i-1);
        countdays=countdays+delta.days-1;
        if(countdays>numberofmissingdates):
            return True;
    return False;
    
def missing_dates(WL,fromdate,todate):
    md=[]
    s=WL.dindex(fromdate);
    e=WL.dindex(todate);
    countdays=0;
    for i in range(s+1,e+1):
        x=WL.getdate(i);
        y=WL.getdate(i-1);
        delta=x-y;
        if(delta.days>1):
            oneday=datetime.timedelta(days=1);
            md.append((y+oneday,x-oneday));
    return md;




