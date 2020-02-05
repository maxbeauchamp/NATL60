from pb_anda import *
import matplotlib.dates as mdates

file = netCDF4.Dataset(datapath+"/"+"data/dataset_nadir_5d.nc",'r')
ssh_obs = file.variables["ssh_obs"][:].data.astype('float64').flatten()
lag     = file.variables["lag"][:].data.astwhiskerpropsype('float64').flatten()

file2 = netCDF4.Dataset(datapath+"/"+"maps/NATL60-CJM165_ssh_y2013.1y.nc",'r')
ssh_mod = file2.variables["ssh"][:].data.astype('float64').flatten()

idx = ~np.isnan(ssh_obs)
ssh_obs = ssh_obs[idx]
ssh_mod = ssh_mod[idx]
err=ssh_obs-ssh_mod
lag = lag[idx]

dfr = pd.DataFrame(np.transpose(np.asarray([err,lag])),columns=['error','lag'])
boxprops = dict(linestyle='-', linewidth=1, color='k')
medianprops = dict(linestyle='-', linewidth=1, color='k')
fig, ax = plt.subplots(figsize=(10,7))
var= dfr.groupby("lag").error.agg(np.var)
var.index = np.arange(1,len(var)+1)
ax.plot(var,'r-')
bp = dfr.boxplot(column="error",by="lag", showfliers=False,\
boxprops=boxprops,medianprops=medianprops,ax=ax, rot=45) 
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::10])
ax.xaxis.set_ticklabels(ticklabels[::10])
ax.set_ylim([-0.25,0.25])
plt.title('')
fig.suptitle('')
plt.savefig(datapath+"/"+"data/boxplot_error_lag.pdf")
plt.close()




