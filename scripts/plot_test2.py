from natl60 import *

def plot_maps(date,nadir_lag,diro,extent):
    if not os.path.exists(diro+"/"+date):
        mk_dir_recursive(diro+"/"+date)     
    yy=date[0:4]
    mm=date[5:7]
    dd=date[8:10]
    # plot maps
    natl60=NATL60_maps(datapath+"/maps/NATL60-CJM165_ssh_y2013.1y.nc")
    natl60.set_extent(extent)  
    natl60.sel_time(date,date)
    natl60.plot("ssh",diro+"/"+date+"/NATL60_"+date+".png")
    # plot OI
    natl60=NATL60_maps(datapath+"/oi/ssh_NATL60_4nadir.nc")
    natl60.set_extent(extent)  
    natl60.sel_time(date,date)
    natl60.plot("ssh_obs",diro+"/"+date+"/OI4nadir_obs_"+date+".png")
    natl60.plot("ssh_mod",diro+"/"+date+"/OI4nadir_mod_"+date+".png")
    # plot data
    natl60=NATL60_maps(datapath+"/data/dataset_nadir_swot.nc")
    natl60.set_extent(extent)  
    natl60.sel_time(date,date)
    natl60.plot("ssh_obs",diro+"/"+date+"/data4nadirswot_obs_"+date+".png")
    natl60.plot("ssh_mod",diro+"/"+date+"/data4nadirswot_mod_"+date+".png")
    natl60.plot("anomaly_obs",diro+"/"+date+"/data4nadirswot_anom_obs_"+date+".png")
    natl60.plot("anomaly_mod",diro+"/"+date+"/data4nadirswot_anom_mod_"+date+".png")

if __name__ == '__main__':

    date="2013-04-03"
    extent=[-65.,-55.,30.,40.]
    plot_maps(date,5,datapath+"/plots",extent)


