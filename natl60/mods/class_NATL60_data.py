from .class_NATL60 import *

class NATL60_data(NATL60):                   
    ''' NATL60_data class definition '''

    def __init__(self):
        ''' '''
        NATL60.__init__(self)
        #super(NATL60_maps, self).__init__()

    def filtering(self,N):
        ''' compute filtered SSH version '''

        self.data = self.data.unstack('z')
        filter_val_obs = np.zeros(len(self.data.sat.values))
        filter_val_mod = np.zeros(len(self.data.sat.values))
        for sat in np.unique(self.data.sat.values):
            idsat = np.where(self.data.sat.values == sat)[0]
            nn = [ np.argsort(np.abs(self.data.time.values[idsat] - time))[:2*N] \
                    for time in self.data.time.values[idsat] ]
            filter_val_obs[idsat] = [ np.nanmean(self.data.ssh_obs.values[idsat[idtime]]) for idtime in nn ]
            filter_val_mod[idsat] = [ np.nanmean(self.data.ssh_mod.values[idsat[idtime]]) for idtime in nn ]
        # add filtered value
        self.data = self.data.stack(('nC','time'))
        self.data = self.data.assign({"ssh_obs_filtered_N"+str(N): (('z'),filter_val_obs) })
        self.data = self.data.assign({"ssh_mod_filtered_N"+str(N): (('z'),filter_val_mod) })

    def convert_on_grid(self,date,mask_file=None,lon_bnds=(-65,-54.95,0.05),lat_bnds=(30,40.05,0.05),coord_grid=False, N_filter=None):
        ''' '''

        def mm(ix, iy, X):
            df = pd.DataFrame({'ix': ix,
                   'iy': iy,
                   'X': X},
                    columns=['ix', 'iy', 'X'])
            df = df.groupby(['ix', 'iy'])
            ix = np.asarray(list(df.groups)).T[0]
            iy = np.asarray(list(df.groups)).T[1]
            return ix, iy, np.asarray(df.mean()['X'])

        # mask_file='/home/user/Bureau/NATL60/src/mask_subgrid1_natl60.txt'
        # create lon and lat of the subdomain grid
        lon_min,lon_max,lon_step=lon_bnds
        lon = np.arange(lon_min, lon_max, lon_step)
        lat_min,lat_max,lat_step=lat_bnds
        lat = np.arange(lat_min, lat_max, lat_step)
        # import maskfile
        if mask_file is not None:
            mask = np.genfromtxt(mask_file).T
        else:
            mask = np.ones((len(lat),len(lon)))
        mesh_lat, mesh_lon = np.meshgrid(lat, lon)
        # time as number of days since 2012-10-01
        td = datetime.strptime(date,'%Y-%m-%d')\
             -datetime.strptime("2012-10-01",'%Y-%m-%d')
        time_u    = [td.days]
        lag     = np.empty((len(lon),len(lat),len(time_u))) ; lag.fill(np.nan)
        flag    = np.empty((len(lon),len(lat),len(time_u))) ; flag.fill(np.nan)
        ssh_obs = np.empty((len(lon),len(lat),len(time_u))) ; ssh_obs.fill(np.nan)
        ssh_mod = np.empty((len(lon),len(lat),len(time_u))) ; ssh_mod.fill(np.nan)
        #sat = np.empty((len(lon),len(lat),len(time_u)),dtype=object) ; sat.fill(np.nan)
        #anomaly_obs = np.empty((len(lon),len(lat),len(time_u))) ; anomaly_obs.fill(np.nan)
        #anomaly_mod = np.empty((len(lon),len(lat),len(time_u))) ; anomaly_mod.fill(np.nan)
        # find nearest grid point from each datapoint 
        xi = np.searchsorted(lon,convert_lon_360_180(self.data.longitude.values)) 
        yi = np.searchsorted(lat,self.data.latitude.values)
        # convert for each time step
        days = np.repeat([0],len(self.data.longitude))
        idx = np.where( (xi<len(lon)) & (yi<len(lat)) & (~np.isnan(self.data.ssh_obs.values)))[0]
        if len(idx)>1:
            ix, iy, lag_ = mm(xi[idx], yi[idx], self.data.lag.values[idx])
            lag[ix, iy, 0] = lag_
            ix, iy, flag_ = mm(xi[idx], yi[idx], self.data.flag.values[idx])
            flag[ix,iy,0] = flag_
            ix, iy, ssh_obs_ = mm(xi[idx], yi[idx], self.data.ssh_obs.values[idx])
            ssh_obs[ix,iy,0]= ssh_obs_
            ix, iy, ssh_mod_ = mm(xi[idx], yi[idx], self.data.ssh_mod.values[idx])
            ssh_mod[ix,iy,0]= ssh_mod_
            #anomaly_obs[xi[idx], yi[idx], 0]=self.data.anomaly_obs.values[idx]
            #anomaly_mod[xi[idx], yi[idx], 0]=self.data.anomaly_mod.values[idx]
        # specify xarray arguments
        if coord_grid:
            data_on_grid = xr.Dataset(\
                        data_vars={'longitude': (('lat','lon'),mesh_lon),\
                                   'latitude' : (('lat','lon'),mesh_lat),\
                                   'Time'     : (('time'),time_u),\
                                   'mask'     : (('lat','lon'),mask),\
                                   'lag'      : (('time','lat','lon'),lag.transpose(2,1,0)),\
                                   'flag'      : (('time','lat','lon'),flag.transpose(2,1,0)),\
                                   'ssh_obs'  : (('time','lat','lon'),ssh_obs.transpose(2,1,0)),\
                                   'ssh_mod'  : (('time','lat','lon'),ssh_mod.transpose(2,1,0))},\
                                   #'sat'      : (('time','lat','lon'),sat.transpose(2,1,0)),\
                                   #'anomaly_obs'  : (('time','lat','lon'),anomaly_obs.transpose(2,1,0)),\
                                   #'anomaly_mod'  : (('time','lat','lon'),anomaly_mod.transpose(2,1,0))},\
                        coords={'lon': lon,\
                                'lat': lat,\
                                'time': range(0,len(time_u))})
        else:
            data_on_grid = xr.Dataset(\
                        data_vars={'mask'     : (('lat','lon'),mask),\
                                   'lag'      : (('time','lat','lon'),lag.transpose(2,1,0)),\
                                   'flag'     : (('time','lat','lon'),flag.transpose(2,1,0)),\
                                   'ssh_obs'  : (('time','lat','lon'),ssh_obs.transpose(2,1,0)),\
                                   'ssh_mod'  : (('time','lat','lon'),ssh_mod.transpose(2,1,0))},\
                                   #'sat'      : (('time','lat','lon'),sat.transpose(2,1,0)),\
                                   #'anomaly_obs'  : (('time','lat','lon'),anomaly_obs.transpose(2,1,0)),\
                                   #'anomaly_mod'  : (('time','lat','lon'),anomaly_mod.transpose(2,1,0))},\
                        coords={'lon': lon,\
                                'lat': lat,\
                                'time': time_u})

        if N_filter is not None:
            for N in N_filter:
                ssh_obs_filter = np.empty((len(longitude),len(latitude),len(time_u)),dtype=object) ; ssh_obs_filter.fill(np.nan)
                ssh_obs_filter[xi[idx], yi[idx], days[idx]]=self.data["ssh_obs_filtered_N"+str(N)].values[idx]
                data_on_grid = data_on_grid.assign({"ssh_obs_filtered_N"+str(N): (('time','lat','lon'),ssh_obs_filter.transpose(2,1,0)) })
                ssh_mod_filter = np.empty((len(longitude),len(latitude),len(time_u)),dtype=object) ; ssh_mod_filter.fill(np.nan)
                ssh_mod_filter[xi[idx], yi[idx], days[idx]]=self.data["ssh_mod_filtered_N"+str(N)].values[idx]
                data_on_grid = data_on_grid.assign({"ssh_mod_filtered_N"+str(N): (('time','lat','lon'),ssh_mod_filter.transpose(2,1,0)) })
                        
        data_on_grid.time.attrs['units']='days since 2012-10-01 00:00:00'
        return data_on_grid 

    def anomaly(self,OI,nmvar1,nmvar2,newvar):
        ''' compute anomaly: data-OI '''

        # bilinear interpolation of OI on data locations
        lats_OI = np.sort(np.unique(OI.data.latitude.values))
        lons_OI = np.sort(np.unique(OI.data.longitude.values))
        time_OI = np.sort(np.unique(OI.data.time.values)).astype("float")
        f3d = RegularGridInterpolator( (time_OI,lats_OI,lons_OI), OI.data[nmvar2].values.transpose(2,1,0),\
                                      bounds_error=False, fill_value=np.nan)
        n_pts=len(self.data.time.values)
        pts = np.asarray(list(zip(self.data.time.values.astype("float"),\
                                  self.data.latitude.values,\
                                  convert_lon_360_180(self.data.longitude.values))))
        interpOI = f3d(pts)
        # remove large-scale OI 
        self.data = self.data.assign({newvar: (('z'),np.reshape(self.data[nmvar1].values-interpOI,n_pts)) })
        

