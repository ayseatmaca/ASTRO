#!/bin/bash

current_month=`date +%Y%m`
if [[ -n "$1" && "$1" != "-" ]]; then
   current_month="$1"
fi

indir=/home/msok/bighorns/data/TLE/
if [[ -n "$2" && "$2" != "-" ]]; then
   indir="$2"
fi

echo "#####################################"
echo "PARAMETERS:"
echo "#####################################"
echo "current_month = $current_month"
echo "#####################################"

mkdir -p /tmp/tle/

if [[ -d ${indir} ]]; then
   cd ${indir}

   echo "tar --exclude='SATDB' --exclude 'RESULTS' --exclude '*~' --exclude 'doit!' -zcvf /tmp/tle/${current_month}.tar.gz ${current_month}??"
   tar --exclude='SATDB' --exclude 'RESULTS' --exclude '*~' --exclude 'doit!' -zcvf /tmp/tle/${current_month}.tar.gz ${current_month}??   
else
   echo "ERROR : input ($indir) directory does not exist"
fi
   