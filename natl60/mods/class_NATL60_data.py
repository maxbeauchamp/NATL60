from .class_NATL60 import *

class NATL60_data(NATL60):                   
    ''' NATL60_data class definition '''

    def __init__(self):
        ''' '''
        NATL60.__init__(self)
        #super(NATL60_maps, self).__init__()
        
    def convert_on_grid(self,grid_file):
        ''' '''
        # grid_file='/home/user/Bureau/NATL60/src/subgrid1_natl60.txt'
        # import lon and lat of the subdomain grid
        lon, lat = np.genfromtxt(grid_file).T
        mesh_lon, mesh_lat = np.meshgrid(lon, lat)
        time = [datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
        time_u = np.sort(np.unique(time))
        ssh = np.empty((len(lon),len(lat),len(time_u)))
        ssh.fill(np.nan)
        # find nearest grid point from each datapoint 
        xi = np.searchsorted(lon,convert_lon_360_180(self.data.longitude.values)) 
        yi = np.searchsorted(lat,self.data.latitude.values)
        # convert for each time step
        for i in range(0,len(self.data.longitude)):
            day = np.where( time_u == time[i] )[0][0]
            if ( (xi[i]<len(lon)) & (yi[i]<len(lat)) ):
                ssh[ xi[i], yi[i], day] = self.data.ssh.values[i]
        # specify xarray arguments
        data_on_grid = xr.Dataset(\
                        data_vars={'longitude': (('lat','lon'),mesh_lat),\
                                   'latitude' : (('lat','lon'),mesh_lon),\
                                   'Time'     : (('time'),time_u),\
                                   'ssh'      : (('time','lat','lon'),ssh.transpose(2,1,0))},\
                        coords={'lon': lon,\
                                'lat': lat,\
                                'time': range(0,len(time_u))})
        return data_on_grid 
        
