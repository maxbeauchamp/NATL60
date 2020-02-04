#!/bin/bash

HOMEDIR=/home/user/Bureau/NATL60/DATA/maps
declare -a lvar=('sosaline' 'sossheig' 'sosstsst')
declare -a lvar2=('sss' 'ssh' 'sst')
for k in 0 1 2; do
  var=${lvar[$k]}
  newvar=${lvar2[$k]}
  for i in {0..364}; do 
    day=$(date -I -d "2012-10-01 +$i days")
    yy=$(date -d $day '+%Y')
    mm=$(date -d $day '+%m')
    dd=$(date -d $day '+%d')
    hfile=${HOMEDIR}/${var}/NATL60-CJM165_${var}_y${yy}m${mm}d${dd}.1h_gridT.nc
    dfile=${HOMEDIR}/${var}/NATL60-CJM165_${newvar}_y${yy}m${mm}d${dd}.1d.nc
    echo DATE" : "$day"\n"
    ncks -O --mk_rec_dmn time ${hfile} ${hfile}.tmp
    ncra -O -F -d time,1,,1 ${hfile}.tmp ${dfile}
    rm -rf ${hfile}.tmp
  done
  ldfile=`ls ${HOMEDIR}/${var}/NATL60-CJM165_${newvar}_*.1d.nc`
  yfile=${HOMEDIR}/NATL60-CJM165_${newvar}_y${yy}.1y.nc
  ncrcat -O ${ldfile[*]} ${yfile}
  ncrename -O -v ${var},${newvar} ${yfile}
  python3 replace_nan.py ${yfile} ${newvar}
done
