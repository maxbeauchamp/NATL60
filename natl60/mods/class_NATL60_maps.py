from .class_NATL60 import *

class NATL60_maps(NATL60):
    ''' NATL60_map class definition '''

    def __init__(self,file,var=None,new_var=None):
        ''' '''
        NATL60.__init__(self)
        #super(NATL60_maps, self).__init__()
        self.data = xr.open_dataset(file)
        dimnames = list(self.data.dims.keys())
        if 'lon' in dimnames:
            self.data = self.data.rename({'lon': 'longitude',\
                          'lat': 'latitude',\
                          'time': 'time'})
        else:
            self.data = self.data.rename({'x': 'longitude',\
                          'y': 'latitude',\
                          'time': 'time'})
        if var is not None:
            for i in range(0,len(var)):
                self.data = self.data.rename({var[i] : new_var[i]})
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

    def regrid(self,var,mask_file,lon_bnds=(-65,-54.95,0.05),lat_bnds=(30,40.05,0.05),time_step=None):
        ''' regrid from curvilinear or rectangular grid to rectangular grid'''
        # time_step="1D"

        ## output_grid parameters
        # longitude
        lon_min,lon_max,lon_step=lon_bnds
        vlon = np.arange(lon_min, lon_max, lon_step)
        # latitude
        lat_min,lat_max,lat_step=lat_bnds
        vlat = np.arange(lat_min, lat_max, lat_step)
        # import maskfile
        mask = np.genfromtxt(mask_file).T
        ## Rename some variables for internal regridding 
        ds = self.data
        ds = ds.rename({'longitude': 'lon', 'latitude': 'lat'})
        ds = ds.transpose('time','lat','lon')
        dr = ds[[var]]
        ## Generate new xarray Datasets
        ds_out    = xr.Dataset({'lat': (['lat'], vlat),\
                                'lon': (['lon'], vlon)})
        regridder = xe.Regridder(ds, ds_out, 'bilinear')#, periodic=True, reuse_weights=True)
        dr_regridded = regridder(dr)
        if len(self.data.time.values)>1:
            # time
            time_fmt=[datetime.strftime(datetime.utcfromtimestamp(x.astype('O')/1e9),'%Y-%m-%d') for x in self.data.time.values]
            time_min = min(time_fmt)
            time_max = max(time_fmt)
            vtime = pd.date_range(time_min, time_max, freq=time_step)
            dr_out = dr_regridded.chunk(dr_regridded.sizes).interp(time=vtime)
        else:
            dr_out=dr_regridded
        # put values where mask==1 to nan
        newval=dr_out[var].values
        newval[:,np.where(mask==False)[0],np.where(mask==False)[1]]=np.nan
        print(newval.shape)
        dr_out.update({var: (('time','lat','lon'),newval)})
        regridder.clean_weight_file()
        del dr_regridded ; del ds ; del dr
        return dr_out
