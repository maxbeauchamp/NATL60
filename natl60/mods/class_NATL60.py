from natl60 import *

class NATL60:
    ''' NATL60 class definition'''

    def __init__(self):
        ''' '''
        self.cmap="coolwarm"
        self.extent=[-80,0,25,65]

    def sel_spatial(self,extent):
        ''' '''
        index = np.where( (convert_lon_360_180(self.data.longitude.values) >= extent[0]) &\
                          (convert_lon_360_180(self.data.longitude.values) <= extent[1]) &\
                          (self.data.latitude.values >= extent[2]) &\
                          (self.data.latitude.values <= extent[3]) )[0]
        self.data = self.data.isel(time=index)

    def gpd_fmt(self):
        ''' import via pandas and convert in geopandas '''
        if self.gridded:
            lon,lat=np.meshgrid(self.data.longitude,self.data.latitude)
            df = pd.DataFrame({'Lon': lon.flatten(),'Lat': lat.flatten(),\
                               'Time': np.repeat(self.data.time,np.prod(self.shape[0:2])),\
                               'Ssh_obs': self.data.ssh_obs.values.flatten(),\
                               'Ssh_mod': self.data.ssh_mod.values.flatten()})          
        else:
            df = pd.DataFrame({'Lon': self.data.longitude,'Lat': self.data.latitude,\
                               'Time': self.data.time, 'Ssh_obs': self.data.ssh_obs,\
                               'Ssh_mod': self.data.ssh_mod})
        gdf = gpd.GeoDataFrame(df, crs={'init' :'epsg:4326'}, \
                       geometry=[shapely.geometry.Point(xy) for xy in zip(df.Lon, df.Lat)])
        return gdf

    def set_extent(self,extent):
        ''' '''
        self.extent=extent

    def set_colormap(self, cmap):
        ''' '''
        self.cmap=cmap
    
    def plot(self,var,file):
        ''' '''
        gdf = self.gpd_fmt()
        minx, miny, maxx, maxy = gdf.geometry.total_bounds
        fig, ax = make_map(self.extent)
        data=getattr(self.data,var)
        if self.gridded:
            lon2=(gdf.centroid.x).values.reshape(self.shape[0:2],order='F')
            lat2=(gdf.centroid.y).values.reshape(self.shape[0:2],order='F')
            im=ax.pcolormesh(lon2, lat2, data.values[:,:,0], cmap=self.cmap,\
                          vmin=-2, vmax=2,edgecolors='face', alpha=1, \
                          transform= ccrs.PlateCarree(central_longitude=0.0))
        else:
            lon2=(gdf.centroid.x).values
            lat2=(gdf.centroid.y).values
            im=ax.scatter(lon2, lat2, c=data.values, cmap=self.cmap, s=1,\
                       vmin=-2, vmax=2,edgecolors='face', alpha=1, \
                       transform= ccrs.PlateCarree(central_longitude=0.0)) 
        im.set_clim(-2,2)
        clb = fig.colorbar(im, orientation="horizontal", extend='both', pad=0.1)
        clb.ax.set_title('SSH (meters)')
        plt.savefig(file, bbox_extra_artists=(clb))
        plt.close()
