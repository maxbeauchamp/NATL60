from natl60 import *

date="2013-04-03"
extent=[-65.,-55.,30.,40.]
yy=date[0:4]
mm=date[5:7]
dd=date[8:10]
natl60=NATL60_maps(datapath+"/maps/NATL60-CJM165_y"+yy+"m"+mm+"d"+dd+".1d_SSH.nc")
natl60.set_extent(extent)
natl60_regrid=natl60.regrid("ssh")
natl60_regrid.to_netcdf('/home3/datahome/mbeaucha/NATL60/test.nc')
natl60_regrid=NATL60_maps('/home3/datahome/mbeaucha/NATL60/test.nc')
natl60_regrid.plot('ssh','/home3/datahome/mbeaucha/NATL60/test.png')

