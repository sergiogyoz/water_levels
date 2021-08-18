import watlevpy.time_series as wal
import watlevpy.stats.tools as tools
import watlevpy.data as data
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime


#path for ffmpeg for the animation save/recording to work
plt.rcParams['animation.ffmpeg_path']="./watlevpy/plot/ffmpeg-2021-07-04-essentials_build/bin/ffmpeg.exe"

def animate(WL,fromyear=None,toyear=None,smooth=2, save=False, interval=50 ,bitrate=100, dpi=100, filename="year_evol_animation",
            fileformat="mp4",yeardata=None, units="", xfiguresize=6.4, yfiguresize=4.8):
    
    if not fromyear:
        fromyear=WL.first_date.year;
    if not toyear:
        toyear=WL.last_date.year;
    ys=range(fromyear,toyear+1);
    
    sm=[];
    days=[];
    
    #-----aux function
    def toyeardays(date):
        return date.toordinal()-datetime.date(date.year,1,1).toordinal();
    #-----end
    
    for year in ys:
        thisyear=WL.get_time_window_dates(datetime.date(year,1,1),datetime.date(year,12,31));
        #----make this into a function if you ever make dates into day of the year again
        dayoneordinal=datetime.date(year,1,1).toordinal();
        thisyeardays=list(map(toyeardays,thisyear));
        
        #----up to here
        yeardata=tools.average_smoother(WL.get_time_window(datetime.date(year,1,1),datetime.date(year,12,31)),
                                        thisyear,
                                        smooth);
        days.append(thisyeardays);
        sm.append(yeardata);
    #animation
    fig, ax= plt.subplots();
    fig.set_size_inches(xfiguresize, yfiguresize)
    ax.set_xlim(0, 365);
    ax.set_ylim(580, 615);
    ax.set_xlabel("day of the year");
    ax.set_ylabel(f"water level ({WL.units})");
    ycounter=ax.text(160,610, '',fontsize=15);
    lines=plt.plot(days[0], sm[0], '.',[], [],'.');
    
    def init():
        ycounter.set_text(f"year: {ys[0]}");
        return lines[0],lines[1],ycounter;
    def update(frame):
        print(frame);
        ycounter.set_text(f"year: {frame}");
        lines[1].set_data(days[frame-fromyear], sm[frame-fromyear]);
        return lines[0],lines[1],ycounter;
    
    ani = FuncAnimation(fig, update,frames=ys,
                        interval=interval, repeat=False,
                        init_func=init, blit=True,
                        save_count=len(ys))
    #save animation
    if save:
        print(plt.rcParams['animation.ffmpeg_path']);
        ani.save(filename+"."+fileformat,bitrate=bitrate,dpi=dpi) #bitrate good quality around the 4000
    plt.show();
    return ani;

def averages(WL,smooth=2,empty_format=None, yeardata=None, units=None):
    ys=data.YearData.from_WL(WL);
    yearaverages=[];
    for year in ys.d:
        try:
            yearaverages.append(sum(ys.d[year][1])/len(ys.d[year][1]));
        except (ZeroDivisionError, TypeError):
            print("data at index {i} is very empty");
            yearaverages.append(None);
    #smooth            
    yearaverages=tools.average_smoother(yearaverages,m=smooth,empty_format=empty_format);
    #plot
    plt.figure();
    ax=plt.subplot();
    ax.set_xlabel("year");
    ax.set_ylabel(f"water level average ({WL.units})");
    plt.plot(range(ys.first_year, ys.last_year+1),yearaverages);
    plt.show();

def months(WL,smooth=0,empty_format=None, miss_days_tol=31):
    monthdata=[];
    initialyear=WL.first_date.year;
    endyear=WL.last_date.year;
    for month in range(1,12+1):
        monthdata.append(
            wal.TSFilter.get_month_from_years(WL,month,range(initialyear,endyear+1),miss_days_tol=miss_days_tol));
    monthaverages=[];
    numyears=len(monthdata[0]);
    novalueformat=620; #COLOR STRIPS FIX FORMAT
    for month in range(12):
        currentmonth=[];
        for year in range(numyears):
            total=0; n=0;
            for i in range(len(monthdata[month][year])):
                if monthdata[month][year][i]!=-1:
                    total= total+monthdata[month][year][i];
                    n=n+1;
            try:
                currentmonth.append(total/n);
            except ZeroDivisionError:
                currentmonth.append(novalueformat);#COLOR STRIPS FIX FORMAT
        monthaverages.append(currentmonth);
    #weird but fun thing #COLOR STRIPS FIX FORMAT
    plt.figure();
    plt.imshow(monthaverages); # add parameter: interpolation='bilinear' if I want average_smoother colors
    #let's plot every month in a single figure
    trashfig,ax=plt.subplots(nrows=6,ncols=2,sharex=True,sharey=True);
    ax[0][0].set_ylim(585, 615);
    for month in range(12):
        smonth=tools.average_smoother(monthaverages[month],m=smooth,empty_format=novalueformat);
        ax[month//2][month%2].plot( range(initialyear,endyear+1), smonth, marker='.')
    plt.show();
