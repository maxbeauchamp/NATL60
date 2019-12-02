from natl60 import *
date="2013-04-03"
extent=[-65.,-55.,30.,40.]
yy=date[0:4]
mm=date[5:7]
dd=date[8:10]
natl60=NATL60_maps(datapath+"/maps/NATL60-CJM165_y"+yy+"m"+mm+"d"+dd+".1d_SSH.nc") 
natl60.set_extent(extent)
test=natl60.data.ssh.values[:,:,0]-natl60.lap_diffusionMask("ssh",250,.1,lamData=0.)

grad_HR = np.sqrt(np.gradient(natl60.data.ssh.values[:,:,0],axis=0)**2+np.gradient(natl60.data.ssh.values[:,:,0],1,axis=1)**2)
grad_LR = np.sqrt(np.gradient(test,axis=0)**2+np.gradient(test,1,axis=1)**2)
plt.close()
fig, (ax1, ax2) = plt.subplots(1, 2)
im=ax1.pcolormesh(natl60.data.longitude.values,natl60.data.latitude.values,grad_HR.T, vmin=0, vmax=.05, cmap='viridis')
ax1.title.set_text('HR gradient')
im=ax2.pcolormesh(natl60.data.longitude.values,natl60.data.latitude.values,grad_LR.T, vmin=0, vmax=.05, cmap='viridis')
ax2.title.set_text('LR gradient')
clb=fig.colorbar(im, ax = [ax1,ax2],orientation = 'horizontal', extend='both', pad=0.2)
clb.ax.set_title('SSH Gradient (meters)')
plt.savefig(datapath+"/grad_HR_LR.png", bbox_extra_artists=(clb))

