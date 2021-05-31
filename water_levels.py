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
                    n=n+1;
                except ValueError:
                    #print("Value at  ", i, " position is not parseable to float");
                    pass;
                try:
                    x=datetime.datetime.strptime(mydata[i][0],dateformat).date();
                    dates[n-1]=x;
                except ValueError:
                    print( "format on date entry "+ str(i)+" is wrong: " +str(mydata[i][0]) );
            print(f"There are {m-n} wrong format water levels (possibly missing dates)")

            dates=dates[:n];
            wl=wl[:n];
            return WaterLevels(waterlevels=wl,datesarray=dates);

    def dindex(self,date):
        """
        Index of a given date. If date doesn't exist it throws a key error
        """
        return self.date_index[date];
    
    def peaks(self, fromdate,todate, window_size):
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
        s=self.dindex(fromdate);
        e=self.dindex(todate);
        num_windows=int(((e-s)+1)/window_size);
        peak_array=[0]*num_windows;
        aux=s;
        for i in range(0,num_windows):
            peak_array[i]=max(self.wl[aux:(aux+window_size-1) ] );
            aux=aux+window_size;
        return peak_array;
    
    def plot(self,fromdate,todate):
        """
        Line plot of water levels time series and histogram from fromdate to todate
        """
        s=self.dindex(fromdate);
        e=self.dindex(todate);
        ndays=e-s;
        plt.figure(1);
        axs=plt.subplot(2,1,1);
        plt.plot(self.dates[s:e], self.wl[s:e]);
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
        plt.hist(self.wl[s:e]);
    