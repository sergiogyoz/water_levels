import water_levels as wal
import matplotlib.pyplot as plt
import datetime

x=wal.WaterLevels.from_csvfile(csvfile="smalltest.csv",headers=False,dateformat="%m/%d/%Y %H:%M");

aux1=x.first_date;
date1=datetime.date(1931, 1, 1);
date2=date1+datetime.timedelta(days=365);

#Jump range
#date3=datetime.date(1930,1,1);
#date4=datetime.date(1950,1,1);
#wal.plot(x, x.round_date(date3) , x.round_date(date4));

y=wal.WaterLevels.missing_dates(x,x.first_date, x.last_date);

tdate1=x.first_date;
tdate2=x.last_date;

#This week new stuff
#missdate=x.round_date(datetime.date(1878, 10, 26));
#w=x.getdate([1,3,5,7]);
#wal.WaterLevels.warning_missing_dates(x, tdate1, tdate2,5);

wal.WaterLevels.plot(x, tdate1, tdate2);
z=wal.WaterLevels.peaks(x,tdate1,tdate2, 15);


plt.plot(z);
