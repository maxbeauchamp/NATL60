from natl60 import *

domain='OSMOSIS'
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
else:
    extent=[-65.,-55.,33.,43.]

var='sossheig'
newvar='ssh'
file=datapath+"/"+domain+"/REF/NATL60"+domain+"_2012-10-01_2013-09-30.1d.nc"
newfile=datapath+"/"+domain+"/REF/"+"NATL60-CJM165_"+domain+"_ssh_y2013.1y.tmp.nc"
map=xr.open_dataset(file)
ssh=map[var].values
# rebuild xarray 
newmap = xr.Dataset(\
               data_vars={newvar  : (('time','lat','lon'),ssh)},\
               coords={'lon': convert_lon_360_180(np.sort(np.unique(map.nav_lon))),\
                       'lat': np.sort(np.unique(map.nav_lat)),\
                       'time': map.time.values})
newmap.time.attrs['units'] = 'seconds since 1958-01-01 00:00:00'
newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])
newmap.close()
# regrid xarray
map=NATL60_maps(newfile)
map.set_extent(extent)
map.data.update({'time':(('time'),map.data.time.values-np.timedelta64(29*60+52,'s'))})
map_=map.regrid("ssh",\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
time= [datetime.strftime(datetime.strptime("2012-10-01","%Y-%m-%d") \
       +timedelta(days=x),"%Y-%m-%d") for x in range (0,365)]  
map_.update({'time':(('time'),time)})
map_.time.attrs['units']='days since 2012-10-01'
os.remove(newfile)
# replace nans
newval=map_[newvar].values
n_lat=newval.shape[1]
n_lon=newval.shape[2]
# first & last line 
newval[:,n_lat-1,:]=newval[:,n_lat-2,:]
newval[:,0,:]=newval[:,1,:]   
# first & last column
newval[:,:,n_lon-1]=newval[:,:,n_lon-2]
newval[:,:,0]=newval[:,:,1]
newmap = xr.Dataset(\
               data_vars={newvar  : (('time','lat','lon'),newval)},\
               coords={'lon': map_.lon.values,\
                       'lat': map_.lat.values,\
                       'time': time})
newmap.time.attrs['units']='days since 2012-10-01 00:00:00'
newfile=datapath+"/"+domain+"/REF/"+"NATL60-CJM165_"+domain+"_ssh_y2013.1y.nc"
newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])

