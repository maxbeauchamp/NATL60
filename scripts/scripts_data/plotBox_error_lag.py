from natl60 import *
import netCDF4
import matplotlib.dates as mdates

file = netCDF4.Dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_5d.nc",'r')
ssh_obs = file.variables["ssh_obs"][:].data.astype('float64').flatten()
lag      = file.variables["lag"][:].data.astype('float64').flatten()
flag     = file.variables["flag"][:].flatten()
file2 = netCDF4.Dataset(datapath+"/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",'r')
ssh_mod = file2.variables["ssh"][:].data.astype('float64').flatten()

idx = ~np.isnan(ssh_obs)
ssh_obs = ssh_obs[idx]
ssh_mod = ssh_mod[idx]
err=ssh_obs-ssh_mod
lag = lag[idx]
flag = flag[idx]

idx= np.where(flag==0)[0]
ssh_obs = ssh_obs[idx]
ssh_mod = ssh_mod[idx]
err=ssh_obs-ssh_mod
lag = lag[idx]
flag = flag[idx]

dfr = pd.DataFrame(np.transpose(np.asarray([err,lag])),columns=['error','lag'])
boxprops = dict(linestyle='-', linewidth=1, color='k')
medianprops = dict(linestyle='-', linewidth=1, color='k')
fig, ax = plt.subplots(figsize=(10,7))
var= dfr.groupby("lag").error.agg(np.var)
var.index = np.arange(1,len(var)+1)
# fit variance=f(lag)
coeff = np.polyfit(np.unique(lag), var, 2)
fit = pd.Series(np.polyval(coeff, np.unique(lag)))
fit.index = np.arange(1,len(var)+1)
ax.plot(fit,'k-',linewidth=2,label=r"$\mathrm{\widehat{Var}}[y-Hx | lag]=f(lag)$")
ax.plot(var,'r--',linewidth=1.25,label=r"$\mathrm{Var}[y-Hx | lag]$")
# boxplot
bp = dfr.boxplot(column="error",by="lag", showfliers=False,\
boxprops=boxprops,medianprops=medianprops,ax=ax, rot=45) 
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::10])
ax.xaxis.set_ticklabels(ticklabels[::10])
ax.set_ylim([-0.25,0.25])
#ax.legend()
plt.title('')
fig.suptitle('')
plt.savefig(datapath+"/GULFSTREAM/data/boxplot_error_lag.pdf")
plt.close()






