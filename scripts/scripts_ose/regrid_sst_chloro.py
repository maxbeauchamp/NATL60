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

# regrid SST
list_files = rawdatapath+"/OSE/SST-Chloro/METOFFICE-GLO-SST-L4-REP-OBS-SST_1593762904880_"+domain+".nc"
data_sst=NATL60_maps(list_files,["analysed_sst"],["analysed_sst"])
data_sst.set_extent(extent)
data_sst=data_sst.regrid("analysed_sst",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
data_sst2=NATL60_maps(list_files,["analysis_error"],["analysis_error"])
data_sst2.set_extent(extent)
data_sst2=data_sst2.regrid("analysis_error",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
data_sst=xr.merge([data_sst,data_sst2])
if mask_file is not None:  
    mask = np.genfromtxt(mask_file).T
else:
    mask=np.ones((data_sst.analysed_sst.shape[1],data_sst.analysed_sst.shape[2]))
data_sst.assign({'mask': (('lat','lon'),mask)})
data_sst.to_netcdf(datapath+"/OSE/"+domain+'/training/oi/sst_CMEMS.nc')

# regrid Chloro
list_files = rawdatapath+"/OSE/SST-Chloro/dataset-oc-glo-chl-olci_a-l3-av_4km_daily-rt-v02_1593763414511_"+domain+".nc"
data_chloro=NATL60_maps(list_files,["CHL"],["CHL"])
data_chloro.set_extent(extent)
data_chloro.data = data_chloro.data.update({'time':data_sst.time.values})
data_chloro=data_chloro.regrid("CHL",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D",itrp="nearest_s2d")
data_chloro2=NATL60_maps(list_files,["CHL_flags"],["CHL_flags"])
data_chloro2.set_extent(extent)
data_chloro2.data = data_chloro2.data.update({'time':data_sst.time.values})
data_chloro2=data_chloro2.regrid("CHL_flags",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D",itrp="nearest_s2d")
data_chloro=xr.merge([data_chloro,data_chloro2])
if mask_file is not None:  
    mask = np.genfromtxt(mask_file).T
else:
    mask=np.ones((data_chloro.CHL.shape[1],data_chloro.CHL.shape[2]))
data_chloro.assign({'mask': (('lat','lon'),mask)})
data_chloro.to_netcdf(datapath+"/OSE/"+domain+'/training/data/chloro_CMEMS.nc')

