import watlevpy.time_series as wal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import watlevpy.stats.tools as tools
from matplotlib.animation import FuncAnimation
import datetime

#graphics ffmpeg path for animations
plt.rcParams['animation.ffmpeg_path']="./watlevpy/plot/ffmpeg-2021-07-04-essentials_build/bin/ffmpeg.exe";

def plotTS(WL=None,fromdate=-1,todate=-1, gtype=1,dataname="water levels"): #plots WL from fromdate to todate
    """
    Line plot of water levels time series and histogram from fromdate to todate. If no from or last date provided it
    will use the first and last date from WL. gtype from 1 to 5 to see different styles
    """
    
    WL=WL if WL else wal.TS();
    if(fromdate==-1): fromdate=WL.first_date;
    if(todate==-1): todate=WL.last_date;        
    dates=[];
    wl=[];
    try:
        s=WL.getindex(fromdate);
    except KeyError:
        s=wal.round_date(WL, fromdate,roundup=True);
        s=WL.getindex(s);
        dates.append(fromdate);
        wl.append(None);
        print("missing days at the beginning");
    missinglast=False;
    try:
        e=WL.getindex(todate);
    except KeyError:
        e=wal.round_date(WL, todate);
        e=WL.getindex(e);
        missinglast=True;
        print("missing days at the end");
    
    ndays=(todate-fromdate).days+1;
    dates.extend(WL.getdate(range(s,e+1)));
    wl.extend(WL.getwl(range(s,e+1)));
    if missinglast:
        dates.append(todate);
        wl.append(None);
    
    #dots curve
    fig1,axs1= plt.subplots()
    if gtype==1: axs1.scatter(dates, wl ,marker=".");
    if gtype==2: axs1.plot(dates,wl);
    if gtype==3: axs1.plot(dates,wl,marker=".");
    if gtype==4: axs1.scatter(dates,wl,marker="o")
    if gtype==5: axs1.plot(dates,wl,marker="o")
    locator=None;
    if ndays<36:
        locator=mdates.DayLocator(interval=7);
    elif ndays<130:
        locator=mdates.WeekdayLocator(interval=3);
    elif ndays<370:
        locator=mdates.MonthLocator(interval=2);
    else:
        locator=mdates.AutoDateLocator(maxticks=6);
    
    axs1.xaxis.set_major_locator(locator);
    axs1.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator));
    axs1.set_title(dataname+" series");
    axs1.set_ylabel(f"{dataname} ({WL.units})");
    axs1.set_xlabel(f" date ({WL.frequency}) ");
    
    #histogram
    fig2,axs2=plt.subplots();
    axs2.hist(WL.getwl(range(s,e+1)), edgecolor='#E6E6E6');
    axs2.set_xlabel(f"{dataname} ({WL.units})");
    axs2.set_axisbelow(True);
    axs2.set_ylabel("frequency");
    axs2.set_title(f"{dataname} distribution");
    axs2.grid(color='#E6E6E6', linestyle='solid');
    
    plt.show();
    return fig1,axs1,fig2,axs2;

class YearEvol:
        
    @staticmethod 
    def animate(WL,fromyear=None,toyear=None,smooth=2, save=False, interval=50 ,bitrate=100, dpi=100, filename="year_evol_animation",
                fileformat="mp4",yeardata=None, units="", xfiguresize=6.4, yfiguresize=4.8):
        """You need to save the return of this variable in order so see/save the animation, otherwise it will be trashed"""
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
            thisyeardays=list(map(toyeardays,thisyear));        
            #----
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
    
    #DEPRECATED use the average filter on yearly and plot it using simple.plot
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
        fig=plt.figure();
        plt.imshow(monthaverages); # add parameter: interpolation='bilinear' if I want average_smoother colors
        #let's plot every month in a single figure
        trashfig,ax=plt.subplots(nrows=6,ncols=2,sharex=True,sharey=True);
        ax[0][0].set_ylim(585, 615);
        for month in range(12):
            smonth=tools.average_smoother(monthaverages[month],m=smooth,empty_format=novalueformat);
            ax[month//2][month%2].plot( range(initialyear,endyear+1), smonth, marker='.')
        plt.show();
        return fig;
