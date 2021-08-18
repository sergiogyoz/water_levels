import watlevpy.time_series as wal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot(WL=None,fromdate=-1,todate=-1, gtype=1): #plots WL from fromdate to todate
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
    plt.plot(ylabel=(f"water level {WL.units}"), xlabel=" date ");
    if gtype==1: plt.scatter(dates, wl ,marker=".");
    if gtype==2: plt.plot(dates,wl);
    if gtype==3: plt.plot(dates,wl,marker=".");
    if gtype==4: plt.scatter(dates,wl,marker="o")
    if gtype==5: plt.plot(dates,wl,marker="o")
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
    
    #histogram
    fig2,axs2=plt.subplots();
    plt.hist(WL.getwl(range(s,e+1)), edgecolor='#E6E6E6');
    axs2.set_xlabel(f"water level {WL.units}");
    axs2.set_axisbelow(True);
    plt.grid(color='#E6E6E6', linestyle='solid');
    
    plt.show();
    return fig1,axs1,fig2,axs2;
