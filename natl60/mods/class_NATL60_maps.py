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

    def lap_diffusionMask(self,var,iter,lam,lamData=0.):
        '''@author: rfablet'''
        ## assume missing data are NaN
        ## I : image to be filtered
        ## iter : number of iterations of the diffusion
        ## lam : diffusion coefficient, It=lam . laplacian(I)
        ## lamData : weight for data-driven term, It=lam*(I-Init)
        debug = 0
        I = getattr(self.data,var).values[:,:,0]  
        Iinit = I
        lapI  = np.zeros((I.shape[0],I.shape[1],4))
        slapI = np.zeros((I.shape[0],I.shape[1]))
        for ii in range(0,iter):
            ## compute laplacian
            Ix           = I[1:,:]-I[0:-1,:]
            Iy           = I[:,1:]-I[:,0:-1]
            lapI[:,:,0]  = np.concatenate((-Ix[0:1,:],Ix),axis=0)
            lapI[:,:,1]  = np.concatenate((-Ix,Ix[I.shape[0]-2:,:]),axis=0)
            lapI[:,:,2]  = np.concatenate((-Iy[:,0:1],Iy),axis=1)
            lapI[:,:,3]  = np.concatenate((-Iy,Iy[:,I.shape[1]-2:]),axis=1)        
            slapI = np.nansum(lapI,axis=2) / (1e-10+np.nansum(1.0-np.isnan(lapI).astype(float),axis=2))
            I = I - lam * slapI + lamData * (Iinit - I)
        return I

