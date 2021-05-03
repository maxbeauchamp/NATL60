from natl60 import *

domain=sys.argv[1]
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
if domain=="GULFSTREAM":
    extent=[-65.,-55.,33.,43.]
if domain=='NATL':
    extent=[-79.,7.,26.,65.]

var='H'
newvar='ssh'
file=rawdatapath+"/ref/1_10/natl60CH_D.nc"
newfile=datapath+"/"+domain+"/ref/"+"NATL60-CJM165_"+domain+"_ssh_y2013.1y.tmp.nc"
if not os.path.exists(datapath+"/"+domain+"/ref"):
    mk_dir_recursive(datapath+"/"+domain+"/ref")
map=xr.open_dataset(file)
ssh=map[var].values

# rebuild xarray 
newmap = xr.Dataset(\
               data_vars={newvar  : (('time','lat','lon'),ssh)},\
               coords={'lon': convert_lon_360_180(map.lon.values),\
                       'lat': map.lat.values,\
                       'time': map.time.values})
newmap.time.attrs['units'] = 'days since 2012-10-01 00:00:00'
newmap = newmap.sortby(["time","lat","lon"])
newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])
newmap.close()

# regrid xarray
map=NATL60_maps(newfile)
#map.sel_spatial([extent[0]-1,extent[1]+1,\
#                 extent[2]-1,extent[3]+1])
#map.set_extent(extent)
map.data.update({'time':(('time'),map.data.time.values+np.timedelta64(24*60*60,'s'))})
map_=map.regrid("ssh",\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
time= [ (np.datetime64(datetime.strptime("2012-10-01 12:00:00",'%Y-%m-%d %H:%M:%S')+timedelta(days=x))-\
        np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') for x in range (0,365)] 
map_.update({'time':(('time'),time)})
newmap.time.attrs['units'] = 'seconds since 2012-10-01 00:00:00'
os.remove(newfile)

# replace nans
newval=map_[newvar].values
newmap = xr.Dataset(\
               data_vars={newvar  : (('time','lat','lon'),newval)},\
               coords={'lon': map_.lon.values,\
                       'lat': map_.lat.values,\
                       'time': time})
newmap.time.attrs['units'] = 'seconds since 2012-10-01 00:00:00'
newfile=datapath+"/"+domain+"/ref/"+"NATL60-CJM165_"+domain+"_ssh_y2013.1y.nc"
newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])

