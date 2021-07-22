import watlevpy.waterlevels as wal
import watlevpy.plot.year_evol as yevol

WL=wal.WaterLevels.from_csvfile(csvfile="./DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");
donttrashme=yevol.animate(WL);

#ys=data.YearData.from_WL(WL);
#yevol.averages(WL);
#yevol.months(WL);

