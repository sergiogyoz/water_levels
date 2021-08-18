import csv
import datetime
import calendar

#I should use numpy to keep data size of simple data types like integers small.
        
class TS:
    """
    Time Series base class for daily, monthly, yearly, and other period measurements. A 
    placeholder for the data, used in the for plotting, applycation of statistical
    analisys, reading of files and more!
    
    """
    
    _FREQUENCIES=["daily","weekly","30monthly","365yearly","monthly","yearly","custom",];
    
    def __init__(self, waterlevels=None, datesarray=None, units="", frequency="daily", customdelta=0): #class constructor
        """
        Use for raw python data, if reading from a file use any of the from_(filetype) constructors
        
        Parameters
        ----------
        waterlevels: float array
            the daily measurements of the water level
        datesarray: datetime array
            dates as datetime objects corresponding to the day of the wl measurements 
        units: string (optional)
            units of the wl measurements as a string
        frequency: string (optional)
            the frequency of the measurements used in the delta function to calculate next or previous date, etc.
        customtimewindow: int (optional)
            a custom time delta for a custom frequency. It only works if the frequency is set to "custom".
        """
        waterlevels=waterlevels if waterlevels else [];
        datesarray=datesarray if datesarray else [];        
        self.first_date=datesarray[0];
        self.last_date=datesarray[-1];
        n=len(waterlevels);
        m=len(datesarray);
        if n!=m :
            raise Exception(f"water levels and dates array are not the same size. Sizes are: {n} and {m}")
        self._custom_delta=customdelta;
        if frequency=="custom":
            if customdelta!=0:
                self._custom_delta=datetime.timedelta(days=customdelta);
            else:
                raise Exception("custom frequency set with no customtimewindow set");
        self.frequency=frequency;
        self.n=n;
        self.wl=waterlevels;
        self.dates=datesarray;
        self.date_index=dict(zip(datesarray,range(n)));
        self.units=units;
    
    def getdate(self,i): #use range to acess several indices from it
        if isinstance(i,int):
            return self.dates[i];
        return [self.dates[index] for index in i]
    
    def _setdates(self,dates):
        self.dates=dates;        
    
    def _setwl(self, wl):
        self.wl=wl;
    
    def getwl(self,i): #use range to acess several indices from it
        if isinstance(i,int):
            return self.wl[i];
        return [self.wl[index] for index in i]
        
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
        use for extracting wl values only). If rounding down or up is impossible inside the data it returns
        an empty array. If rounding is possible but the range contains no values it returns an empty array.
        """
        
        try:
            s=TS.round_date(self, fromdate,roundup=True);
            s=self.getindex(s);
            e=TS.round_date(self, todate);
            e=self.getindex(e);        
        except KeyError:
            print("range outside of bounds")
            return [];
        return [self.wl[i] for i in range(s,e+1)];
    
    def delta(self,currentdate=None):
        """
        time delta based on the frequency of the time series. If needed e.g., monthly delta changes each month,
        current date should be provided as a datetime object.
        """
        d=None;
        if self.frequency=="daily":
            d=datetime.timedelta(days=1);
        if self.frequency=="weekly":
            d=datetime.timedelta(days=7);
        if self.frequency=="30monthly":
            d=datetime.timedelta(days=30);
        if self.frequency=="365yearly":
            d=datetime.timedelta(days=365);
        if self.frequency=="monthly":
            if currentdate==None:
                raise ValueError("no currentdate provided");
            d=datetime.timedelta(days=calendar.monthrange(currentdate.year,currentdate.month)[1]);
        if self.frequency=="yearly":
            if currentdate==None:
                raise ValueError("no currentdate provided");
            d=datetime.timedelta(days=365+calendar.isleap(currentdate.year));
        if self.frequency=="custom":
            d=self._custom_delta;
        return d;
    
    def _normalize_date(self,date):
        """
        Formats a given date using the TS frequency and structure so that adding delta will yield the (possible) next date.
        """
        if self.frequency=="monthly":
            return datetime.date(date.year,date.month,1);
        if self.frequency=="yearly":
            return datetime.date(date.year,1,1);
        firstday=datetime.date.toordinal(self.first_date);
        delta=self.delta().days;
        dateordinal=datetime.date.toordinal(date);
        newdate= datetime.date.fromordinal(dateordinal-(dateordinal-firstday)%delta);
        return newdate;

    
    def get_time_window_dates(self,fromdate,todate):
        """
        returns the existing dates from fromdate to todate on the object.
        If rounding down or up is impossible inside the data it throws an error. If rounding is possible 
        but the range contains no values it returns an empty array.
        """
        
        s=TS.round_date(self, fromdate,roundup=True);
        s=self.getindex(s);
        e=TS.round_date(self, todate);
        e=self.getindex(e); 
        return [self.dates[i] for i in range(s,e+1)];
    
    @staticmethod 
    def round_date(WL,date,roundup=False): #rounds down the date in the array (if possible)
        """
        defaults to rounding down. Set roundup to True to round up. Impossible to round if
        round up above data or rounding down below data, in which case it throws a KeyError Exception. 
        It uses the corresponding frequency to calculate the "next" or "previous" date.
        """
        
        newdate=None;
        debugtext="down";
        try:
            WL.date_index[date];
            return date;
        except KeyError:
            pass;
        normdate=WL._normalize_date(date);
        try:
            WL.date_index[normdate];
            return normdate;
        except KeyError:
            pass;
        roundable=(WL.first_date<normdate);
        if roundup:
            roundable=(WL.last_date>normdate);
            debugtext="up";
        if not roundable:
           raise KeyError(f"date {date} can't be rounded {debugtext} because is outside of bounds"); 
        #We are roundable so we can try to start rounding from date or the boundaries, whichever closer
        if not roundup:
            if normdate<WL.last_date: newdate=normdate;
            else: newdate=WL.last_date;
        else:
            if normdate>WL.first_date: newdate=normdate;
            else: newdate=WL.first_date;
        #start rounding
        delta=WL.delta(newdate);
        if not roundup:  
            delta=-delta;
        
        isfixeddelta=(WL.frequency!="monthly" and WL.frequency!="yearly");
        if isfixeddelta:            
            while newdate not in WL.date_index:
                newdate=newdate+delta;
        else:
            while newdate not in WL.date_index:
                delta=WL.delta(newdate);
                if not roundup:  
                    delta=-delta;
                newdate=newdate+delta;

        print(f"closest date found to {date} is: {newdate}")
        return newdate;
        

        raise IndexError("The date can't be rounded in the dates array");
 
    @staticmethod 
    def sub_wl(WL,fromdate,todate):
        s=TS.round_date(WL, fromdate,roundup=True);
        s=WL.getindex(s);
        e=TS.round_date(WL, todate);
        e=WL.getindex(e);
        indices=range(s,e+1);
        sub=TS(WL.getwl(indices),WL.getdate(indices),WL.units,WL.frequency,WL._custom_delta);
        return sub;
    
    @staticmethod    
    def num_missing_dates(WL,fromdate,todate): #returns the number of missing dates in WL from fromdate to todate
        """
        returns the number of missing days DAYS DAYS
        """
        try:
            s=WL.getindex(fromdate);
        except KeyError:
            try:
                s=TS.round_date(WL, fromdate,roundup=True);
                s=WL.getindex(s);
            except KeyError:
                return (todate-fromdate).days+1;
        try:
            e=WL.getindex(todate);
        except KeyError:
            try:
                e=TS.round_date(WL, todate);
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
                s=TS.round_date(WL, fromdate,roundup=True);
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
                e=TS.round_date(WL, todate);
                e=WL.getindex(e);
                missinglast=True;
            except KeyError:
                md=[(fromdate,todate)];
                return md;
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
        
        if(TS.num_missing_dates(WL, fromdate, todate)>num_missing_dates): return True;
        return False;

    @staticmethod 
    def is_missing_in_a_row(WL,fromdate,todate,max_consecutive_days): #returns true if it's missing more than max_consecutive_days consecutive days in a row
        """
        returns true if there are more than max_consecutive_days consecutive days missing from fromdate to todate
        """
        
        md=TS.missing_dates(WL,fromdate,todate);
        for i in range(len(md)):
            if (md[i][1]-md[i][0]).days+1>max_consecutive_days:
                print(f"last consecutive day check at {md[i][1]}")
                return True;
        return False;
    
    @staticmethod 
    def missing_periods(): #missing function for different periods
        pass;

    

class TSFilter:
    """
    Utility filtering class for further statistical analysis from TS objects. 
    Helps extract specific years or months from TS objects. It can extract the peaks, 
    POTs, averages and more from a TS object. It also has several checks that return
    true or false if data has holes, is missing too many dates, etc. 
    """
    @staticmethod 
    def averages_from_TS(WL, outfreq, customdelta=0):#returns a TS object with the averages of a given frequency
        aux=TS([-1,-1],[WL.first_date, WL.last_date],units="",frequency=outfreq, customdelta=customdelta);
        sdate=aux._normalize_date(WL.first_date);
        edate=aux._normalize_date(WL.last_date);
        rdates=[];
        rwls=[];
        
        x=sdate;
        oneday=datetime.timedelta(days=1);
        while(x<=edate):
            val=WL.get_time_window(x,x+aux.delta(x)-oneday);
            if len(val)>0:
                rdates.append(x);
                rwls.append(sum(val)/len(val));
                #print(f"found {len(val)} values, expected {aux.delta(x)} from {aux.frequency} frequency");
            else:
                print("no values found in {x} ");
            x=x+aux.delta(x);
        return TS(rwls,rdates,WL.units,outfreq,customdelta);
    
    @staticmethod 
    def peaks_from_TS(WL, outfreq, customdelta=0, maximum=True): #maximum false returns minimums
        aux=TS([-1,-1],[WL.first_date, WL.last_date],units="",frequency=outfreq, customdelta=customdelta);
        sdate=aux._normalize_date(WL.first_date);
        edate=aux._normalize_date(WL.last_date);
        rdates=[];
        rwls=[];
        
        x=sdate;
        oneday=datetime.timedelta(days=1);
        while(x<=edate):
            val=WL.get_time_window(x,x+aux.delta(x)-oneday);
            if len(val)>0:
                rdates.append(x);
                if maximum:
                    rwls.append(max(val));
                else:
                    rwls.append(min(val));
                #print(f"found {len(val)} values, expected {aux.delta(x)} from {aux.frequency} frequency");
            else:
                print("no values found in {x} ");
            x=x+aux.delta(x);
        return TS(rwls,rdates,WL.units,outfreq,customdelta);
    
    @staticmethod 
    def month_from_years_from_TS(WL,month,years=None,miss_days_tol=27,consecutive_days_missed=31):
        """
        get data from a month in a given year(s). If data doesn't pass the test it returns the [-1] array.
        if no data exist on the range but passes the test it returns an empty array [].
        """
        m=[];
        ys=[];
        if not years:
            years=range(WL.first_date.year, WL.last_date.year);
        aux=TS([-1],[WL.first_date],frequency="monthly");
        for year in years:
            firstdaymonth=datetime.date(year, month, 1);
            lastdaymonth=datetime.date(year, month, 1)+aux.delta(firstdaymonth);
            if TSFilter.check_time_window(WL, firstdaymonth, lastdaymonth,miss_days_tol,consecutive_days_missed):
                values=WL.get_time_window(firstdaymonth,lastdaymonth);
                dates=WL.get_time_window_dates(firstdaymonth,lastdaymonth);
                mts=TS(values,dates,WL.units,WL.frequency,WL._custom_delta);
                ys.append(year);
                m.append(mts);
            else:
                print("Not enought {month} dates from {year} ");
        rmts=dict(zip(ys,m));
        return rmts;

    def years_from_TS(WL,years,checkid=0,miss_day_tol=365,consecutive_days_missed=365):
        """
        returns a TS object with the data from the given years. If data doesn't pass the 
        test or no data exist it skips that year. checkid=1 uses the miss_day_tol, 
        checkid=2 uses the consecutive_days_missed
        """
        #if I want this to work more generally I should make the missing_periods function        
        ts=[];
        ds=[];
        for year in years:
            goodyear=True;
            if checkid==1:
                goodyear=TSFilter.check_year(WL, year, miss_day_tol, consecutive_days_missed);
            if checkid==2:
                goodyear=TSFilter.check_year_by_month(WL,year,miss_day_tol);
            if goodyear:
                ts.extend( WL.get_time_window(datetime.date(year,1,1), datetime.date(year,12,31)) );
                ds.extend(WL.get_time_window_dates(datetime.date(year,1,1), datetime.date(year,12,31)));
            else:
                pass; #skipping bad years
        
        rts=TS(ts,ds,WL.units);
        return rts;

    @staticmethod 
    def check_time_window(WL,fromdate,todate,miss_days_tol=0,consecutive_days_missed=0): #check from fromdate to todate
        """
        returns false if the number of missing days is more than miss_day_tol. it also returns false if there are more
        than consecutive_days_missed consecutive days missing. otherwise it returns true
        
        general function to check if there are missing days and missing consecutive days in a window
        """
        
        passed=not (TS.is_missing_dates(WL, fromdate, todate, num_missing_dates=miss_days_tol) or
                TS.is_missing_in_a_row(WL, fromdate, todate, max_consecutive_days=consecutive_days_missed))
        return passed;
        
    @staticmethod 
    def check_week(WL,fromdate,miss_days_tol=0,consecutive_days_missed=7): #check a 7 day period 
        return TSFilter.check_time_window(WL, fromdate, fromdate+datetime.deltatimedelta(days=7) ,miss_days_tol,consecutive_days_missed);

    @staticmethod 
    def check_month(WL,year,month,miss_days_tol=0,consecutive_days_missed=30): #check a 30 day period 
        firstdayofmonth=datetime.date(year,1 , 1)+datetime.timedelta(days=(month-1)*30);
        lastdayofmonth=firstdayofmonth+datetime.timedelta(days=29);
        return TSFilter.check_time_window(WL, firstdayofmonth, lastdayofmonth, miss_days_tol, consecutive_days_missed);

    @staticmethod 
    def check_year(WL,year, miss_days_tol=0,consecutive_days_missed=365): #check a 365 day period
        dindex=datetime.date(year, 1, 1);        
        return TSFilter.check_time_window(WL, dindex, dindex+datetime.timedelta(days=365),miss_days_tol,consecutive_days_missed);

    @staticmethod 
    def check_year_by_month(WL,year,miss_days_month=0): #check a 360 year making sure there're no big holes along
        dindex=datetime.date(year, 1, 1);
        for i in range(12):
            fdm=dindex+datetime.timedelta(days=i*30);
            if TSFilter.check_month(WL, fdm, miss_days_month) :
                return False;
        return True;
    

class TSReader:
    
    @classmethod
    def from_csvfile(cls,csvfile,headers=True,dateformat="%m/%d/%Y", units="ft"): #reads TS from csvfile
        """
        Creates instance of TS class from two column csv file
        
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
            return TS(waterlevels=wl,datesarray=dates,units=units);

    
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
    
    
    
