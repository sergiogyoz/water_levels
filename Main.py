import watlevpy.time_series as wal
import watlevpy.plot.year_evol as yevol
import watlevpy.data as data
import watlevpy.plot.simple as wplot
import datetime

WL=wal.TSReader.from_csvfile(csvfile="./DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
foryearplot=wal.TS.sub_wl(WL, datetime.date(WL.first_date.year+1,1,1), datetime.date(WL.last_date.year-1,12,31));

#yaver=wal.TSFilter.averages_from_TS(WL, "yearly");
#wplot.plot(yaver,gtype=2);

#ypeaks=wal.TSFilter.peaks_from_TS(WL, "monthly");
#wplot.plot(ypeaks,gtype=1);

#donttrashme=yevol.animate(foryearplot);
#yevol.months(WL,smooth=2);

#decade=wal.TSFilter.years_from_TS(WL, range(2000,2010+1));

Februaries=wal.TSFilter.month_from_years_from_TS(WL, month=2);


#wplot.plot(decade);

#-----Let's do some testing
