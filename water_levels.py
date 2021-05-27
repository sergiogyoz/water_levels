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
                 missingdays=[]
                 ):
        """
        Use for raw python data, if reading from a file use any of the from_(filetype) constructors
        
        Parameters
        ----------
        waterlevels: float array
            the daily measurements of the water level
        datesarray: datetime array
            dates as datetime objects corresponding to the day of the wl measurements
        missingdays: (optional) integer array
            each entry has the last index of a continuous sequence of days    
        """
        self.first_date=datesarray[0];
        self.last_date=datesarray[-1];
        self.n=len(waterlevels);
        self.wl=waterlevels;
        self.dates=datesarray;
        self.md=missingdays;

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
            print(m);
            print(n);
            dates=dates[:n];
            wl=wl[:n];
            return WaterLevels(waterlevels=wl,datesarray=dates);

    def date_index(self,date):
        n=self.first_date;
        while(n<=self.last_date and n<=date):
            if(n==date):
                return (n-self.first_date).days;
            n=n+datetime.timedelta(days=1);
        return (n-self.first_date).days;
    
    def peaks(self, fromdate,todate, window_size):
        start=self.date_index(fromdate);
        end=self.date_index(todate);
        num_windows=int(((end-start)+1)/window_size);
        peak_array=[0]*num_windows;
        aux=0;
        for i in range(0,num_windows):
            peak_array[i]=max(self.wl[aux:(aux+window_size-1) ] );
            aux=aux+window_size;
        return peak_array;
    
    def plot(self,fromdate,todate):
        start=self.date_index(fromdate);
        end=self.date_index(todate);
        ndays=end-start;
        plt.figure(1);
        axs=plt.subplot(2,1,1);
        plt.plot(self.dates[start:end], self.wl[start:end]);
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
        plt.hist(self.wl[start:end]);
    