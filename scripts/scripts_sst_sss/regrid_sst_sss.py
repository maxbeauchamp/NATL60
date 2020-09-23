from natl60 import *

domain='GULFSTREAM'
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
    mask_file=None
elif domain=='GULFSTREAM':
    extent=[-65.,-55.,33.,43.]
    mask_file=None
else: 
    extent=[-65.,-55.,30.,40.]
    mask_file=basepath+"/src/mask_"+domain+".txt"

path = rawdatapath+"/SST_SSS/"+domain
list_files = [ path+'/'+file for file in os.listdir(path) ]
list_files_sst = [ list_files[i]  for i in range(len(list_files)) if "sosstsst" in list_files[i] ]
list_files_sss = [ list_files[i]  for i in range(len(list_files)) if "sosaline" in list_files[i] ]

# SST
data_sst=NATL60_maps(list_files_sst,['sosstsst'],['sst']) 
data_sst.data = data_sst.data.update({'time':data_sst.data.time_counter.values})
order = np.argsort(data_sst.data.time.values)
new_time = data_sst.data.time.values[order]
data_sst.data['time'] = new_time
data_sst.data = data_sst.data.update({'sst':(('x','y','time'),data_sst.data['sst'].values[:,:,order])})
data_sst.data = data_sst.data.rename({'longitude': 'x', 'latitude':'y'})
data_sst.data = data_sst.data.rename({'nav_lon': 'longitude', 'nav_lat':'latitude'})
#data_sst.data = data_sst.data.update({'lon': (('x','y'),data_sst.data.nav_lon.values)})
#data_sst.data = data_sst.data.update({'lat': (('x','y'),data_sst.data.nav_lat.values)})
data_sst.set_extent(extent)
data_sst_regrid=data_sst.regrid("sst",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D",curvilinear=True)
if mask_file is not None:  
    mask = np.genfromtxt(mask_file).T
else:
    mask=np.ones(data_sst_regrid.sst.shape[-1:])
#data_sst_regrid.assign({'mask': (('y','x'),mask)})
data_sst_regrid = data_sst_regrid.rename({'lat': 'latitude', 'lon':'longitude'})
data_sst_regrid = data_sst_regrid.rename_dims({'y': 'lat', 'x':'lon'})
data_sst_regrid = data_sst_regrid.update({'lon':(('lon'),np.sort(np.unique(data_sst_regrid.longitude.values)))})
data_sst_regrid = data_sst_regrid.update({'lat':(('lat'),np.sort(np.unique(data_sst_regrid.latitude.values)))})
data_sst_regrid = data_sst_regrid.drop_vars({'longitude','latitude'})
data_sst_regrid.to_netcdf(datapath+"/"+domain+'/ref/NATL60-CJM165_'+domain+'_sst_y2013.1y.nc')

# SSS
data_sss=NATL60_maps(list_files_sss,['sosaline'],['sss']) 
data_sss.data = data_sss.data.update({'time':data_sss.data.time_counter.values})
order = np.argsort(data_sss.data.time.values)
new_time = data_sss.data.time.values[order]
data_sss.data['time'] = new_time
data_sss.data = data_sss.data.update({'sss':(('x','y','time'),data_sss.data['sss'].values[:,:,order])})
data_sss.data = data_sss.data.rename({'longitude': 'x', 'latitude':'y'})
data_sss.data = data_sss.data.rename({'nav_lon': 'longitude', 'nav_lat':'latitude'})
#data_sss.data = data_sss.data.update({'lon': (('x','y'),data_sss.data.nav_lon.values)})
#data_sss.data = data_sss.data.update({'lat': (('x','y'),data_sss.data.nav_lat.values)})
data_sss.set_extent(extent)
data_sss_regrid=data_sss.regrid("sss",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D",curvilinear=True)
if mask_file is not None:  
    mask = np.genfromtxt(mask_file).T
else:
    mask=np.ones(data_sss_regrid.sss.shape[-1:])
#data_sss_regrid.assign({'mask': (('y','x'),mask)})
data_sss_regrid = data_sss_regrid.rename({'lat': 'latitude', 'lon':'longitude'})
data_sss_regrid = data_sss_regrid.rename_dims({'y': 'lat', 'x':'lon'})
data_sss_regrid = data_sss_regrid.update({'lon':(('lon'),np.sort(np.unique(data_sss_regrid.longitude.values)))})
data_sss_regrid = data_sss_regrid.update({'lat':(('lat'),np.sort(np.unique(data_sss_regrid.latitude.values)))})
data_sss_regrid = data_sss_regrid.drop_vars({'longitude','latitude'})
data_sss_regrid.to_netcdf(datapath+"/"+domain+'/ref/NATL60-CJM165_'+domain+'_sss_y2013.1y.nc')



