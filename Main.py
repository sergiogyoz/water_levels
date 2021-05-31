import water_levels as wal
import matplotlib.pyplot as plt
import datetime

x=wal.WaterLevels.from_csvfile(csvfile="DubuqueIA.csv",headers=False,dateformat="%m/%d/%Y %H:%M");

aux1=x.first_date;
date1=datetime.date(1931, 1, 1);
date2=date1+datetime.timedelta(days=365);

date3=datetime.date(1878,8,1);
date4=datetime.date(1879,8,1);

print(wal.is_missing_dates(x,date3,date4));

y=wal.missing_dates(x,date3, date4);

wal.plot(x,date3, date4);

#y=x.peaks(date1,date3, 365);

#plt.plot(y);
