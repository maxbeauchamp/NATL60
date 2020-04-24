from natl60 import *

# OI from CLS (model-based) 
OI_mod_4nadir="DUACS-OI_maps/ssh_model/ssh_sla_boost_NATL60_en_j1_tpn_g2.nc"
OI_mod_swot_4nadir="DUACS-OI_maps/ssh_model/ssh_sla_boost_NATL60_swot_en_j1_tpn_g2.nc"
OI_mod_swot="DUACS-OI_maps/ssh_model/ssh_sla_boost_NATL60_swot.nc"

# OI from CLS (obs-based i.e. model+err) 
OI_obs_4nadir="DUACS-OI_maps/ssh_obs/ssh_sla_boost_NATL60_en_j1_tpn_g2.nc"
OI_obs_swot_4nadir="DUACS-OI_maps/ssh_obs/ssh_sla_boost_NATL60_swot_en_j1_tpn_g2_karinerr-only.nc"
OI_obs_swot="DUACS-OI_maps/ssh_obs/ssh_sla_boost_NATL60_swot_karinerr-only.nc"

domain='OSMOSIS'
if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
    mask_file=None
elif domain=='GULFSTREAM':
    extent=[-65.,-55.,33.,43.]
    mask_file=None
else: 
    extent=[-65.,-55.,30.,40.]
    mask_file=basepath+"/src/mask_"+domain+".txt"

## 4NADIR
# mod
OI_mod=NATL60_maps(rawdatapath+"/"+OI_mod_4nadir,["ssh"],["ssh_mod"])
OI_mod.set_extent(extent)
OI_mod_regrid=OI_mod.regrid("ssh_mod",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
OI_obs=NATL60_maps(rawdatapath+"/"+OI_obs_4nadir,["ssh"],["ssh_obs"])
OI_obs.set_extent(extent)
OI_obs_regrid=OI_obs.regrid("ssh_obs",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
# merge
OI=xr.merge([OI_mod_regrid,OI_obs_regrid])
if mask_file is not None:  
    mask = np.genfromtxt(mask_file).T
else:
    mask=np.ones(OI_mod.data.ssh_mod.shape)
OI.assign({'mask': (('lat','lon'),mask)})
OI.to_netcdf(datapath+"/"+domain+'/oi/ssh_NATL60_4nadir.nc')

## 1SWOT
# mod
OI_mod=NATL60_maps(rawdatapath+"/"+OI_mod_swot,["ssh"],["ssh_mod"])
OI_mod.set_extent(extent)
OI_mod_regrid=OI_mod.regrid("ssh_mod",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
# obs
OI_obs=NATL60_maps(rawdatapath+"/"+OI_obs_swot,["ssh"],["ssh_obs"])
OI_obs.set_extent(extent)
OI_obs_regrid=OI_obs.regrid("ssh_obs",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
# merge
OI=xr.merge([OI_mod_regrid,OI_obs_regrid])
mask = np.genfromtxt(basepath+"/src/mask_"+domain+".txt").T
OI.assign({'mask': (('lat','lon'),mask)})
OI.to_netcdf(datapath+"/"+domain+'/oi/ssh_NATL60_swot.nc')

## 4NADIR + 1SWOT 
# mod
OI_mod=NATL60_maps(rawdatapath+"/"+OI_mod_swot_4nadir,["ssh"],["ssh_mod"])
OI_mod.set_extent(extent)
OI_mod_regrid=OI_mod.regrid("ssh_mod",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
# obs
OI_obs=NATL60_maps(rawdatapath+"/"+OI_obs_swot_4nadir,["ssh"],["ssh_obs"])
OI_obs.set_extent(extent)
OI_obs_regrid=OI_obs.regrid("ssh_obs",mask_file=mask_file,\
               lon_bnds=(extent[0],extent[1]+0.05,0.05),\
               lat_bnds=(extent[2],extent[3]+0.05,0.05), time_step="1D")
# merge
OI_mod_regrid.update({'time': OI_obs_regrid.time.values})
OI=xr.merge([OI_mod_regrid,OI_obs_regrid])
mask = np.genfromtxt(basepath+"/src/mask_"+domain+".txt").T
OI.assign({'mask': (('lat','lon'),mask)})
OI.to_netcdf(datapath+"/"+domain+'/oi/ssh_NATL60_swot_4nadir.nc')


