import csv
import datetime

#I should use numpy to keep data size of simple data types as integers small.
        
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
    
    def __init__(self, waterlevels=None, datesarray=None, units=""): #class constructor
        """
        Use for raw python data, if reading from a file use any of the from_(filetype) constructors
        
        Parameters
        ----------
        waterlevels: float array
            the daily measurements of the water level
        datesarray: datetime array
            dates as datetime objects corresponding to the day of the wl measurements 
        """
        waterlevels=waterlevels if waterlevels else [];
        datesarray=datesarray if datesarray else [];        
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
        self.units=units;
    
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
        
    def getindex(self,date): #get index of a date if it exist
        """
        Index of a given date. If date doesn't exist it throws a key error
        """
        if isinstance(date, datetime.date):
            return self.date_index[date];
        return [self.date_index[d] for d in date];
    
    def get_time_window(self,fromdate,todate): #returns the existing water level values from fromdate to todate
        """
        Returns the water level values from from date to todate (it does not keep track of the dates, 
        use for extracting wl values only). If rounding down or up is impossible inside the data it throws an
        error. If rounding is possible but the range contains no values it returns an empty array.
        """
    
        s=WaterLevels.round_date(self, fromdate,roundup=True);
        s=self.getindex(s);
        e=WaterLevels.round_date(self, todate);
        e=self.getindex(e);    
        return [self.wl[i] for i in range(s,e+1)];
    
    def get_time_window_dates(self,fromdate,todate):
        """
        returns the existing dates from fromdate to todate on the object.
        If rounding down or up is impossible inside the data it throws an error. If rounding is possible 
        but the range contains no values it returns an empty array.
        """
        
        s=WaterLevels.round_date(self, fromdate,roundup=True);
        s=self.getindex(s);
        e=WaterLevels.round_date(self, todate);
        e=self.getindex(e); 
        return [self.dates[i] for i in range(s,e+1)];
    
    @staticmethod 
    def round_date(WL,date,roundup=False): #rounds down the date in the array (if possible)
        """
        defaults to rounding down. Set roundup to True to round up. 
        """
        
        newdate=None;
        debugtext="down";
        try:
            WL.date_index[date];
            return date;
        except KeyError:
            pass;
        delta=datetime.timedelta(days=-1);
        roundable=(WL.first_date<date);
        if roundup:
            delta=datetime.timedelta(days=1);
            roundable=(WL.last_date>date);
            debugtext="up";
        if not roundable:
           raise KeyError(f"date {date} can't be rounded {debugtext} because is outside of bounds"); 
        #We are roundable so we can try to start rounding from date or the boundaries, whichever closer
        if not roundup:
            if date<WL.last_date: newdate=date;
            else: newdate=WL.last_date;
        else:
            if date>WL.first_date: newdate=date;
            else: newdate=WL.first_date;
        while newdate not in WL.date_index:
            newdate=newdate+delta;
        print(f"closest date found to {date} is: {newdate}")
        return newdate;
        

        raise IndexError("The date can't be rounded in the dates array");

    @classmethod
    def from_csvfile(cls,csvfile,headers=True,dateformat="%m/%d/%Y", units="ft"): #reads WaterLevels from csvfile
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
                print(f"There are {m-n} wrong format water levels (possibly missing dates)");
            dates=dates[:n];
            wl=wl[:n];
            return WaterLevels(waterlevels=wl,datesarray=dates,units=units);
    
    @staticmethod 
    def sub_wl(WL,fromdate,todate):
        s=WaterLevels.round_date(WL, fromdate,roundup=True);
        s=WL.getindex(s);
        e=WaterLevels.round_date(WL, todate);
        e=WL.getindex(e);
        indices=range(s,e+1);
        sub=WaterLevels(WL.getwl(indices),WL.getdate(indices),WL.units);
        return sub;
    
    @staticmethod    
    def num_missing_dates(WL,fromdate,todate): #returns the number of missing dates in WL from fromdate to todate
        """
        returns the number of missing days
        """
        try:
            s=WL.getindex(fromdate);
        except KeyError:
            try:
                s=WaterLevels.round_date(WL, fromdate,roundup=True);
                s=WL.getindex(s);
            except KeyError:
                return (todate-fromdate).days+1;
        try:
            e=WL.getindex(todate);
        except KeyError:
            try:
                e=WaterLevels.round_date(WL, todate);
                e=WL.getindex(e);
            except KeyError:
                return (todate-fromdate).days+1;
        return (todate-fromdate).days-(e-s);
        
    @staticmethod
    def missing_dates(WL,fromdate,todate): #returns missing days in WL from fromdate to todate
        """
        Returns an array of 2-tuples (a,b) such that the run from day a to day b are missing days
        """
        
        md=[]
        try:
            s=WL.getindex(fromdate);
        except KeyError:
            try:
                s=WaterLevels.round_date(WL, fromdate,roundup=True);
                md.append((fromdate,s-datetime.timedelta(days=1)));
                s=WL.getindex(s);
            except KeyError:
                md=[(fromdate,todate)];
                return md;
        missinglast=False;
        try:
            e=WL.getindex(todate);
        except KeyError:
            try:
                e=WaterLevels.round_date(WL, todate);
                e=WL.getindex(e);
                missinglast=True;
            except KeyError:
                md=[(fromdate,todate)];
                return md;
        countdays=0;
        for i in range(s+1,e+1):
            x=WL.getdate(i);
            y=WL.getdate(i-1);
            if((x-y).days>1):
                oneday=datetime.timedelta(days=1);
                md.append((y+oneday,x-oneday));
        if missinglast:
            md.append((WL.getdate(e)+datetime.timedelta(days=1),todate));
        return md;

    @staticmethod            
    def is_missing_dates(WL,fromdate,todate, num_missing_dates=0): #returns true if WL is missing more than num_missing_dates
        """
        True if there are num_missing_dates or more missing dates from fromdate to todate. Otherwise returns false
        """
        
        if(WaterLevels.num_missing_dates(WL, fromdate, todate)>num_missing_dates): return True;
        return False;

    @staticmethod 
    def is_missing_in_a_row(WL,fromdate,todate,max_consecutive_days): #returns true if it's missing more than max_consecutive_days consecutive days in a row
        """
        returns true if there are more than max_consecutive_days consecutive days missing from fromdate to todate
        """
        
        md=WaterLevels.missing_dates(WL,fromdate,todate);
        for i in range(len(md)):
            if (md[i][1]-md[i][0]).days+1>max_consecutive_days:
                print(f"last consecutive day check at {md[i][1]}")
                return True;
        return False;
    
    @staticmethod 
    def check_time_window(WL,fromdate,todate,miss_days_tol=0,consecutive_days_missed=0): #check from fromdate to todate
        """
        returns false if the number of missing days is more than miss_day_tol. it also returns false if there are more
        than consecutive_days_missed consecutive days missing. otherwise it returns true
        
        general function to check if there are missing days and missing consecutive days in a window
        """
        
        passed=not (WaterLevels.is_missing_dates(WL, fromdate, todate, num_missing_dates=miss_days_tol) or
                WaterLevels.is_missing_in_a_row(WL, fromdate, todate, max_consecutive_days=consecutive_days_missed))
        return passed;

    @staticmethod 
    def check_week(WL,fromdate,miss_days_tol=0,consecutive_days_missed=7): #check a 7 day period 
        return WaterLevels.check_time_window(WL, fromdate, fromdate+datetime.deltatimedelta(days=7) ,miss_days_tol,consecutive_days_missed);

    @staticmethod 
    def check_month(WL,year,month,miss_days_tol=0,consecutive_days_missed=30): #check a 30 day period 
        firstdayofmonth=datetime.date(year,1 , 1)+datetime.timedelta(days=(month-1)*30);
        lastdayofmonth=firstdayofmonth+datetime.timedelta(days=29);
        return WaterLevels.check_time_window(WL, firstdayofmonth, lastdayofmonth, miss_days_tol, consecutive_days_missed);

    @staticmethod 
    def check_year(WL,year, miss_days_tol=0,consecutive_days_missed=365): #check a 365 day period
        dindex=datetime.date(year, 1, 1);        
        return WaterLevels.check_time_window(WL, dindex, dindex+datetime.timedelta(days=365),miss_days_tol,consecutive_days_missed);

    @staticmethod 
    def check_year_by_month(WL,year,miss_days_month=0): #check a 360 year making sure there're no big holes along
        dindex=datetime.date(year, 1, 1);
        for i in range(12):
            fdm=dindex+datetime.timedelta(days=i*30);
            if WaterLevels.check_month(WL, fdm, miss_days_month) :
                return False;
        return True;
    
    @staticmethod
    def get_month_from_years(WL,month,years,miss_days_tol=0,consecutive_days_missed=30):
        """
        get data from a month in a given year(s). If data doesn't pass the test it returns the [-1] array.
        if no data exist on the range but passes the test it returns an empty array [].
        """
        
        if isinstance(years,int): #if only a number then make it into a single value array
            years=[years];
        n=len(years);
        m=[];
        addyear=[False]*n;
        for i in range(n):
                #Does resizing impact performance too much in here??
                if WaterLevels.check_month(WL, years[i], month,miss_days_tol,consecutive_days_missed):
                    firstdayofmonth=datetime.date(years[i],1,1)+datetime.timedelta(days=30*(month-1));
                    m.append(WL.get_time_window(firstdayofmonth,firstdayofmonth+datetime.timedelta(days=30-1)));
                else:
                    m.append([-1]);
        return m;
                
    @staticmethod
    def get_years(WL,years,checkid=0,miss_day_tol=365,consecutive_days_missed=365):
        """
        gets wl data from the given years. If data doesn't pass the test in a year it returns the [-1] array for that year.
        if no data exist on the range but passes the test it returns an empty array [].
        """
        
        ys=[];
        for year in years:
            goodyear=True;
            if checkid==1:
                goodyear=WaterLevels.check_year(WL, year, miss_day_tol, consecutive_days_missed);
            if checkid==2:
                goodyear=WaterLevels.check_year_by_month(WL,year,miss_day_tol);
            if goodyear:
                ys.append( WL.get_time_window(datetime.date(year,1,1), datetime.date(year,12,31)) );
            else:
                ys.append([-1]);
        
        if isinstance(years, int) : return ys[0];
        return ys;        

def peaks(WL,fromdate,todate,window_size,max_missing_dates=0):
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
    
    
    
