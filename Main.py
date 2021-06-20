import water_levels as wal
import matplotlib.pyplot as plt
import datetime

#x=wal.WaterLevels.from_csvfile(csvfile="smalltest.csv",headers=False,dateformat="%m/%d/%Y %H:%M");

#date1=datetime.date(1931, 1, 1);
#date2=date1+datetime.timedelta(days=365);

#Jump range
#date3=datetime.date(1930,1,1);
#date4=datetime.date(1950,1,1);
#wal.plot(x, x.round_date(date3) , x.round_date(date4));
#z=wal.peaks(x,tdate1,tdate2, 15); needs fixing now


#tdate1=x.first_date-datetime.timedelta(days=10);
#tdate2=x.first_date+datetime.timedelta(days=81);

#missx=wal.WaterLevels.missing_dates(x,tdate1, tdate2);
#wal.WaterLevels.plot(x, tdate1, tdate2)

#This week new stuff
#missdate=x.round_date(datetime.date(1878, 10, 26));
#w=x.getdate([1,3,5,7]);
#w=x.get_time_window(tdate, tdate2);
#print(wal.WaterLevels.num_missing_dates(x, tdate1, tdate2));
#print(wal.WaterLevels.is_missing_in_a_row(x, tdate1, tdate2, 21));
#print(wal.WaterLevels.check_time_window(x, tdate1, tdate2));
#wal.WaterLevels.plot(x, tdate1, tdate2);

y=wal.WaterLevels.from_csvfile(csvfile="DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
date1=datetime.date(1932, 12, 25);
date2=date1+datetime.timedelta(days=30);

#z=y.get_time_window(date1,date2);


Janus=wal.WaterLevels.get_month_from_years(y, 1, range(1879,1979),20);
Marchies=wal.WaterLevels.get_month_from_years(y, 3, range(1879,1979),20);

means=[  sum(Janus[i])/len(Janus[i]) for i in range(len(Janus)) ];

means=[ means[i] if means[i]>0 else None for i in range(len(means))];
plt.plot(means);
