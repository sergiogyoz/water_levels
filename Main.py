import water_levels as wal
import matplotlib.pyplot as plt
import datetime

x=wal.WaterLevels.from_csvfile(csvfile="DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");

aux1=x.first_date;
date1=datetime.date(1931, 1, 1);


date2=date1+datetime.timedelta(days=365);
date3=x.last_date;

x.plot(date1,date2);

#y=x.peaks(date1,date3, 365);

#plt.plot(y);
