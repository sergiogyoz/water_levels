import water_levels as wal
import matplotlib.pyplot as plt
import datetime

x=wal.WaterLevels.from_csvfile("MadeupData.csv");

date1=x.start_date;
date2=x.start_date+datetime.timedelta(days=365);
date3=x.end_date;

#x.plot(date1,date2);

y=x.peaks(date1,date3, 365);

plt.plot(y);
plt.ylim(119.8, 120);
