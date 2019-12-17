from natl60 import *

# OI from CLS (model-based) 
OI_mod_4nadir="oi/DUACS-OI_maps/ssh_model/ssh_sla_boost_NATL60_en_j1_tpn_g2.nc"
OI_mod_swot_4nadir="oi/DUACS-OI_maps/ssh_model/ssh_sla_boost_NATL60_swot_en_j1_tpn_g2.nc"
OI_mod_swot="oi/DUACS-OI_maps/ssh_model/ssh_sla_boost_NATL60_swot.nc"

# OI from CLS (obs-based i.e. model+err) 
OI_obs_4nadir="oi/DUACS-OI_maps/ssh_obs/ssh_sla_boost_NATL60_en_j1_tpn_g2.nc"
OI_obs_swot_4nadir="oi/DUACS-OI_maps/ssh_obs/ssh_sla_boost_NATL60_swot_en_j1_tpn_g2_karinerr-only.nc"
OI_obs_swot="oi/DUACS-OI_maps/ssh_obs/ssh_sla_boost_NATL60_swot_karinerr-only.nc"
extent=[-65.,-55.,30.,40.]

## 4NADIR
# mod
OI_mod=NATL60_maps(datapath+"/"+OI_mod_4nadir,["ssh"],["ssh_mod"])
OI_mod.set_extent(extent)
OI_mod_regrid=OI_mod.regrid("ssh_mod",mask_file=basepath+"/src/mask_subgrid1_natl60.txt",time_step="1D")
# obs
OI_obs=NATL60_maps(datapath+"/"+OI_obs_4nadir,["ssh"],["ssh_obs"])
OI_obs.set_extent(extent)
OI_obs_regrid=OI_obs.regrid("ssh_obs",mask_file=basepath+"/src/mask_subgrid1_natl60.txt",time_step="1D")
# merge
OI=xr.merge([OI_mod_regrid,OI_obs_regrid])
mask = np.genfromtxt(basepath+"/src/mask_subgrid1_natl60.txt").T
OI.assign({'mask': (('lat','lon'),mask)})
OI.to_netcdf(datapath+"/"+'oi/ssh_NATL60_4nadir.nc')

## 1SWOT
# mod
OI_mod=NATL60_maps(datapath+"/"+OI_mod_swot,["ssh"],["ssh_mod"])
OI_mod.set_extent(extent)
OI_mod_regrid=OI_mod.regrid("ssh_mod",mask_file=basepath+"/src/mask_subgrid1_natl60.txt",time_step="1D")
# obs
OI_obs=NATL60_maps(datapath+"/"+OI_obs_swot,["ssh"],["ssh_obs"])
OI_obs.set_extent(extent)
OI_obs_regrid=OI_obs.regrid("ssh_obs",mask_file=basepath+"/src/mask_subgrid1_natl60.txt",time_step="1D")
# merge
OI=xr.merge([OI_mod_regrid,OI_obs_regrid])
mask = np.genfromtxt(basepath+"/src/mask_subgrid1_natl60.txt").T
OI.assign({'mask': (('lat','lon'),mask)})
OI.to_netcdf(datapath+"/"+'oi/ssh_NATL60_swot.nc')

## 4NADIR + 1SWOT 
# mod
OI_mod=NATL60_maps(datapath+"/"+OI_mod_swot_4nadir,["ssh"],["ssh_mod"])
OI_mod.set_extent(extent)
OI_mod_regrid=OI_mod.regrid("ssh_mod",mask_file=basepath+"/src/mask_subgrid1_natl60.txt",time_step="1D")
# obs
OI_obs=NATL60_maps(datapath+"/"+OI_obs_swot_4nadir,["ssh"],["ssh_obs"])
OI_obs.set_extent(extent)
OI_obs_regrid=OI_obs.regrid("ssh_obs",mask_file=basepath+"/src/mask_subgrid1_natl60.txt",time_step="1D")
# merge
OI_mod_regrid.update({'time': OI_obs_regrid.time.values})
OI=xr.merge([OI_mod_regrid,OI_obs_regrid])
mask = np.genfromtxt(basepath+"/src/mask_subgrid1_natl60.txt").T
OI.assign({'mask': (('lat','lon'),mask)})
OI.to_netcdf(datapath+"/"+'oi/ssh_NATL60_swot_4nadir.nc')


