#!/bin/bash

HOMEDIR=/gpfsscratch/rech/yrf/uba22to/u_v
declare -a lvar=('vozocrtx' 'vomecrty')
declare -a lvar2=('u' 'v')
declare -a lvar3=('gridU' 'gridV')
for k in 1; do
  var=${lvar[$k]}
  var2=${lvar3[$k]}
  newvar=${lvar2[$k]}
  for i in {0..364}; do 
    day=$(date -I -d "2012-10-01 +$i days")
    yy=$(date -d $day '+%Y')
    mm=$(date -d $day '+%m')
    dd=$(date -d $day '+%d')
    hfile=${HOMEDIR}/NATL60-CJM165_y${yy}m${mm}d${dd}.1h_${var2}.nc
    dfile=${HOMEDIR}/NATL60-CJM165_${newvar}_y${yy}m${mm}d${dd}.1d.nc
    echo DATE" : "$day"\n"
    #ncks -O --mk_rec_dmn time ${hfile} ${hfile}.tmp
    ncra -O -F -d time_counter,1,,1 ${hfile} ${dfile}
    ncks --dmn x,0,5421,3 --dmn y,0,3453,3 ${dfile} ${dfile}.tmp
    rm -rf ${dfile}
    mv -f ${dfile}.tmp ${dfile}
  done
  ldfile=`ls ${HOMEDIR}/NATL60-CJM165_${newvar}_*.1d.nc`
  yfile=${HOMEDIR}/NATL60-CJM165_${newvar}_y${yy}.1y.nc
  ncrcat -O ${ldfile[*]} ${yfile}
  ncrename -O -v ${var},${newvar} ${yfile}
  #python3 replace_nan.py ${yfile} ${newvar}
done
