from natl60 import *

if __name__ == '__main__':
  
    # convert nadir files to daily NetCDF files
    '''list_path = [datapath+"/data/alongtracks/"+str for str in ["en","g2","j1","tpn"] ]
    list_files = list([ [ path+'/'+file for file in os.listdir(path) ] for path in list_path ])
    list_files = list(itertools.chain(*list_files))
    data=NATL60_nadir(list_files,1) 
    data.convert2dailyNetCDF()'''
    # convert swot files to daily NetCDF files
    domain="OSMOSIS"
    if domain=="GULFSTREAM":
        cyclemax=18
    if domain=="GULFSTREAM2":
        cyclemax=19
    if domain=="OSMOSIS":
        cyclemax=18
    path = rawdatapath+"/swot/"+domain
    '''list_files = [path+'/'+file for file in os.listdir(path) if "nadir" not in file]
    data=NATL60_swot(list_files,dateref=None,type_err="wocor")
    data.convert2dailyNetCDF(path)'''
    for i in range(1, cyclemax):
        print("CYCLE:"+str(i))
        list_files = [path+'/'+file for file in os.listdir(path) if ( ("nadir" not in file) and ("c"+str(i).zfill(2) in file) )]
        data=NATL60_swot(list_files,dateref=None,type_err="wocor")
        data.convert2dailyNetCDF(path)
    '''# convert nadir-swot combined data
    nadir_lag=5 #(days)
    swot_lag=0
    daterange = [datetime.strftime(datetime.strptime("2012-10-01","%Y-%m-%d") + timedelta(days=x),"%Y-%m-%d")\
                 for x in range (0,365)]
    for date in daterange:
        print(date)
        date1_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=-1*nadir_lag),"%Y-%m-%d")
        date2_nadir=datetime.strftime(datetime.strptime(date,"%Y-%m-%d") + timedelta(days=nadir_lag),"%Y-%m-%d")
        nadir=NATL60_nadir.init2(date1_nadir,date2_nadir)  
        nadir.sel_spatial([-65,-55,30,40]) 
        swot=NATL60_swot.init2(date,date)
        nadir_swot_fusion=NATL60_fusion(nadir,swot)
        nadir_swot_fusion.convert2dailyNetCDF(date,nadir_lag,swot_lag)'''

