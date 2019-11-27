from natl60 import *

def plot_data_and_maps(date,nadir_lag,diro,extent):

    if not os.path.exists(diro+"/"+date):
        mk_dir_recursive(diro+"/"+date)     

    yy=date[0:4]
    mm=date[5:7]
    dd=date[8:10]
    date1_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=-1*nadir_lag),"%Y-%m-%d")
    date2_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=nadir_lag),"%Y-%m-%d")
    # plot maps
    natl60=NATL60_maps(datapath+"/maps/NATL60-CJM165_y"+yy+"m"+mm+"d"+dd+".1d_SSH.nc")  
    natl60.set_extent(extent)  
    natl60.plot(diro+"/"+date+"/NATL60_"+date+".png")
    # plot nadir tracks in [date-nadir_lag;date+nadir_lag]
    nadir=NATL60_nadir.init2(date1_nadir,date2_nadir)  
    nadir.sel_spatial(extent) 
    nadir.set_extent(extent)
    nadir.plot(diro+"/"+date+"/NATL60_nadir_"+date+"_nadlag"+str(nadir_lag)+"d.png")
    # convert swot to daily swot files
    swot=NATL60_swot.init2(date,date)
    swot.set_extent(extent)
    swot.plot(diro+"/"+date+"/NATL60_swot_"+date+".png")
    # nadir-swot fusion 
    nadir_swot_fusion=NATL60_fusion(nadir,swot)
    nadir_swot_fusion.plot(diro+"/"+date+"/NATL60_nadir_swot_"+date+"_nadlag"+str(nadir_lag)+"d.png")

if __name__ == '__main__':

    date="2013-04-03"
    #extent=[-65.,-55.,30.,40.]
    extent=[-80.,0.,25.,65.]
    plot_data_and_maps(date,5,datapath+"/plots",extent)


