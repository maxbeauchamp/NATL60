from .class_NATL60 import *

class NATL60_maps(NATL60):
    ''' NATL60_map class definition '''

    def __init__(self,file):
        ''' '''
        NATL60.__init__(self)
        #super(NATL60_maps, self).__init__()
        self.data = xr.open_dataset(file)
        self.data = self.data.rename({'lon': 'longitude',\
                          'lat': 'latitude',\
                          'time': 'time',\
                          'sossheig': 'ssh'})
        self.data = self.data.transpose('longitude', 'latitude', 'time')
        self.extent=[np.min(self.data.longitude.values),np.max(self.data.longitude.values),\
                         np.min(self.data.latitude.values),np.max(self.data.latitude.values)]
        self.gridded=True
        self.shape = tuple(self.data.dims[d] for d in ['longitude', 'latitude', 'time'])

    def sel_time(self,t1,t2):
        ''' '''
        self.data = self.data.sel(time=slice(t1,t2))


