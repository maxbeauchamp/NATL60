from natl60 import *

domain="GULFSTREAM2"
ssh=NATL60_maps(datapath+"/"+domain+"/maps/NATL60-CJM165_ssh_y2013.1y.nc").data.ssh.values[:,:,0]
np.savetxt(basepath+"/src/mask_"+domain+".txt",~np.isnan(ssh),fmt='%i')
