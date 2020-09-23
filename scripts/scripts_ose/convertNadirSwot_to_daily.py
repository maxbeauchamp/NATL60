from natl60 import *

if __name__ == '__main__':
  
    # convert nadir files to daily NetCDF files
    list_path = [rawdatapath+"/OSE/alongtracks/"+str for str in ["alg","h2g","j2g","j2n","j3","s3a"] ]
    #list_path = [rawdatapath+"/OSE/alongtracks/"+str for str in ["c2"] ]
    list_files = list([ [ path+'/'+file for file in os.listdir(path) ] for path in list_path ])
    list_files = list(itertools.chain(*list_files))
    data=NATL60_nadir2(list_files,"OSMOSIS") 
    data.convert2dailyNetCDF(domain="OSMOSIS",id_phase="training")
