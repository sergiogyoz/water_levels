import datetime
import watlevpy.time_series as wal

class YearData:
    """Raw data class used in the year evolution plotting"""
    
    def __init__(self, d, initialyear, endyear):
        years=range(initialyear, endyear+1);
        self.d=d;
        self.first_year=initialyear;
        self.last_year=endyear;
        self.n=len(years);


    @classmethod    
    def sub_YearData(cls, yeardata, initialyear=None, endyear=None):
        d=dict();
        first=True;
        ini=0;
        end=-1;
        for year in range(initialyear,endyear+1):
            if year in yeardata: 
                d[year]=yeardata[d];
                if not ini:
                    ini=year;
                end=year;
        return YearData(d, ini, end);
            
    @classmethod    
    def from_WL(cls, WL, initialyear=None, endyear=None): #you can probably put a year tolerance for years with too many missing days
        initialyear=initialyear if initialyear else WL.first_date.year; 
        endyear= endyear if endyear else WL.last_date.year;
        initialyear=wal.TS.round_date(WL,datetime.date(initialyear,1,1),True).year;
        endyear= wal.TS.round_date(WL,datetime.date(endyear,12,31)).year;
        ys=[];
        years=range(initialyear, endyear+1);
        for year in years:
            date1=datetime.date(year, 1, 1);
            date365=date1+datetime.timedelta(days=364);
            #get data and dates from that year
            wl=WL.get_time_window(date1, date365);
            dates=WL.get_time_window_dates(date1, date365);
            #append to ys
            dayoftheyear=[(dates[i]-date1).days+1 for i in range(len(dates))];
            ys.append([dayoftheyear,wl]);
        d=dict(zip(years,ys));
        return YearData(d, initialyear, endyear);