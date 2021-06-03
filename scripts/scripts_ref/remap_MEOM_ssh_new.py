from natl60 import *

domain=sys.argv[1]
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
if domain=="GULFSTREAM":
    extent=[-65.,-55.,33.,43.]
if domain=='NATL':
    extent=[-79.,7.,27.,65.]

var='degraded_sossheig'
newvar='ssh'
file=rawdatapath+"/ref/NATL20-CJM165_y2012m10d01-y2013m09d30.1d_SSH-cdf.nc"
newfile=datapath+"/"+domain+"/ref/"+"NATL60-CJM165_"+domain+"_ssh_y2013.1y.tmp.nc"
if not os.path.exists(datapath+"/"+domain+"/ref"):
    mk_dir_recursive(datapath+"/"+domain+"/ref")
map=xr.open_dataset(file)
ssh=map[var].values

# rebuild xarray
newmap = xr.Dataset(\
               data_vars={newvar  : (('time_counter','y','x'),ssh),
                          'lat': (('y','x'),map.nav_lat.values),
                          'lon': (('y','x'),map.nav_lon.values)},\
               coords={'x': map.x.values,\
                       'y': map.y.values,\
                       'time_counter': map.time_counter.values})
newmap = newmap.rename({'time_counter': 'time'})
newmap = newmap.sortby(["time","y","x"])
newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])
newmap.close()

# regrid xarray
map=NATL60_maps(newfile)
map.data.update({'time':(('time'),map.data.time.values)})
map_=map.regrid(newvar,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D",
               curvilinear=True)
time= [ (np.datetime64(datetime.strptime("2012-10-01 12:00:00",'%Y-%m-%d %H:%M:%S')+timedelta(days=x))-\
        np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') for x in range (0,365)]
map_.update({'time':(('time'),time)})
newmap.time.attrs['units'] = 'seconds since 2012-10-01 00:00:00'
os.remove(newfile)

# replace nans
newval=map_[newvar].values
newmap = xr.Dataset(\
               data_vars={newvar  : (('time','lat','lon'),newval)},\
               coords={'lon': np.unique(np.sort(map_.lon.values)),\
                       'lat': np.unique(np.sort(map_.lat.values)),\
                       'time': time})
newfile=datapath+"/"+domain+"/ref/"+"NATL60-CJM165_"+domain+"_ssh_y2013.1y.nc"
newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])

