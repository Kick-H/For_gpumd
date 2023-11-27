#!/bin/bash
set -e
set -u

myhome=$(pwd)
dn=1499

for i in 0 1 ; do

    odir=k_shc_-1
    wdir=shc_-1_${i}
    if [ ! -d ${wdir} ] ; then mkdir ${wdir}
    else rm -rf ${wdir} ; mkdir ${wdir} ; fi
    end=$(echo "${dn}*${i}+${dn}" | bc)
    head -n ${end} ${odir}/shc.out | tail -n ${dn} > ${wdir}/shc.out

done
