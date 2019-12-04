from natl60 import *

if __name__ == '__main__':
  
    # convert nadir files to daily NetCDF files
    list_path = [datapath+"/alongtracks/"+str for str in ["en","g2","j1","tpn"] ]
    list_files = list(flatten([ [ path+'/'+file for file in os.listdir(path) ] for path in list_path ]))
    data=NATL60_nadir(list_files) 
    data.convert2dailyNetCDF()
    # convert swot files to daily NetCDF files
    for i in range(1, 19):
        print "STEP:"+str(i)
        data=NATL60_swot(datapath+"/swot/NATL60-CJM165_SWOT_c"+str(i).zfill(2)+"*.nc")
        data.convert2dailyNetCDF()
    # convert nadir-swot combined data
    nadir_lag=5 #(days)
    swot_lag=0
    daterange = [datetime.strftime(datetime.strptime("2012-10-01","%Y-%m-%d") + timedelta(days=x),"%Y-%m-%d")\
                 for x in range (0,365)]
    for date in daterange:
        date1_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=-1*nadir_lag),"%Y-%m-%d")
        date2_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=nadir_lag),"%Y-%m-%d")
        nadir=NATL60_nadir.init2(date1_nadir,date2_nadir)  
        nadir.sel_spatial([-65,-55,30,40]) 
        swot=NATL60_swot.init2(date,date)
        nadir_swot_fusion=NATL60_fusion(nadir,swot)
        nadir_swot_fusion.convert2dailyNetCDF(date,nadir_lag,swot_lag)

