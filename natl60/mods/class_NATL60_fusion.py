from .class_NATL60 import *

class NATL60_fusion(NATL60):
 
    def __init__(self,nadir,swot):
        ''' '''
        NATL60.__init__(self )
        # define fake nadir cycles to merge with swot data
        nadir.data=nadir.data.drop('ncycle')
        nadir.data=nadir.data.expand_dims('nC')
        nadir.data=nadir.data.stack(z=('nC', 'time'))
        _, index = np.unique(nadir.data['z'], return_index=True)
        nadir.data=nadir.data.isel(z=index)
        if swot.data is not None:
            self.data=xr.merge([nadir.data,swot.data])
        else:
            self.data=nadir.data
        self.extent=[np.min(convert_lon_360_180(self.data.longitude.values)),\
                     np.max(convert_lon_360_180(self.data.longitude.values)),\
                     np.min(self.data.latitude.values),np.max(self.data.latitude.values)]
        self.gridded=False
        self.shape = tuple(self.data.dims[d] for d in ['z'])

    def convert2dailyNetCDF(self,date,nadir_lag):
        ''' '''
        date1_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=-1*nadir_lag),"%Y-%m-%d")
        date2_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=nadir_lag),"%Y-%m-%d")
        data_tmp = self.data.unstack('z').sel(time=slice(date1_nadir,date2_nadir))
        data_tmp = data_tmp.rename({'longitude': 'lon',\
                                        'latitude': 'lat',\
                                        'ssh': 'ssh_obs'}) 
        new_time = [(x-np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') for x in data_tmp.time.values]
        data_tmp = data_tmp.assign(time=new_time)
        if not os.path.exists(datapath+"/fusion"):
            mk_dir_recursive(datapath+"/fusion")  
        new_file = datapath+"/fusion/NATL60-CJM165_NADIR_SWOT_"+date+"_nadlag"+str(nadir_lag)+"d.nc"
        if os.path.exists(new_file):
            mode_="a"
        else:
            mode_="w"
        data_tmp.to_netcdf(path=new_file,mode=mode_)