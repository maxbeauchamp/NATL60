from .class_NATL60_data import *

class NATL60_swot(NATL60_data):
    ''' NATL60_swot class definition'''

    @staticmethod
    def preprocess(ds):
        ds.time.attrs['units'] = 'seconds since 2012-10-01'
        ds.time.attrs['calendar'] = 'standard'
        ds = xr.decode_cf(ds)
        ds = ds.stack(z=('nC', 'time'))
        return ds

    def __init__(self,list_files,dateref):
        ''' '''
        NATL60_data.__init__(self )
        if len(list_files)>0:
            self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess)
            self.data = self.data.rename({'lon': 'longitude',\
                          'lat': 'latitude',\
                          'ssh_obs': 'ssh_obs',\
                          'ssh_model': 'ssh_mod'})
            self.data = self.data.dropna('z', how='all')
            # add lag variable
            lag = np.asarray([ np.round( ( (x-np.datetime64(datetime.strptime(dateref,'%Y-%m-%d'))) / np.timedelta64(1, 's'))/(3600*24),1) \
                    for x in self.data.time.values])
            self.data = self.data.update({'lag':('z',lag)})
            # finalize
            self.extent=[np.min(convert_lon_360_180(self.data.longitude.values)),\
                     np.max(convert_lon_360_180(self.data.longitude.values)),\
                     np.min(self.data.latitude.values),np.max(self.data.latitude.values)]
            self.shape = tuple(self.data.dims[d] for d in ['z'])
        else:
            self.data=None
            self.shape = (0)
        self.gridded=False

    @classmethod
    def init2(cls,dateref,t1,t2):
        ''' '''
        t1_fmt=datetime.strptime(t1,'%Y-%m-%d')
        t2_fmt=datetime.strptime(t2,'%Y-%m-%d')    
        daterange = [datetime.strftime(t1_fmt + timedelta(days=x),"%Y-%m-%d") for x in range(0, (t2_fmt-t1_fmt).days+1)]
        list_files=[datapath+"/data/swot/NATL60-CJM165_SWOT_"+t+"_1d.nc" for t in daterange if os.path.exists(datapath+"/data/swot/NATL60-CJM165_SWOT_"+t+"_1d.nc")]
        return cls(list_files,dateref)

    def sel_time(self,t1,t2):
        ''' '''
        self.data = (self.data.unstack('z').sel(time=slice(t1,t2))).stack(z=('nC', 'time'))
        self.data = self.data.dropna('z', how='all')
        self.shape = tuple(self.data.dims[d] for d in ['z'])

    def convert2dailyNetCDF(self):
        ''' '''
        ldate = [datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
        daterange = np.sort(np.unique(ldate))
        for t in daterange:
            data_tmp = self.data.unstack('z').sel(time=slice(t,t))
            data_tmp = data_tmp.rename({'longitude': 'lon',\
                                        'latitude': 'lat',\
                                        'ssh_obs': 'ssh_obs',\
                                        'ssh_mod': 'ssh_model'})
            new_time = [(x-np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') for x in data_tmp.time.values]
            data_tmp = data_tmp.assign(time=new_time)
            new_file = datapath+"/data/swot/NATL60-CJM165_SWOT_"+t+"_1d.nc"
            if os.path.exists(new_file):
                mode_="a"
            else:
                mode_="w"
            data_tmp.to_netcdf(path=new_file,mode=mode_)


