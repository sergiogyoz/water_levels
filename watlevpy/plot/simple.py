import watlevpy.time_series as wal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot(WL=None,fromdate=-1,todate=-1, gtype=1,dataname="water levels"): #plots WL from fromdate to todate
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
