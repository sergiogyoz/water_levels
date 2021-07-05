import water_levels as wal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

#path for ffmpeg for the animation save/recording to work
plt.rcParams['animation.ffmpeg_path']="./ffmpeg-2021-07-04-essentials_build/bin/ffmpeg.exe"


WL=wal.WaterLevels.from_csvfile(csvfile="DubuqueIA.csv",headers=True,dateformat="%m/%d/%Y %H:%M");

#Extracting dates as int indices with their corresponding values
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


#smoother method
def smoother(values, continuity_indices=[], m=0, empty_format=None): 
    """
    returns an array of smoother values using the average of the 2m+1 values center around each value. It makes an average
    of those avaliable if there are missing values
    """   
    if len(continuity_indices)==0:
        #work with values, so holes are in the values array as empty format e.g. 2,5,None,3,...
        newvalues=[None]*len(values);
        for i in range(len(values)):
            s=0; n=0;
            for k in range(-m,m+1):
                try:
                    if values[i+k] != empty_format:
                        s=s+values[i+k];
                        n=n+1;
                except IndexError:
                    pass; #left/right limits
            try:
                newvalues[i]=s/n;
            except (ZeroDivisionError, TypeError):
                newvalues[i]=None; #we could also just pass but... lets not
        return newvalues;
    else:
        if len(values)!=len(continuity_indices) : raise ValueError(f"values and indices are not the same size: {len(values)} and {len(continuity_indices)}");
        newvalues=[0]*len(values);
        #work with indices, so holes are differences of indices values e.g. 1,2,4,...
        for i in range(len(continuity_indices)):
            s=0; n=0;
            for k in range(-m,m+1):
                try:
                    if continuity_indices[i+k]==continuity_indices[i]+k:
                        s=s+values[i+k];
                        n=n+1;
                except IndexError:
                    pass; #left/right limits
            newvalues[i]=s/n;
        return newvalues;
                    

#do I want to smooch the curve?
smoothcurve=True;
if(smoothcurve): 
    sm=[]; 
    m1=2; #smoothness parameter
    for year in range(len(ys)):
        yeardata=smoother(ys[year][1],ys[year][0],m1);
        sm.append([ys[year][0],yeardata]);    
    ys=sm;


#animation of wl data evolution along the year
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
                    interval=50, repeat=False,
                    init_func=init, blit=True,
                    save_count=143)
#save animation
#ani.save("wholeRange.mp4",bitrate=100) #bitrate good quality around the 4000

#Year averages
yearaverages=[];
for i in range(len(ys)):
    try:
        yearaverages.append(sum(ys[i][1])/len(ys[i][1]));
    except (ZeroDivisionError, TypeError):
        print("data at index {i} is very empty");
        yearaverages.append(None);

 
#do I wanna smooth?
smoothaverages=True;
if(smoothaverages): 
    m2=2; #smoothness parameter
    yearaverages=smoother(yearaverages,m=m2,empty_format=None);

plt.figure();
ax2=plt.subplot();
ax2.set_ylim(587, 600);
ax2.set_xlabel("year");
ax2.set_ylabel(f"water level average ({WL.units})");
plt.plot(range(WL.first_date.year, WL.first_date.year+len(yearaverages)),yearaverages);


#From monthly data now
monthdata=[];
for month in range(1,12+1):
    monthdata.append( 
        wal.WaterLevels.get_month_from_years(WL, 
                                             month, 
                                             range(initialyear,WL.last_date.year),
                                             miss_days_tol=16) 
        );
    
monthaverages=[];
ny=len(monthdata[0]);
novalueformat=620;
for month in range(12):
    currentmonth=[];
    for year in range(ny):
        total=0; n=0;
        for i in range(len(monthdata[month][year])):
            if monthdata[month][year][i]!=-1:
                total= total+monthdata[month][year][i];
                n=n+1;
        try:
            currentmonth.append(total/n);
        except ZeroDivisionError:
            currentmonth.append(novalueformat);
    monthaverages.append(currentmonth);

#weird but fun thing
plt.figure();
plt.imshow(monthaverages); # add parameter: interpolation='bilinear' if I want smoother colors

#let's plot every month in a single figure
trashfig,ax3=plt.subplots(nrows=6,ncols=2,sharex=True,sharey=True);
ax3[0][0].set_ylim(585, 615);
for month in range(12):
    ax3[month//2][month%2].plot(
        range(initialyear, WL.first_date.year+len(monthaverages[month])+1),
        smoother(monthaverages[month],m=0,empty_format=novalueformat),
        marker='.'
        )



plt.show()