from natl60 import *

domain=sys.argv[1]
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
if domain=="GULFSTREAM":
    extent=[-65.,-55.,33.,43.]

rawdatapath="/gpfswork/rech/yrf/rote001/NATL60/NATL60-CJM165-S/1d/W10-20-30-40-50-60m"

#for depth in ["10","20","30","40","50","60"]:
for depth in ["40","50","60"]:

    var='vovecrtz'
    newvar='vv'
    file=rawdatapath+"/NATL60-CJM165_y*.1d_vovecrtz_"+depth+"m.nc"
    print(file)
    newfile=datapath+"/"+domain+"/vv_depth/"+"NATL60-CJM165_"+domain+"_vv_"+depth+"_y2013.1y.tmp.nc"
    if not os.path.exists(datapath+"/"+domain+"/vv_depth"):
        mk_dir_recursive(datapath+"/"+domain+"/vv_depth")
    map = xr.open_mfdataset(file)
    map = map.squeeze(drop=True)
    vv=map[var].values

    # rebuild xarray 
    newmap = xr.Dataset(\
               data_vars={newvar  : (('time_counter','y','x'),vv),
                          'lat': (('y','x'),map.nav_lat.values[0]),
                          'lon': (('y','x'),map.nav_lon.values[0])},\
               coords={'x': map.x.values,\
                       'y': map.y.values,\
                       'time_counter': map.time_counter.values})
    #newmap.time.attrs['units'] = 'days since 2012-10-01 00:00:00'
    newmap = newmap.rename({'time_counter': 'time'})
    newmap = newmap.sortby(["time","y","x"])
    newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])
    newmap.close()

    # regrid xarray
    map=NATL60_maps(newfile)
    map.data.update({'time':(('time'),map.data.time.values+np.timedelta64(24*60*60,'s'))})
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
    #newmap.time.attrs['units'] = 'seconds since 2012-10-01 00:00:00'
    newfile=datapath+"/"+domain+"/vv_depth/"+"NATL60-CJM165_"+domain+"_vv_"+depth+"m_y2013.1y.nc"
    newmap.to_netcdf(newfile,mode='w',unlimited_dims=["time"])

