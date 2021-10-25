import csv
import datetime
import calendar

#I should use numpy to keep data size of simple data types like integers small.

#Whenever you see WL it is an instance of a TS object, it used to stand for WaterLevels
class TS:
    """
    TS is the base class for daily, monthly, yearly, and other period measurements. 
    It is a placeholder for the data, which is used in the for plotting, application 
    of statistical analisys, reading of files and more!
    
    """
    #this are the currently supported frequencies
    _FREQUENCIES=["daily","weekly","30monthly","365yearly","monthly","yearly","custom",];
    
    def __init__(self, waterlevels=[], datesarray=[], units="", frequency="daily", customdelta=0): #class constructor
        """
        Time series object instance. Use this constructor for raw python data, 
        if reading from a file use any of the from_(filetype) functions in 
        the TSReader class
        
        Parameters
        ----------
        waterlevels: float array
            array of the time series values
        datesarray: datetime array
            dates as datetime objects corresponding to the day of the waterlevels measurements 
        units: string (optional)
            units of the wl measurements as a string
        frequency: string (optional)
            the frequency of the measurements used in the delta function to calculate next or previous date, etc.
        customtimewindow: int (optional)
            a custom time delta for a custom frequency. It only works if the frequency is set to "custom".
        """
        waterlevels=waterlevels if waterlevels else [];
        datesarray=datesarray if datesarray else [];  
        try:
            self.first_date=datesarray[0];
            self.last_date=datesarray[-1];
        except IndexError:
            pass; #empty TS object
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
    
    def __repr__(self): 
        try:
            self.wl[0];
            return f"[{self.first_date}:{self.wl[0]},..., {self.last_date}:{self.wl[-1]}]"; 
        except IndexError:
            return f"TS empty";

    def __str__(self): 
        try:
            self.wl[0];
            rstr=f"time: {self.first_date},..., {self.last_date} \n";
            rstr=rstr+f"frequency: {self.frequency} \n";
            rstr=rstr+f"units: {self.units} \n";
            rstr=rstr+f"lenght: {self.n} \n";
            rstr=rstr+f"values: {self.wl[0]},...,{self.wl[-1]}";
            return rstr; 
        except IndexError:
            return "  empty TS object  ";
        
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
    
    def get_time_window(self,fromdate=None,todate=None): #returns the existing time series values from fromdate to todate
        """
        Returns the time series values from fromdate to todate (it does not keep track of the dates, 
        use for extracting values only). If rounding down or up is impossible inside the data it returns
        an empty array. If rounding is possible but the range contains no values it returns an empty array.
        """
        if not self.wl:
            return [];
        fromdate=fromdate if fromdate else self.first_date;
        todate=todate if todate else self.last_date;
        
        try:
            s=TS.round_date(self, fromdate,roundup=True);
            s=self.getindex(s);
            e=TS.round_date(self, todate);
            e=self.getindex(e);        
        except KeyError:
            print(f"range {fromdate} to {todate} is outside of bounds");
            return [];
        return [self.wl[i] for i in range(s,e+1)];
    
    def delta(self,currentdate=None,forward=True):
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
            if forward:
                d=datetime.timedelta(days=calendar.monthrange(currentdate.year,currentdate.month)[1]);
            else:
                aux=TS(frequency="monthly");
                prev_month_date=aux._normalize_date(currentdate)-datetime.timedelta(days=1);
                d=datetime.timedelta(days=calendar.monthrange(prev_month_date.year,prev_month_date.month)[1]);                
        if self.frequency=="yearly":
            if currentdate==None:
                raise ValueError("no currentdate provided");
            if forward:
                d=datetime.timedelta(days=365+calendar.isleap(currentdate.year));
            else:
                aux=TS(frequency="yearly");
                prev_year_date=aux._normalize_date(currentdate)-datetime.timedelta(days=1);
                d=datetime.timedelta(days=365+calendar.isleap(prev_year_date.year));
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

    def get_time_window_dates(self,fromdate=None,todate=None):
        """
        returns the existing dates from fromdate to todate on the object.
        If rounding down or up is impossible inside the data it returns and
        empty array. If rounding is possible but the range contains no values
        it returns an empty array.
        """
        if not self.wl:
            return [];
        fromdate=fromdate if fromdate else self.first_date;
        todate=todate if todate else self.last_date;
        try:
            s=TS.round_date(self, fromdate,roundup=True);
            s=self.getindex(s);
            e=TS.round_date(self, todate);
            e=self.getindex(e); 
        except KeyError:
            print(f"range {fromdate} to {todate} is outside of bounds");
            return [];
        return [self.dates[i] for i in range(s,e+1)];
    
    @staticmethod 
    def round_date(WL,date,roundup=False): #rounds down the date in the array (if possible)
        """
        This method takes a datetime.date object and rounds it to a date inside the
        WL object. It defaults to rounding down (roundup=False).

        Impossible to round if rounding up above data or rounding down below data, 
        in which case it throws a KeyError Exception. 

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
            delta=-WL.delta(newdate,False);
        
        isfixeddelta=(WL.frequency!="monthly" and WL.frequency!="yearly");
        if isfixeddelta:            
            while newdate not in WL.date_index:
                newdate=newdate+delta;
        else:
            while newdate not in WL.date_index:
                delta=WL.delta(newdate);
                if not roundup:  
                    delta=-WL.delta(newdate,False);
                newdate=newdate+delta;

        print(f"closest date found to {date} is: {newdate}")
        return newdate;
        

        raise IndexError("The date can't be rounded in the dates array");
    
    @staticmethod
    def isEmpty(WL):
        try:
            WL.getwl(0);
            return False;
        except IndexError:
            return True;
    
    @staticmethod 
    def sub_TS(WL,fromdate,todate):
        """
        Returns a TS object with the same parameters as WL with the range between 
        fromdate to todate.
        """
        s=TS.round_date(WL, fromdate,roundup=True);
        s=WL.getindex(s);
        e=TS.round_date(WL, todate);
        e=WL.getindex(e);
        indices=range(s,e+1);
        sub=TS(WL.getwl(indices),WL.getdate(indices),WL.units,WL.frequency,WL._custom_delta);
        return sub;
    
    @staticmethod
    def save_to_csv(WL,name,valuesonly=False):
        with open(name+".csv","w",newline='') as csvfile:        
            writer = csv.writer(csvfile);
            for i in range(WL.n):
                x=[] if valuesonly else [str(WL.dates[i])]; 
                x.append(str(WL.wl[i]));
                writer.writerow(x);
                
    @staticmethod
    def _check_freq(frequency,raiseError=True):
        if frequency in TS._FREQUENCIES:
            return True;
        else:
            if raiseError:
                raise TypeError(f"frequency value '{frequency}' is not supported (possibly a typo)");
            print(f"frequency value '{frequency}' is not supported (possibly a typo)");
            return False;
    
    @staticmethod
    def scalarFuction(WL,func,fromdate=None,todate=None):
        fromdate= fromdate if fromdate else WL.first_date;
        todate= todate if todate else WL.last_date;      
        
        values=WL.get_time_window(fromdate,todate);
        return func(values);
    
    @staticmethod
    def applyFunction(WL,func,fromdate=None,todate=None):
        fromdate= fromdate if fromdate else WL.first_date;
        todate= todate if todate else WL.last_date;      
        
        values=WL.get_time_window(fromdate,todate);
        values=[func(val) for val in values];
        x=TS(values,WL.get_time_window_dates(fromdate,todate),WL.units,WL.frequency,WL._custom_delta);
        return x;
        
class TSFilter:
    """
    Utility filtering class for further statistical analysis from TS objects. 
    Helps extract specific years or months from TS objects. It can extract the peaks, 
    POTs, averages and more from a TS object. It also has several checks that return
    true or false if data has holes, is missing too many dates, etc. 
    """
    
    #--------BASE FUNCTIONS FOR THE CHECKS, CAREFUL WHEN EDITING THESE
    @staticmethod    
    def num_missing_dates(WL,fromdate,todate): #returns the number of missing dates in WL from fromdate to todate
        """
        returns the number of missing dates (it takes into account the frequency information)
        """
        if WL.frequency=="daily":            
            try: 
                s=TS.round_date(WL, fromdate,roundup=True);
                s=WL.getindex(s);
            except KeyError: #impossible to round means it's missing all dates
                return (todate-fromdate).days+1;

            try:
                e=TS.round_date(WL, todate);
                e=WL.getindex(e);
            except KeyError: #same here
                return (todate-fromdate).days+1;

            return (todate-fromdate).days-(e-s);
        else:
            total=0; #total dates that should fit in WL
            actual=0;#actual dates in WL
            idate=WL.first_date;
            while idate<=WL.last_date:
                total=total+1;
                missing=False;
                try:
                    TS.getindex(idate);
                except KeyError:
                    missing=True;
                actual=actual+(not missing);
                idate=idate+WL.delta(idate);
            return total-actual;
        
    @staticmethod
    def missing_dates(WL,fromdate,todate): #returns missing DAYS in WL from fromdate to todate
        """
        Returns an array of pairs (firstdaymiss,lastdatemiss) where the run from 
        firstdaymiss to lastdaymiss are missing days.
        """        
        if WL.frequency=="daily":
            md=[]
            try:
                s=TS.round_date(WL, fromdate,roundup=True);
                if s!=fromdate:
                    md.append((fromdate,s-WL.delta(s,forward=False)));
                s=WL.getindex(s);
            except KeyError:
                return [(fromdate,todate)];
            missinglast=False;
            try:
                e=TS.round_date(WL, todate);
                if e!=todate:
                    missinglast=True;
                e=WL.getindex(e);
            except KeyError:
                return [(fromdate,todate)];
            
            for i in range(s+1,e+1):
                x=WL.getdate(i);
                y=WL.getdate(i-1);
                if((x-y).days>1):
                    oneday=datetime.timedelta(days=1);
                    md.append((y+oneday,x-oneday));
            if missinglast:
                md.append((WL.getdate(e)+WL.delta(e),todate));
            return md;
        else:
            md=[]
            fd=WL._normalize_date(fromdate);
            td=WL._normalize_date(todate);
            try:
                s=TS.round_date(WL, fd,roundup=True);
                if s!=fd:
                    md.append((fd,s-WL.delta(s,forward=False)));
                s=WL.getindex(s);
            except KeyError:
                return [(fd,td)];
            missinglast=False;
            try:
                e=TS.round_date(WL, td);
                if e!=td:
                    missinglast=True;
                e=WL.getindex(e);
            except KeyError:
                return [(fd,td)];
            
            for i in range(s+1,e+1):
                x=WL.getdate(i);
                y=WL.getdate(i-1);
                if((x-y).days> WL.delta(y).days):
                    fdelta=WL.delta(y);
                    bdelta=WL.delta(x);
                    md.append((y+fdelta,x-bdelta));
            if missinglast:
                ld=WL.getdate(e);
                fdelta=WL.delta(ld);
                md.append((ld+WL.delta(ld),td));
            return md;

    @staticmethod            
    def is_missing_dates(WL,fromdate,todate, num_missing_dates=0): #returns true if WL is missing more than num_missing_dates
        """
        True if there are num_missing_dates or more missing DAYS from fromdate to todate. Otherwise returns false
        """
        
        if(TSFilter.num_missing_dates(WL, fromdate, todate)>num_missing_dates): return True;
        return False;

    @staticmethod 
    def is_missing_in_a_row(WL,fromdate,todate,max_consecutive_days): #returns true if it's missing more than max_consecutive_days consecutive days in a row
        """
        returns true if there are more than max_consecutive_days consecutive days missing from fromdate to todate
        """
        
        md=TSFilter.missing_dates(WL,fromdate,todate);
        for i in range(len(md)):
            if (md[i][1]-md[i][0]).days+1>max_consecutive_days:
                print(f"last consecutive day check at {md[i][1]}")
                return True;
        return False;
    
    @staticmethod 
    def _missing_periods(WL,fromdate,todate): #missing date function for different frequencies
        """
        Assumes fromdate and todate a
        """
        pass;
    
    #-----------------HERE THEY END
    
    @staticmethod 
    def averages_from_TS(WL, outfreq, customdelta=0):#returns a TS object with the averages of a given frequency
        """
        It returns a TS object with outfreq frequency (e.g. monthly) averages 
        from WL. The input can be any TS object
        """
        TS._check_freq(outfreq);
        if TS.isEmpty(WL):
            return WL;
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
                print(f"no values found in {x} ");
            x=x+aux.delta(x);
        return TS(rwls,rdates,WL.units,outfreq,customdelta);
    
    @staticmethod 
    def peaks_from_TS(WL, outfreq, customdelta=0, maximum=True): #returns max peaks every outfreq (e.g. monthly)
        """
        It returns a TS object with outfreq (e.g. monthly) maximums or minimums from WL. The input can be any TS object.
        """    
        TS._check_freq(outfreq);
        if TS.isEmpty(WL):
            return WL;
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
    def POT_from_TS(WL, threshold, over=True): #returns a TS object with the Peaks Over Threshold
        """
        It returns a TS objects with the values that are larger than
        the threshold parameter. The input can be any TS object.
        """        
        if TS.isEmpty(WL):
            return WL;
        
        rdates=[];
        rwls=[];
        
        for index in range(WL.n):
            add=False;
            if over and (WL.wl[index]>threshold):#if over threshold
                add=True;
            if (not over) and WL.wl[index]<threshold:#if under threshold
                add=True;
            if add: #add date and value
                rwls.append(WL.wl[index]);
                rdates.append(WL.dates[index]);
        return TS(rwls,rdates,WL.units,WL.frequency,WL._custom_delta);

    @staticmethod 
    def month_of_years_from_TS(WL,month,years=None,miss_days_tol=27,consecutive_days_missed=31):
        """
        Returns a dictionary with keys being the year and values being the 
        TS object(s) from a month in a (the) given year(s), e.g.
        all Februaries from 1980 to 2010.
        
        If data doesn't pass the test it returns the [-1] array. if no data exist 
        on the range but passes the test it returns an empty array [].
        """
        m=[];
        ys=[];
        if not years:
            years=range(WL.first_date.year, WL.last_date.year);
        aux=TS([-1],[WL.first_date],frequency="monthly");
        for year in years:
            firstdaymonth=datetime.date(year, month, 1);
            lastdaymonth=datetime.date(year, month, 1)+aux.delta(firstdaymonth)-datetime.timedelta(days=1); #not the actual last day of the month
            if TSFilter.check_time_window(WL, firstdaymonth, lastdaymonth,miss_days_tol,consecutive_days_missed):
                values=WL.get_time_window(firstdaymonth,lastdaymonth);
                dates=WL.get_time_window_dates(firstdaymonth,lastdaymonth);
                mTS=TS(values,dates,WL.units,WL.frequency,WL._custom_delta);
                ys.append(year);
                m.append(mTS);
            else:
                mTS=TS([],[],WL.units,WL.frequency,WL._custom_delta);
                ys.append(year);
                m.append(mTS);
                print(f"Not enought {datetime.date(1,month,1).strftime('%B')} dates in {year} ");
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
        
        passed=not (TSFilter.is_missing_dates(WL, fromdate, todate, num_missing_dates=miss_days_tol) or
                TSFilter.is_missing_in_a_row(WL, fromdate, todate, max_consecutive_days=consecutive_days_missed))
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
    
    @staticmethod
    def longest_continuous_streak(WL):
        pass;

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

    @classmethod
    def from_USGS(cls,csvfile,site_code,param_code,dateformat="%m/%d/%Y", units="ft"): #reads TS from csvfile
        """
        Creates instance of TS class from a two column file in the default USGS tab
        separated format
        
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
            mydata=list(csv.reader(
                csvdata,
                delimiter="\t"
                ));

            while(mydata[0][0][0]=='#'):
                x=mydata.pop(0);        
            headers=mydata.pop(0);
            mydata.pop(0); #trash the line with the weird stuff
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
