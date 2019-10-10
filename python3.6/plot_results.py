from netCDF4 import Dataset
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.cm as cm

# choose a stream
stream_id = 292364
year_list = []
f=[]
t=[]
t_datetime=[]
rivid=[]
n=[]
time_flow=[]
nc_folder_path = "/home/sherry/Downloads/erai_test/"
i=0

for j in range(1995, 2015):
    year_list.append(str(j))
    j=j+1

for i in range(0, 20):

    # get discharge
    nc_file_path = nc_folder_path + "Qout_streamflow"+year_list[i]+".nc"
    print(nc_file_path)
    f.append(Dataset(nc_file_path, "r"))
    t.append(f[i].variables["time"][:])
    t_datetime.append([dt.datetime.utcfromtimestamp(e) for e in t[i]])

    # get index of the stream
    rivid = f[i].variables["rivid"][:]
    n=np.argwhere(rivid==stream_id)[0][0]

    i = i + 1

#line plot daily data of every year in different colors
xs = np.arange(20)
ys = [i+xs+(i*xs)**2 for i in range(20)]
colors = cm.rainbow(np.linspace(0, 1, len(ys)))
days =np.arange(1,366)
for x, c in zip(xs, colors):
    plt.plot(days, f[x].variables["Qout"][0:365, n], color=c, label=year_list[x])

plt.xlabel('Time (month)')
plt.ylabel('Discharge(m3/s)')
# plt.xticks([0,31,59,90,120,151,181,212,243,273,304,334],labels=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
plt.xticks([15,46,74,105,135,166,196,227,258,288,319,349],labels=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
plt.legend(loc='upper left', ncol=2)
plt.show()

# line plot the average flow of every year
flow_mean_list=[]
flow_min_list=[]
flow_max_list = []
years=np.arange(1995,2015)
for x in range(0, 20):
    flow_mean_list.append(f[x].variables["Qout"][:, n].mean())
    flow_min_list.append(f[x].variables["Qout"][:, n].min())
    flow_max_list.append(f[x].variables["Qout"][:, n].max())
    x=x+1
plt.plot(years, flow_mean_list,'green', label="MEAN")
plt.xticks([1995,1997,1999,2001,2003,2005,2007,2009,2011,2013,2015])
# plt.plot(years, flow_min_list,'blue', label="MIN")
# plt.plot(years, flow_max_list,'red', label="MAX")

plt.xlabel('Time (year)')
plt.ylabel('Discharge(m3/s)')
plt.legend(loc='best')
plt.show()

# plot monthly average flow
Jan_mean_list=[]
Feb_mean_list=[]
Mar_mean_list=[]
Apr_mean_list=[]
May_mean_list=[]
Jun_mean_list=[]
Jul_mean_list=[]
Aug_mean_list=[]
Sep_mean_list=[]
Oct_mean_list=[]
Nov_mean_list=[]
Dec_mean_list=[]

for x in range(0, 20):
    Jan_mean_list.append(f[x].variables["Qout"][0:31, n].mean())
    Feb_mean_list.append(f[x].variables["Qout"][32:59, n].mean())
    Mar_mean_list.append(f[x].variables["Qout"][60:90, n].mean())
    Apr_mean_list.append(f[x].variables["Qout"][91:120, n].mean())
    May_mean_list.append(f[x].variables["Qout"][121:151, n].mean())
    Jun_mean_list.append(f[x].variables["Qout"][152:181, n].mean())
    Jul_mean_list.append(f[x].variables["Qout"][182:212, n].mean())
    Aug_mean_list.append(f[x].variables["Qout"][213:243, n].mean())
    Sep_mean_list.append(f[x].variables["Qout"][244:274, n].mean())
    Oct_mean_list.append(f[x].variables["Qout"][275:304, n].mean())
    Nov_mean_list.append(f[x].variables["Qout"][305:334, n].mean())
    Dec_mean_list.append(f[x].variables["Qout"][335:365, n].mean())
    x=x+1

xs = np.arange(12)
ys = [i+xs+(i*xs)**2 for i in range(12)]
colors = cm.rainbow(np.linspace(0, 1, len(ys)))
years=np.arange(1995,2015)

plt.plot(years,Jan_mean_list, color=colors[0], label='Jan')
plt.plot(years,Feb_mean_list, color=colors[1], label='Feb')
plt.plot(years,Mar_mean_list, color=colors[2], label='Mar')
plt.plot(years,Apr_mean_list, color=colors[3], label='Apr')
plt.plot(years,May_mean_list, color=colors[4], label='May')
plt.plot(years,Jun_mean_list, color=colors[5], label='Jun')
plt.plot(years,Jul_mean_list, color=colors[6], label='Jul')
plt.plot(years,Aug_mean_list, color=colors[7], label='Aug')
plt.plot(years,Sep_mean_list, color=colors[8], label='Sep')
plt.plot(years,Oct_mean_list, color=colors[9], label='Oct')
plt.plot(years,Nov_mean_list, color=colors[10], label='Nov')
plt.plot(years,Dec_mean_list, color=colors[11], label='Dec')
plt.xticks([1995,1997,1999,2001,2003,2005,2007,2009,2011,2013,2015])
#plt.yticks([0,2000,4000,6000,8000,10000,12000,14000,16000])

plt.xlabel('Time (year)')
plt.ylabel('Discharge(m3/s)')
plt.legend(loc='upper right', ncol=3)
plt.show()

