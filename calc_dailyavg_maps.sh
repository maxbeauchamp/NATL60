#!/bin/bash

HOMEDIR=/home/user/Bureau/NATL60/maps
for i in {0..364}; do 
    day=$(date -I -d "2012-10-01 +$i days")
    yy=$(date -d $day '+%Y')
    mm=$(date -d $day '+%m')
    dd=$(date -d $day '+%d')
    lfile=`ls ${HOMEDIR}/NATL60-CJM165_y${yy}m${mm}d${dd}*`
    hfile=${HOMEDIR}/NATL60-CJM165_y${yy}m${mm}d${dd}.24h_SSH.nc
    dfile=${HOMEDIR}/NATL60-CJM165_y${yy}m${mm}d${dd}.1d_SSH.nc
    for file in ${lfile[*]} ; do
      ncks -O --mk_rec_dmn time ${file} ${file}.tmp
    done
    lfile=`ls ${HOMEDIR}/NATL60-CJM165_y${yy}m${mm}d${dd}*tmp*`
    echo DATE" : "$day"\n"
    ncrcat -O ${lfile[*]} ${hfile}
    ncra -O -F -d time,1,,1 ${hfile} ${dfile}
    rm -rf ${lfile[*]} ${hfile}
done
