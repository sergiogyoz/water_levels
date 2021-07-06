import watlevpy.waterlevels.WaterLevels as wal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot(WL,fromdate=-1,todate=-1): #plots WL from fromdate to todate
    """
    Line plot of water levels time series and histogram from fromdate to todate. If no from or last date provided it
    will use the first and last date from WL.
    """
    
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
    
    plt.figure(1);
    axs=plt.subplot(2,1,1,ylabel=(f"water level {WL.units}"), xlabel=" date ");
    plt.scatter(dates, wl ,marker=".");
    locator=None;
    if ndays<36:
        locator=mdates.DayLocator(interval=7);
    elif ndays<130:
        locator=mdates.WeekdayLocator(interval=3);
    elif ndays<370:
        locator=mdates.MonthLocator(interval=2);
    else:
        locator=mdates.AutoDateLocator(maxticks=6);
    axs.xaxis.set_major_locator(locator);
    axs.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator));
    plt.subplot(2,1,2,xlabel=f"water level {WL.units}");
    plt.hist(WL.getwl(range(s,e+1)));
    plt.show();
