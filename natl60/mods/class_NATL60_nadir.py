from .class_NATL60_data import *
import re
import cftime

class NATL60_nadir(NATL60_data):
    ''' NATL60_nadir class definition'''
     
    @staticmethod
    def preprocess1(ds):
        ds = xr.decode_cf(ds)
        path=ds.encoding['source']
        # Change 0 as nan for the first cycles
        new_ssh_obs = np.where(ds.ssh_obs.values==0., np.nan, ds.ssh_obs.values)
        new_ssh_model = np.where(ds.ssh_model.values==0., np.nan, ds.ssh_model.values)
        ds = ds.update({'ssh_obs':('time',new_ssh_obs)})
        ds = ds.update({'ssh_model':('time',new_ssh_model)})
        # Change time
        nm_sat = ['en','j1','g2','tpn']
        timeshift = [22.10114,3.736615,15.08489,3.731883]
        index=[i for i in range(0,len(nm_sat)) \
               if re.search(nm_sat[i],path)][0]
        new_time = cftime.num2date(ds['time'].values - timeshift[index] * 24 * 3600,\
                                   units='second since 2012-10-01')
        ds['time'] = new_time
        ds = ds.drop('ncycle')
        ds.time.attrs['units'] = 'seconds since 2012-10-01'
        ds.time.attrs['calendar'] = 'standard'
        return ds

    @staticmethod
    def preprocess2(ds):
        ds.time.attrs['units'] = 'seconds since 2012-10-01'
        ds.time.attrs['calendar'] = 'standard'
        ds = xr.decode_cf(ds)
        return ds

    def __init__(self,list_files,dateref,preproc,extent=[-65,-55,30,40]):
        ''' '''
        # preproc: 1 or 2
        NATL60_data.__init__(self)
        if len(list_files)>0:
            if preproc==1:
                self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess1)
            if preproc==2:
                self.data = xr.open_mfdataset(list_files, preprocess=self.preprocess2)
            self.data = self.data.rename({'lon': 'longitude',\
                          'lat': 'latitude',\
                          'time': 'time',\
                          'ssh_obs': 'ssh_obs',\
                          'ssh_model': 'ssh_mod'})
            self.data = self.data.sortby('time')
            lvar=['longitude','latitude','x_al','model_index',\
                  'ssh_obs','ssh_mod']
            order = np.argsort(self.data.time.values)
            new_time = self.data.time.values[order]
            self.data['time'] = new_time
            for i in range(0,len(lvar)):
                self.data = self.data.update({lvar[i]:('time',self.data[lvar[i]].values[order])})
            if len(list_files)==1:
                # add lag variable
                lag = np.asarray([ np.round( ( (x-np.datetime64(datetime.strptime(dateref,'%Y-%m-%d'))) / np.timedelta64(1, 's'))/(3600*24),1) \
                    for x in self.data.time.values])
                self.data = self.data.update({'lag':('time',lag)})
                # add flag variable (nadir=0, swot=1)
                flag = np.repeat(0,len(self.data.time.values))
                self.data = self.data.update({'flag':('time',flag)})
            # finalize
            self.data = self.data.dropna('time', how='any')
            self.extent=extent
            self.shape = tuple(self.data.dims[d] for d in ['time'])
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
        list_files=[rawdatapath+"/data/alongtracks/NATL60-CJM165_"+t+"_1d.nc" for t in daterange if os.path.exists(rawdatapath+"/data/alongtracks/NATL60-CJM165_"+t+"_1d.nc")]
        return cls(list_files,dateref,2)

    def sel_time(self,t1,t2):
        ''' '''
        self.data = self.data.sel(time=slice(t1,t2))
        self.shape = tuple(self.data.dims[d] for d in ['time'])

    def convert2dailyNetCDF(self,path):
        ''' '''
        daterange = [datetime.strftime(datetime.strptime("2012-10-01","%Y-%m-%d") + timedelta(days=x),"%Y-%m-%d") for x in range (0,365)]
        for t in daterange:
            data_tmp = self.data.sel(time=slice(t,t))
            data_tmp = data_tmp.rename({'longitude': 'lon',\
                                        'latitude': 'lat',\
                                        'ssh_obs': 'ssh_obs',\
                                        'ssh_mod': 'ssh_model'})
            new_time = [(x-np.datetime64('2012-10-01T00:00:00Z')) / np.timedelta64(1, 's') for x in data_tmp.time.values]
            data_tmp = data_tmp.assign(time=new_time)
            new_file = path+"/NATL60-CJM165_"+t+"_1d.nc"
            if os.path.exists(new_file):
                mode_="a"
            else:
                mode_="w"
            mode_="w"
            data_tmp.to_netcdf(path=new_file,mode=mode_)



