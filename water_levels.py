import csv
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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
    
    def getdate(self,i): #use range to acess several indices from it
        if isinstance(i,int):
            return self.dates[i];
        return [self.dates[index] for index in i]
    
    def setdate(self,i,date):
        self.dates[i]=date;
        
    def getwl(self,i): #use range to acess several indices from it
        if isinstance(i,int):
            return self.wl[i];
        return [self.wl[index] for index in i]
    
    def setwl(self, i, value):
        self.wl[i]=value;
        
    def getindex(self,date):
        """
        Index of a given date. If date doesn't exist it throws a key error
        """
        
        return self.date_index[date];
        
    def round_date(self, date, roundup=False, rounding=True):
        """
        defaults to round down
        """
        
        newdate=None;
        try:
            self.date_index[date];
            return date;
        except KeyError:
            if not rounding:
                raise KeyError(f"date {date} is missing");                
        #brute force solution to rounding up or down
        delta=datetime.timedelta(days=-1);
        if roundup:
            delta=datetime.timedelta(days=1)
        if rounding:
            newdate=date+delta;
            while newdate not in self.date_index:
                newdate=newdate+delta;
            print(f"closest date found to {date} is: {newdate}")
            return newdate;
        raise IndexError("The date can't be rounded in the dates array");

    @classmethod
    def from_csvfile(cls,csvfile,headers=True,dateformat="%m/%d/%Y"):
        """
        Creates instance of WaterLevels class from two column csv file
        
        The first column of the csv are the dates and the second one the water levels. If using csv files 
        imported from excel save as csv (MS-DOS)
        
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
            n=0;
            for i in range(0,m):
                parseable=False;
                try:
                    wl[n]=float(mydata[i][1]);
                    parseable=True;
                except ValueError:
                    pass;
                except:
                    print("Unexpected error while reading water values");
                    raise;
                else:
                    n=n+1;
                if parseable:
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
    
    @staticmethod    
    def num_missing_dates(WL,fromdate,todate,tolerance=0):
        """
        returns the number of missing days
        """
        
        s=WL.getindex(fromdate);
        e=WL.getindex(todate);
        return (todate-fromdate).days-(e-s);
        
#I should push this one out and instead make filtering methods since this one is more about the stats than handling WLs
    
    @staticmethod
    def peaks(WL,fromdate,todate, window_size, max_missing_dates=0):
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
        max_missing_dates: int
            maximum number of missing dates it tolerates in a window
        """
        
        s=WL.getindex(fromdate);
        e=WL.getindex(todate);
        
        num_windows=int(((e-s)+1)/window_size);
        peak_array=[0]*num_windows;
        aux=s;
        for i in range(0,num_windows):
            peak_array[i]=max(WL.getwl(range(aux,aux+window_size)));
            aux=aux+window_size;
        return peak_array;
    
    @staticmethod    
    def plot(WL,fromdate,todate):
        """
        Line plot of water levels time series and histogram from fromdate to todate
        """
        
        s=WL.getindex(fromdate);
        e=WL.getindex(todate);
        ndays=e-s;
        plt.figure(1);
        axs=plt.subplot(2,1,1);
        plt.scatter(WL.getdate(range(s,e+1)), WL.getwl(range(s,e+1)),marker=".");
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
        plt.hist(WL.getwl(range(s,e+1)));
        plt.show();

    @staticmethod            
    def is_missing_dates(WL,fromdate,todate, num_missing_dates=1):
        """
        True if there are num_missing_dates or more missing dates from fromdate to todate. Otherwise returns
        false
        """
        
        s=WL.getindex(fromdate);
        e=WL.getindex(todate);
        countdays=0;
        for i in range(s+1,e+1):
            delta=WL.getdate(i)-WL.getdate(i-1);
            countdays=countdays+delta.days-1;
            if(countdays>=num_missing_dates):
                return True;
        return False;

    @staticmethod
    def missing_dates(WL,fromdate,todate):
        """
        Returns an array of 2-tuples (a,b) such that the run from day a to day b are missing days
        """
        
        md=[]
        s=WL.getindex(fromdate);
        e=WL.getindex(todate);
        countdays=0;
        for i in range(s+1,e+1):
            x=WL.getdate(i);
            y=WL.getdate(i-1);
            if((x-y).days>1):
                oneday=datetime.timedelta(days=1);
                md.append((y+oneday,x-oneday));
        return md;
    
    
    
    
