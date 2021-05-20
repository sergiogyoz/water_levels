import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

class WaterLevels:
    
    def __init__(self,
                 startdate=datetime.date.min,
                 enddate=datetime.date.min,
                 n=0,
                 waterlevels=[],
                 datesarray=[]
                 ):
        self.start_date=startdate;
        self.end_date=enddate;
        self.n=n;
        self.wl=waterlevels;
        self.dates=datesarray;

    @classmethod
    def from_csvfile(cls,csvfile,headers=True):
        with open(csvfile,newline='') as csvdata:
            mydata=list(csv.reader(csvdata))
            if headers:
                mydata.pop(0);
            m=len(mydata);
            wl=[0]*m;
            dates=[0]*m;
            n=0;
            for i in range(0,m):
                n=n+1;
                try:
                    dates[i]=datetime.datetime.strptime(mydata[i][0],"%m/%d/%Y").date();
                except ValueError:
                    print("format on entry", mydata[i][0], "is wrong");
                wl[i]=float(mydata[i][1]);
            return WaterLevels(startdate=dates[0],enddate=dates[-1],n=n,waterlevels=wl,datesarray=dates);

    def date_index(self,date):
        n=self.start_date;
        while(n<=self.end_date and n<=date):
            if(n==date):
                return (n-self.start_date).days;
            n=n+datetime.timedelta(days=1);
    
    def peaks(self, fromdate,todate, window_size):
        start=self.date_index(fromdate);
        end=self.date_index(todate);
        num_windows=int(((end-start)+1)/window_size);
        peak_array=[0]*num_windows;
        aux=0;
        for i in range(0,num_windows):
            peak_array[i]=max(self.wl[ aux:(aux+window_size-1) ] );
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
    