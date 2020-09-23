for i in {1..365}; do 
    day=$(date +%Y/%m/%d -d "2012-09-30 +$i days")
    echo $day
    yy=$(date -d "$day" +"%Y")
    mm=$(date -d "$day" +"%m")
    dd=$(date -d "$day" +"%d")
    echo $dd
#    wget -P /home/administrateur/Bureau/NATL60/RAW_DATA/SST_SSS/GULFSTREAM2 https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/NATL60-CJM165/GULFSTREAM/NATL60GULSTREAM-CJM165_y${yy}m${mm}d${dd}.1d_sosstsst.nc
#    wget -P /home/administrateur/Bureau/NATL60/RAW_DATA/SST_SSS/GULFSTREAM2 https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/NATL60-CJM165/GULFSTREAM/NATL60GULSTREAM-CJM165_y${yy}m${mm}d${dd}.1d_sosaline.nc
#    wget -P /home/administrateur/Bureau/NATL60/RAW_DATA/SST_SSS/OSMOSIS https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/NATL60-CJM165/SST-SSS-OSMOSIS/NATL60OSMO-CJM165_y${yy}m${mm}d${dd}.1d_sosstsst.nc
#    wget -P /home/administrateur/Bureau/NATL60/RAW_DATA/SST_SSS/OSMOSIS https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/NATL60-CJM165/SST-SSS-OSMOSIS/NATL60OSMO-CJM165_y${yy}m${mm}d${dd}.1d_sosaline.nc
     wget -P /home/administrateur/Bureau/NATL60/RAW_DATA/SST_SSS/GULFSTREAM https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/NATL60-CJM165/GULF/NATL60GULF-CJM165_y${yy}m${mm}d${dd}.1d_sosstsst.nc
     wget -P /home/administrateur/Bureau/NATL60/RAW_DATA/SST_SSS/GULFSTREAM https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/NATL60-CJM165/GULF/NATL60GULF-CJM165_y${yy}m${mm}d${dd}.1d_sosaline.nc
done

