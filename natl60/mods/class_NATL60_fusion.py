from .class_NATL60_data import *

class NATL60_fusion(NATL60_data):
 
    def __init__(self,nad,sw):
        ''' '''
        NATL60_data.__init__(self )
        # define fake nadir cycles to merge with swot data
        nad.data=nad.data.expand_dims('nC')
        _, index = np.unique(nad.data['time'], return_index=True)
        nad.data=nad.data.isel(time=index)
        nad.data=nad.data.stack(z=('nC', 'time'))
        if sw.data is not None:
            #self.data=xr.merge([sw.data,nad.data])
            self.data = xr.concat([sw.data[['longitude','latitude','ssh_obs','ssh_mod','lag','flag']],
                                   nad.data[['longitude','latitude','ssh_obs','ssh_mod','lag','flag']]],
                                   dim='z')
        else:
            self.data=nad.data
        if len(self.data.longitude)!=0:        
            self.extent=[np.min(convert_lon_360_180(self.data.longitude.values)),\
                         np.max(convert_lon_360_180(self.data.longitude.values)),\
                   np.min(self.data.latitude.values),np.max(self.data.latitude.values)]
            self.shape = tuple(self.data.dims[d] for d in ['z'])
        self.gridded=False

    def convert2dailyNetCDF(self,path,date,nadir_lag,swot_lag):
        ''' '''
        date1_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=-1*nadir_lag),"%Y-%m-%d")
        date2_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=nadir_lag),"%Y-%m-%d")
        data_tmp = self.data.unstack('z').sel(time=slice(date1_nadir,date2_nadir))
        data_tmp = data_tmp.rename({'longitude': 'lon',\
                                    'latitude': 'lat',\
                                    'ssh_obs': 'ssh_obs',\
                                    'ssh_mod': 'ssh_model'}) 
        new_time = (data_tmp.time.values-np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's')
        data_tmp = data_tmp.assign(time=new_time)
        if not os.path.exists(datapath+"/fusion"):
            mk_dir_recursive(datapath+"/fusion")  
        new_file = path+"/NATL60-CJM165_NADIR_SWOT_"+date+"_nadlag"+str(nadir_lag)+"d_swotlag"+str(swot_lag)+"d.nc"
        if os.path.exists(new_file):
            mode_="a"
        else:
            mode_="w"
        mode_="w"
        data_tmp.to_netcdf(path=new_file,mode=mode_)


