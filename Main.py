from watlevpy import waterlevels as wal
import watlevpy.plot.simple as simple

WL=wal.WaterLevels.from_csvfile(csvfile="./smalltest.csv",headers=True,dateformat="%m/%d/%Y %H:%M",units="ft");
simple.plot(WL,gtype=3);