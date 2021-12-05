import datetime
import matplotlib.pyplot as plt
#base class for time series
import watlevpy.time_series as wal 
#for plotting
import watlevpy.plot.plot as wplot


WL=wal.TSReader.from_csvfile(csvfile="./data_files/DubuqueIA.csv",
                             headers=True,
                             dateformat="%m/%d/%Y %H:%M");

fromyear=WL.first_date.year+1;
toyear=WL.last_date.year-1;

x=wplot.YearEvol.animate(WL, fromyear, toyear,smooth=0, save=True, 
                         interval=100 ,bitrate=4800, dpi=100, 
                         filename="year_evol_animation",
                         fileformat="mp4",yeardata=None, 
                         units="ft", xfiguresize=12.8, yfiguresize=9.6)

