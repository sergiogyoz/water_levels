import watlevpy.time_series as wal
import watlevpy.plot.year_evol as yevol
import watlevpy.data as data
import watlevpy.plot.simple as wplot
import datetime

WL=wal.TSReader.from_csvfile(csvfile="./DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
foryearplot=wal.TS.sub_wl(WL, datetime.date(WL.first_date.year+1,1,1), datetime.date(WL.last_date.year-1,12,31));

yaver=wal.TSFilter.averages_from_TS(WL, "monthly");
wplot.plot(yaver,gtype=2);

#donttrashme=yevol.animate(foryearplot);
#ys=data.YearData.from_WL(WL);
#yevol.averages(WL);
#yevol.months(WL);


#Let's do some testing

