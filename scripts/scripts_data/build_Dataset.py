from natl60 import *

nadir_lag=int(sys.argv[1])
domain="GULFSTREAM"
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
    mask_file=None
elif domain=='GULFSTREAM':
    extent=[-65.,-55.,33.,43.]
    mask_file=None
else: 
    extent=[-65.,-55.,30.,40.]
    mask_file=basepath+"/src/mask_"+domain+".txt"

if __name__ == '__main__':

    daterange = [datetime.strftime(datetime.strptime("2012-10-01","%Y-%m-%d") + timedelta(days=x),"%Y-%m-%d")\
                 for x in range (0,365)]
    for i in range(0,len(daterange)):
        print(i)
        date=daterange[i]
        # read nadir
        date1_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") \
                    + timedelta(days=-1*nadir_lag),"%Y-%m-%d")
        date2_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d")\
                    + timedelta(days=nadir_lag),"%Y-%m-%d")
        nadir=NATL60_nadir.init2(date,date1_nadir,date2_nadir)
        nadir.sel_spatial(extent)     
        # read swot
        swot=NATL60_swot.init2(date,domain,date,date,"wocor")
        # fusion nadir/swot
        nadir_swot=NATL60_fusion(nadir,swot)
        if len(nadir.data.longitude)==0:
            # create empty swot dataset 
            time_u = (np.datetime64(datetime.strptime(date,'%Y-%m-%d'))-\
                     np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's')
            nadir.data=xr.Dataset(\
                        data_vars={'longitude': (('nC','time'),np.empty((1,1))),\
                                   'latitude' : (('nC','time'),np.empty((1,1))),\
                                   'lag'      : (('nC','time'),np.empty((1,1))),\
                                   'flag'      : (('nC','time'),np.empty((1,1))),\
                                   'ssh_obs'      : (('nC','time'),np.empty((1,1))),\
                                   'ssh_mod'      : (('nC','time'),np.empty((1,1)))},\
                        coords={'nC':[0],'time': [time_u]})
            nadir.data=nadir.data.stack(z=('nC', 'time'))
        if swot.data is None:
            # create empty swot dataset 
            time_u = (np.datetime64(datetime.strptime(date,'%Y-%m-%d'))-\
                     np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's')
            swot.data=xr.Dataset(\
                        data_vars={'longitude': (('nC','time'),np.empty((1,1))),\
                                   'latitude' : (('nC','time'),np.empty((1,1))),\
                                   'lag'      : (('nC','time'),np.empty((1,1))),\
                                   'flag'      : (('nC','time'),np.empty((1,1))),\
                                   'ssh_obs'      : (('nC','time'),np.empty((1,1))),\
                                   'ssh_mod'      : (('nC','time'),np.empty((1,1)))},\
                        coords={'nC':[0],'time': [time_u]})
            swot.data=swot.data.stack(z=('nC', 'time'))
        if len(nadir_swot.data.longitude)==0:
            # create empty swot dataset 
            time_u = (np.datetime64(datetime.strptime(date,'%Y-%m-%d'))-\
                     np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's')
            nadir_swot.data=xr.Dataset(\
                        data_vars={'longitude': (('nC','time'),np.empty((1,1))),\
                                   'latitude' : (('nC','time'),np.empty((1,1))),\
                                   'lag'      : (('nC','time'),np.empty((1,1))),\
                                   'flag'      : (('nC','time'),np.empty((1,1))),\
                                   'ssh_obs'      : (('nC','time'),np.empty((1,1))),\
                                   'ssh_mod'      : (('nC','time'),np.empty((1,1)))},\
                        coords={'nC':[0],'time': [time_u]})
            nadir_swot.data=nadir_swot.data.stack(z=('nC', 'time'))
        # add anomaly variables to dataset
        OI=NATL60_maps(datapath+"/"+domain+"/oi/ssh_NATL60_4nadir.nc")
        nadir.anomaly(OI,"ssh_mod","ssh_mod","anomaly_mod")
        nadir.anomaly(OI,"ssh_obs","ssh_obs","anomaly_obs")
        swot.anomaly(OI,"ssh_mod","ssh_mod","anomaly_mod")
        swot.anomaly(OI,"ssh_obs","ssh_obs","anomaly_obs")
        nadir_swot.anomaly(OI,"ssh_mod","ssh_mod","anomaly_mod")
        nadir_swot.anomaly(OI,"ssh_obs","ssh_obs","anomaly_obs")

        # conversion on grid
        # modifications of time values to force unique time values after regridding
        new_time = [(np.datetime64(datetime.strptime(date,'%Y-%m-%d') + timedelta(seconds=dt))-\
                     np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') \
                     for dt in np.linspace(0,0.99,len(nadir.data.unstack('z').time)) ]
        nadir.data = (nadir.data.unstack('z').assign(time=new_time)).stack(z=('nC', 'time'))
        nadir=nadir.convert_on_grid(mask_file,\
                                    lon_bnds=(extent[0],extent[1]+0.05,0.05),\
                                    lat_bnds=(extent[2],extent[3]+0.05,0.05))
        # modifications of time values to force unique time values after regridding
        new_time = [(np.datetime64(datetime.strptime(date,'%Y-%m-%d') + timedelta(seconds=dt))-\
                     np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') \
                     for dt in np.linspace(0,0.99,len(swot.data.unstack('z').time)) ]
        swot.data = (swot.data.unstack('z').assign(time=new_time)).stack(z=('nC', 'time'))
        swot=swot.convert_on_grid(mask_file,\
                                    lon_bnds=(extent[0],extent[1]+0.05,0.05),\
                                    lat_bnds=(extent[2],extent[3]+0.05,0.05))
        # modifications of time values to force unique time values after regridding
        new_time = [(np.datetime64(datetime.strptime(date,'%Y-%m-%d') + timedelta(seconds=dt))-\
                     np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') \
                     for dt in np.linspace(0,0.99,len(nadir_swot.data.unstack('z').time)) ]
        nadir_swot.data = (nadir_swot.data.unstack('z').assign(time=new_time)).stack(z=('nC', 'time'))
        nadir_swot=nadir_swot.convert_on_grid(mask_file,\
                                    lon_bnds=(extent[0],extent[1]+0.05,0.05),\
                                    lat_bnds=(extent[2],extent[3]+0.05,0.05))
        # concatenation along time
        if i != 0:
            Gnadir=xr.concat([Gnadir,nadir],dim='time',data_vars='minimal')    
            Gswot=xr.concat([Gswot,swot],dim='time',data_vars='minimal')    
            Gnadir_swot=xr.concat([Gnadir_swot,nadir_swot],dim='time',data_vars='minimal')    
        else:
            Gnadir=nadir
            Gswot=swot
            Gnadir_swot=nadir_swot
    # write in file ()
    Gnadir.to_netcdf(path=datapath+"/"+domain+'/data/gridded_data_swot_wocorr/dataset_nadir_'+str(nadir_lag)+'d.nc',mode="w",unlimited_dims=["time"])
    Gswot.to_netcdf(path=datapath+"/"+domain+'/data/gridded_data_swot_wocorr/dataset_swot.nc',mode="w",unlimited_dims=["time"])
    Gnadir_swot.to_netcdf(path=datapath+"/"+domain+'/data/gridded_data_swot_wocorr/dataset_nadir_'+str(nadir_lag)+'d_swot.nc',mode="w",unlimited_dims=["time"])
