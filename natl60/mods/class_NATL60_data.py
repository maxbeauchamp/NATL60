from .class_NATL60 import *

class NATL60_data(NATL60):                   
    ''' NATL60_data class definition '''

    def __init__(self):
        ''' '''
        NATL60.__init__(self)
        #super(NATL60_maps, self).__init__()
        
    def convert_on_grid(self,grid_file,mask_file,coord_grid=False):
        ''' '''
        # grid_file='/home/user/Bureau/NATL60/src/subgrid1_natl60.txt'
        # maskèfile='/home/user/Bureau/NATL60/src/mask_subgrid1_natl60.txt'

        # import lon and lat of the subdomain grid
        lon, lat = np.genfromtxt(grid_file).T
        mask = np.genfromtxt(mask_file)
        mesh_lon, mesh_lat = np.meshgrid(lon, lat)
        # time as string ('%Y-%m-%d')
        # time = [datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
        # time as number of days since 2012-10-01
        time = np.round(self.data.time.values/86400)
        time_u = np.sort(np.unique(time))
        ssh_obs = np.empty((len(lon),len(lat),len(time_u)))
        ssh_obs.fill(np.nan)
        ssh_mod = np.empty((len(lon),len(lat),len(time_u)))
        ssh_mod.fill(np.nan)
        # find nearest grid point from each datapoint 
        xi = np.searchsorted(lon,convert_lon_360_180(self.data.longitude.values)) 
        yi = np.searchsorted(lat,self.data.latitude.values)
        # convert for each time step
        days=np.asarray([ np.where( time_u == time[i] )[0][0] for i in range(0,len(self.data.longitude)) ])
        idx= np.where( (xi<len(lon)) & (yi<len(lat)) )
        ssh_obs[xi[idx], yi[idx], days[idx]]=self.data.ssh_obs.values[idx]
        ssh_mod[xi[idx], yi[idx], days[idx]]=self.data.ssh_mod.values[idx]
        # specify xarray arguments
        if coord_grid:
            data_on_grid = xr.Dataset(\
                        data_vars={'longitude': (('lat','lon'),mesh_lat),\
                                   'latitude' : (('lat','lon'),mesh_lon),\
                                   'Time'     : (('time'),time_u),\
                                   'mask'     : (('lat','lon'),mask),\
                                   'ssh_obs'  : (('time','lat','lon'),ssh_obs.transpose(2,1,0)),\
                                   'ssh_mod'  : (('time','lat','lon'),ssh_mod.transpose(2,1,0))},\
                        coords={'lon': lon,\
                                'lat': lat,\
                                'time': range(0,len(time_u))})
        else:
            data_on_grid = xr.Dataset(\
                        data_vars={'mask'     : (('lat','lon'),mask),\
                                   'ssh_obs'  : (('time','lat','lon'),ssh_obs.transpose(2,1,0)),\
                                   'ssh_mod'  : (('time','lat','lon'),ssh_mod.transpose(2,1,0))},\
                        coords={'lon': lon,\
                                'lat': lat,\
                                'time': time_u})
        data_on_grid.time.attrs['units']='days since 2012-10-01 00:00:00'
        return data_on_grid 
        

