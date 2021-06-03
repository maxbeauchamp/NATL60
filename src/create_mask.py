from natl60 import *

domain=sys.argv[1]

if domain=="OSMOSIS":
    extent=[-19.5,-11.5,45.,55.]
elif domain=='GULFSTREAM':
    extent=[-65.,-55.,33.,43.]
elif domain=='NATL':
    extent=[-79.,7.,27.,65.]
else:
    extent=[-65.,-55.,30.,40.]

sst=NATL60_maps(datapath+"/"+domain+"/ref/NATL60-CJM165_"+domain+"_sst_y2013.1y.nc").data.sst.values[:,:,1]
np.savetxt(basepath+"/src/mask_"+domain+".txt",~np.isnan(sst),fmt='%i')
