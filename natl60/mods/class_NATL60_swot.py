from .class_NATL60_data import *

class NATL60_swot(NATL60_data):
    ''' NATL60_swot class definition'''

    @staticmethod
    def preprocess(ds):
        ds.time.attrs['units'] = 'seconds since 2012-10-01'
        ds.time.attrs['calendar'] = 'standard'
        ds = xr.decode_cf(ds)
        for d in ds.dims:
            if d=="cycle":
                ds=ds.rename_dims({d:'nC'})
        ds = ds.stack(z=('nC', 'time'))
        return ds

    def __init__(self,list_files,dateref=None,type_err="wocor"):
        ''' '''
        NATL60_data.__init__(self )
        if len(list_files)>0:
            self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess)
            self.data = self.data.rename({'lon': 'longitude',\
                          'lat': 'latitude',\
                          'ssh_obs': 'ssh_obs',\
                          'ssh_model': 'ssh_mod'})
            self.data = self.data.dropna('z', how='all')
            # finalize
            self.extent=[np.min(convert_lon_360_180(self.data.longitude.values)),\
                     np.max(convert_lon_360_180(self.data.longitude.values)),\
                     np.min(self.data.latitude.values),np.max(self.data.latitude.values)]
            self.shape = tuple(self.data.dims[d] for d in ['z'])
            if len(list_files)==1:
                # no correlated SWOT obs errors if type_err=="wocor"
                if type_err=="wocor":
                    self.data.update({'ssh_obs':('z',\
                                   self.data.ssh_mod.values+self.data.karin_err.values)})
                # add lag variable
                lag = np.asarray( np.round( ( (self.data.time.values-np.datetime64(datetime.strptime(dateref,'%Y-%m-%d'))) / np.timedelta64(1, 's'))/(3600*24),1))
                self.data = self.data.update({'lag':('z',lag)})
                # add flag variable (nadir=0, swot=1)
                flag = np.repeat(1,len(self.data.time.values))
                self.data = self.data.update({'flag':('z',flag)})
        else:
            self.data=None
            self.shape = (0)
        self.gridded=False

    @classmethod
    def init2(cls,dateref,t1,t2,type_err):
        ''' '''
        t1_fmt=datetime.strptime(t1,'%Y-%m-%d')
        t2_fmt=datetime.strptime(t2,'%Y-%m-%d')    
        daterange = [datetime.strftime(t1_fmt + timedelta(days=x),"%Y-%m-%d") for x in range(0, (t2_fmt-t1_fmt).days+1)]
        list_files=[rawdatapath+"/data/swot/NATL60-CJM165_SWOT_"+t+"_1d.nc" for t in daterange if os.path.exists(rawdatapath+"/data/swot/NATL60-CJM165_SWOT_"+t+"_1d.nc")]
        return cls(list_files,dateref,type_err)

    def sel_spatial(self,extent):
        ''' '''
        index = np.where( (convert_lon_360_180(self.data.longitude.values) >= extent[0]) &\
                          (convert_lon_360_180(self.data.longitude.values) <= extent[1]) &\
                          (self.data.latitude.values >= extent[2]) &\
                          (self.data.latitude.values <= extent[3]) )[0]
        self.data = self.data.isel(z=index)

    def sel_time(self,t1,t2):
        ''' '''
        self.data = (self.data.unstack('z').sel(time=slice(t1,t2))).stack(z=('nC', 'time'))
        self.data = self.data.dropna('z', how='all')
        self.shape = tuple(self.data.dims[d] for d in ['z'])

    def convert2dailyNetCDF(self,path):
        ''' '''
        ldate = [datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
        daterange = np.sort(np.unique(ldate))
        for t in daterange:
            print(t)
            data_tmp = self.data.unstack('z').sel(time=slice(str(t),str(t)))
            print("ok...")
            data_tmp = data_tmp.rename({'longitude': 'lon',\
                                        'latitude': 'lat',\
                                        'ssh_obs': 'ssh_obs',\
                                        'ssh_mod': 'ssh_model'})
            new_time = [(x-np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') for x in data_tmp.time.values]
            data_tmp = data_tmp.assign(time=new_time)
            list_files = [path+'/'+file for file in os.listdir(path) if (t in file) ]
            N_file = len(list_files)
            new_file = path+"/NATL60-CJM165_SWOT_"+t+"_1d_N"+str(N_file)+".nc"
            mode_="w"
            data_tmp.to_netcdf(path=new_file,mode=mode_)


