import water_levels as wal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

WL=wal.WaterLevels.from_csvfile(csvfile="DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");

ys=[];
initialyear=WL.first_date.year+1;
for year in range(initialyear, WL.last_date.year):
    date1=datetime.date(year, 1, 1);
    date365=date1+datetime.timedelta(days=364);
    #get dates and data from that year
    wl=WL.get_time_window(date1, date365);
    dates=WL.get_time_window_dates(date1, date365);
    #append to ys
    dayoftheyear=[(dates[i]-date1).days+1 for i in range(len(dates))];
    ys.append([dayoftheyear,wl]);
    

fig, ax= plt.subplots()
ax.set_xlim(0, 365);
ax.set_ylim(580, 615);
ax.set_xlabel("day of the year");
ax.set_ylabel(f"water level ({WL.units})");
ycounter=ax.text(160,610, '',fontsize=15)
lines=plt.plot(ys[0][0], ys[0][1], '.',[], [],'.')



def init():
    ycounter.set_text(f"year: {initialyear}")
    return lines[0],lines[1],ycounter
    
def update(frame):
    print(frame);
    ycounter.set_text(f"year: {initialyear+frame}");
    lines[1].set_data(ys[frame][0], ys[frame][1])
    return lines[0],lines[1],ycounter
    

ani = FuncAnimation(fig, update,frames=len(ys),
                    interval=100, repeat=False,
                    init_func=init, blit=True)

plt.show()

