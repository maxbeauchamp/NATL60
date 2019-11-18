from .class_NATL60 import *

class NATL60_nadir(NATL60):
    ''' NATL60_nadir class definition'''
     
    @staticmethod
    def preprocess(ds):
        ds.time.attrs['units'] = 'seconds since 2012-10-01'
        ds.time.attrs['calendar'] = 'standard'
        ds = xr.decode_cf(ds)
        return ds

    def __init__(self,list_files):
        ''' '''
        NATL60.__init__(self)
        if len(list_files)>0:
            self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess)
            self.data = self.data.rename({'lon': 'longitude',\
                          'lat': 'latitude',\
                          'time': 'time',\
                          'ssh_obs': 'ssh'})
            self.data['time']=np.sort(self.data['time'].values)
            self.data = self.data.dropna('time', how='any')
            self.extent=[np.min(convert_lon_360_180(self.data.longitude.values)),\
                     np.max(convert_lon_360_180(self.data.longitude.values)),\
                     np.min(self.data.latitude.values),np.max(self.data.latitude.values)]
            self.shape = tuple(self.data.dims[d] for d in ['time'])
        else:
            self.data=None
            self.shape = (0)
        self.gridded=False

    @classmethod
    def init2(cls,t1,t2):
        ''' '''
        t1_fmt=datetime.strptime(t1,'%Y-%m-%d')
        t2_fmt=datetime.strptime(t2,'%Y-%m-%d')    
        daterange = [datetime.strftime(t1_fmt + timedelta(days=x),"%Y-%m-%d") for x in range(0, (t2_fmt-t1_fmt).days+1)]
        list_files=[datapath+"/alongtracks/NATL60-CJM165_"+t+"_1d.nc" for t in daterange if os.path.exists(datapath+"/alongtracks/NATL60-CJM165_"+t+"_1d.nc")]
        return cls(list_files)

    def sel_time(self,t1,t2):
        ''' '''
        self.data = self.data.sel(time=slice(t1,t2))
        self.shape = tuple(self.data.dims[d] for d in ['time'])

    def convert2dailyNetCDF(self):
        ''' '''
        ldate = [datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
        daterange = np.sort(np.unique(ldate))
        for t in daterange:
            data_tmp = self.data.sel(time=slice(t,t))
            data_tmp = data_tmp.rename({'longitude': 'lon',\
                                         'latitude': 'lat',\
                                         'ssh': 'ssh_obs'}) 
            new_time = [(x-np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') for x in data_tmp.time.values]
            data_tmp = data_tmp.assign(time=new_time)
            new_file = datapath+"/alongtracks/NATL60-CJM165_"+t+"_1d.nc"
            if os.path.exists(new_file):
                mode_="a"
            else:
                mode_="w"
            data_tmp.to_netcdf(path=new_file,mode=mode_)

