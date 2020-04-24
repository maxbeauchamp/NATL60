from natl60 import *

file=sys.argv[1]
var=sys.argv[2]

map=NATL60_maps(file)
newval=map.data[var].values
n_lat=newval.shape[1]
n_lon=newval.shape[0]
# first & last column
newval[n_lon-1,:,:]=newval[n_lon-2,:,:]
newval[0,:,:]=newval[1,:,:]
# first & last line 
newval[:,n_lat-1,:]=newval[:,n_lat-2,:]
newval[:,0,:]=newval[:,1,:]        
newmap = xr.Dataset(\
               data_vars={var  : (('time','lat','lon'),newval.transpose(2,1,0))},\
               coords={'lon': map.data.longitude.values,\
                       'lat': map.data.latitude.values,\
                       'time': map.data.time.values})
del map 
newmap.to_netcdf(file,mode='w',unlimited_dims=["time"])
