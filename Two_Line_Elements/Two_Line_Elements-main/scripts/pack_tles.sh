#!/bin/bash

indir=/home/msok/bighorns/data/TLE/
if [[ -n "$1" && "$1" != "-" ]]; then
   indir="$1"
fi

outdir=/media/msok/625ace3c-584e-49a0-b773-856d6fb8526f/tle
if [[ -n "$2" && "$2" != "-" ]]; then
   outdir="$2"
fi


if [[ -d ${indir} && -d ${outdir} ]]; then
   cd ${indir}
   for year in `echo "2020 2021 2022 2023"`   
   do
      for month in `echo "01 02 03 04 05 06 07 08 09 10 11 12"`
      do
         mon=${year}${month}
         cnt=`ls -d ${mon}?? |wc -l`
         
         if [[ $cnt -gt 0 ]]; then
            echo "tar --exclude='SATDB' --exclude 'RESULTS' --exclude '*~' --exclude 'doit!' -zcvf ${mon}.tar.gz ${mon}??"
            sleep 1
            tar --exclude='SATDB' --exclude 'RESULTS' --exclude '*~' --exclude 'doit!' -zcvf ${mon}.tar.gz ${mon}??
         
            echo "mv ${mon}.tar.gz ${outdir}"
            mv ${mon}.tar.gz ${outdir}
         else
            echo "WARNING : no directory ${mon} -> skipped"
         fi
      done      
   done
   
   
else
   echo "ERROR : input ($indir) or output ($outdir) directory does not exist"
fi
