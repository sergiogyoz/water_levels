import water_levels as wal
import matplotlib.pyplot as plt
import datetime

x=wal.WaterLevels.from_csvfile("MadeupData.csv");

x.plot(x.start_date,x.start_date+datetime.timedelta(days=180));
