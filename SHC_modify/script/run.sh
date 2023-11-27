#!/bin/bash
set -e
set -u

myhome=$(pwd)

for ver in 3.8 3.9 3.9.1 ; do

    vdir=ver-${ver}
    if [ ! -d ${vdir} ] ; then mkdir ${vdir}
    else rm -rf ${vdir} ; mkdir ${vdir} ; fi

    cp -r src_${ver} ${vdir}/o_src_${ver}
    cp -r src_${ver} ${vdir}/k_src_${ver}
    cp -r modify_shc.cu  ${vdir}/k_src_${ver}/measure/shc.cu
    cp -r modify_shc.cuh ${vdir}/k_src_${ver}/measure/shc.cuh
    cp -r run ${vdir}

    cd ${vdir}/o_src_${ver}
    make clean
    make gpumd -j4
    cd ../k_src_${ver}
    make clean
    make gpumd -j4
    cd ..

    for i in -1 0 1 ; do

        odir=k_shc_${i}
        if [ ! -d ${odir} ] ; then cp -r run ${odir}
        else rm -rf ${odir} ; cp -r run ${odir} ; fi
        cd ${odir}
        sed -i "s/Ngroup/${i}/g" run.in
        ../k_src_${ver}/gpumd
        cd ..

    done

    for i in 0 1 ; do

        odir=o_shc_${i}
        if [ ! -d ${odir} ] ; then cp -r run ${odir}
        else rm -rf ${odir} ; cp -r run ${odir} ; fi
        cd ${odir}
        sed -i "s/Ngroup/${i}/g" run.in
        ../o_src_${ver}/gpumd
        cd ..

    done

    cd ..

done

