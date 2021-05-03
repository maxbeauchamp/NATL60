from natl60 import *

def regrid_datasets(nadir_lag,domain):

    if domain=="OSMOSIS":
        extent=[-19.5,-11.5,45.,55.]
        mask_file=None
    elif domain=='GULFSTREAM':
        extent=[-65.,-55.,33.,43.]
        mask_file=None
    elif domain=='NATL':
        extent=[-79.,7.,26.,65.]
        mask_file=basepath+"/src/mask_"+domain+".txt"
    else: 
        extent=[-65.,-55.,30.,40.]
        mask_file=basepath+"/src/mask_"+domain+".txt"

    N_filter=[3,5,10]
    N_filter=[]

    daterange = [datetime.strftime(datetime.strptime("2012-10-01","%Y-%m-%d") + timedelta(days=x),"%Y-%m-%d")\
                 for x in range (0,10)]
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
        swot=NATL60_swot.init2(date,date,date,type_err="wocor")
        # fusion nadir/swot
        nadir_swot=NATL60_fusion(nadir,swot)
        #nadir.data=nadir.data.expand_dims('nC')
        nadir.data = nadir.data.unstack('z')
        _, index = np.unique(nadir.data['time'], return_index=True)
        nadir.data=nadir.data.isel(time=index)
        nadir.data=nadir.data.stack(z=('nC', 'time'))
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
            for N in N_filter:
                nadir.data = nadir.data.assign({"ssh_filtered_N"+str(N): (('nc','time'),np.empty((1,1)))})
            nadir.data=nadir.data.stack(z=('nC', 'time'))
        if len(nadir.data.longitude)!=1:
            for N in N_filter:
                # create filtered data
                nadir.filtering(N)

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
            for N in N_filter:
                swot.data = swot.data.assign({"ssh_filtered_N"+str(N): (('nc','time'),np.empty((1,1)))})
            swot.data=swot.data.stack(z=('nC', 'time'))
        if len(swot.data.longitude)!=1:
            for N in N_filter:
                # create filtered data
                swot.filtering(N)

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
            for N in N_filter:
                nadir_swot.data = nadir_swot.data.assign({"ssh_filtered_N"+str(N): (('nc','time'),np.empty((1,1)))})
            nadir_swot.data=nadir_swot.data.stack(z=('nC', 'time'))
        if len(nadir_swot.data.longitude)!=1:
            for N in N_filter:
                # create filtered data
                nadir_swot.filtering(N)

        # add anomaly variables to dataset
        OI=NATL60_maps(datapath+"/"+domain+"/oi/ssh_NATL60_4nadir.nc")
        nadir.anomaly(OI,"ssh_mod","ssh_mod","anomaly_mod")
        nadir.anomaly(OI,"ssh_obs","ssh_obs","anomaly_obs")
        swot.anomaly(OI,"ssh_mod","ssh_mod","anomaly_mod")
        swot.anomaly(OI,"ssh_obs","ssh_obs","anomaly_obs")
        nadir_swot.anomaly(OI,"ssh_mod","ssh_mod","anomaly_mod")
        nadir_swot.anomaly(OI,"ssh_obs","ssh_obs","anomaly_obs")

        print('toto1')

        # conversion on grid
        # modifications of time values to force unique time values after regridding
        new_time = [(np.datetime64(datetime.strptime(date,'%Y-%m-%d') + timedelta(seconds=dt))-\
                     np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') \
                     for dt in np.linspace(0,0.99,len(nadir.data.unstack('z').time)) ]
        print('toto2')
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
    mk_dir_recursive(datapath+"/"+domain+'/data/gridded_data_swot_wocorr')
    Gnadir.to_netcdf(path=datapath+"/"+domain+'/data/gridded_data_swot_wocorr/dataset_nadir_'+str(nadir_lag)+'d.nc',mode="w",unlimited_dims=["time"])
    Gswot.to_netcdf(path=datapath+"/"+domain+'/data/gridded_data_swot_wocorr/dataset_swot.nc',mode="w",unlimited_dims=["time"])
    Gnadir_swot.to_netcdf(path=datapath+"/"+domain+'/data/gridded_data_swot_wocorr/dataset_nadir_'+str(nadir_lag)+'d_swot.nc',mode="w",unlimited_dims=["time"])

# regrid for nadir_lag = 0 to 5
domain = sys.argv[1]
regrid_datasets(0,domain)
#regrid_datasets(1,domain)
#regrid_datasets(2,domain)
#regrid_datasets(3,domain)
#regrid_datasets(4,domain)
#regrid_datasets(5,domain)
