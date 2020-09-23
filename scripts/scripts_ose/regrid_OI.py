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

list_files = rawdatapath+"/OSE/maps_alg_h2g_j2g_j2n_j3_s3a_duacs/dt_upd_global_merged_2017_"+domain+"_10_10.nc"
OI=NATL60_maps(list_files,["ssh"],["ssh"])
OI.set_extent(extent)
OI_regrid=OI.regrid("ssh",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
if mask_file is not None:  
    mask = np.genfromtxt(mask_file).T
else:
    mask=np.ones(OI_regrid.ssh.shape[1:])
print(OI_regrid)
OI_regrid.assign({'mask': (('lat','lon'),mask)})
OI_regrid.to_netcdf(datapath+"/OSE/"+domain+'/training/oi/ssh_alg_h2g_j2g_j2n_j3_s3a_duacs.nc')
