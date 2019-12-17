from natl60 import *

ssh=NATL60_maps(datapath+"/maps/NATL60-CJM165_ssh_y2013.1y.nc")
ssh=(ssh.data.ssh[:,:,0]).values
np.savetxt(basepath+"/src/mask_subgrid1_natl60.txt",~np.isnan(ssh),fmt='%i')