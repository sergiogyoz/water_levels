import datetime
import watlevpy.time_series as wal
from watlevpy.time_series import TS 

class YearData(TS):
    """Raw data class used in the year evolution plotting"""
    
    def __init__(self, d, waterlevels=None, datesarray=None, units="", frequency="", customdelta=0):
        super().__init__(waterlevels=None, datesarray=None, units=units, frequency=frequency, customdelta=customdelta)
        initialyear=self.first_date.year;
        endyear=self.last_date.year;
        years=range(initialyear, endyear+1);
        self.first_year=initialyear;
        self.last_year=endyear;
            
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