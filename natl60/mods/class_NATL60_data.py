from .class_NATL60 import *

class NATL60_data(NATL60):                   
    ''' NATL60_data class definition '''

    def __init__(self):
        ''' '''
        NATL60.__init__(self)
        #super(NATL60_maps, self).__init__()
        
    def convert_on_grid(self,mask_file=None,lon_bnds=(-65,-54.95,0.05),lat_bnds=(30,40.05,0.05),coord_grid=False):
        ''' '''
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
        # time as string ('%Y-%m-%d')
        # time = [datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
        # time as number of days since 2012-10-01
        time    = np.round(self.data.time.values/86400)
        time_u  = np.sort(np.unique(time))
        lag     = np.empty((len(lon),len(lat),len(time_u))) ; lag.fill(np.nan)
        flag     = np.empty((len(lon),len(lat),len(time_u))) ; flag.fill(np.nan)
        ssh_obs = np.empty((len(lon),len(lat),len(time_u))) ; ssh_obs.fill(np.nan)
        ssh_mod = np.empty((len(lon),len(lat),len(time_u))) ; ssh_mod.fill(np.nan)
        anomaly_obs = np.empty((len(lon),len(lat),len(time_u))) ; anomaly_obs.fill(np.nan)
        anomaly_mod = np.empty((len(lon),len(lat),len(time_u))) ; anomaly_mod.fill(np.nan)
        # find nearest grid point from each datapoint 
        xi = np.searchsorted(lon,convert_lon_360_180(self.data.longitude.values)) 
        yi = np.searchsorted(lat,self.data.latitude.values)
        # convert for each time step
        days=np.asarray([ np.where( time_u == time[i] )[0][0] for i in range(0,len(self.data.longitude)) ])
        idx= np.where( (xi<len(lon)) & (yi<len(lat)) )
        lag[xi[idx], yi[idx], days[idx]]=self.data.lag.values[idx]
        flag[xi[idx], yi[idx], days[idx]]=self.data.flag.values[idx]
        ssh_obs[xi[idx], yi[idx], days[idx]]=self.data.ssh_obs.values[idx]
        ssh_mod[xi[idx], yi[idx], days[idx]]=self.data.ssh_mod.values[idx]
        anomaly_obs[xi[idx], yi[idx], days[idx]]=self.data.anomaly_obs.values[idx]
        anomaly_mod[xi[idx], yi[idx], days[idx]]=self.data.anomaly_mod.values[idx]
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
                                   'ssh_mod'  : (('time','lat','lon'),ssh_mod.transpose(2,1,0)),\
                                   'anomaly_obs'  : (('time','lat','lon'),anomaly_obs.transpose(2,1,0)),\
                                   'anomaly_mod'  : (('time','lat','lon'),anomaly_mod.transpose(2,1,0))},\
                        coords={'lon': lon,\
                                'lat': lat,\
                                'time': range(0,len(time_u))})
        else:
            data_on_grid = xr.Dataset(\
                        data_vars={'mask'     : (('lat','lon'),mask),\
                                   'lag'      : (('time','lat','lon'),lag.transpose(2,1,0)),\
                                   'flag'      : (('time','lat','lon'),flag.transpose(2,1,0)),\
                                   'ssh_obs'  : (('time','lat','lon'),ssh_obs.transpose(2,1,0)),\
                                   'ssh_mod'  : (('time','lat','lon'),ssh_mod.transpose(2,1,0)),\
                                   'anomaly_obs'  : (('time','lat','lon'),anomaly_obs.transpose(2,1,0)),\
                                   'anomaly_mod'  : (('time','lat','lon'),anomaly_mod.transpose(2,1,0))},\
                        coords={'lon': lon,\
                                'lat': lat,\
                                'time': time_u})
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
        

