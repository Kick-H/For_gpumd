#!/bin/bash
# Prediction XYZ via NEP from nep.txt
# nep.in created from nep.txt
# author: Ke XU

set -e
set -u

check_file(){
   cfile=$1
   if [ ! -f "${cfile}" ] ; then
       echo "Errors: there is no file ${cfile}"
       exit
   fi
}
check_dir(){
   cdir=$1
   if [ ! -d "${cdir}" ] ; then
       echo "Errors: there is no dir ${cdir}"
       exit
   fi
}

predict_NEP_XYZ(){
   name=$1
   if [ ! -d ${name} ] ; then mkdir ${name}
   else rm -rf ${name} ; mkdir ${name} ; fi

   xyzfile=$3
   check_file "${xyzfile}"

   cd "${name}"
   nepfile=$2
   ln -s "${nepfile}" nep.txt
   echo "type $(head -n 1 nep.txt | cut -d ' ' -f2-)" > nep.in
   echo "$(head -n 2 nep.txt | tail -n 1 | cut -d ' ' -f1,2,3)" >> nep.in
   echo "$(head -n 5 nep.txt | tail -n 3)" >> nep.in
   echo "neuron $(head -n 6 nep.txt | tail -n 1 | cut -d ' ' -f2)" >> nep.in
   echo "prediction 1" >> nep.in
   ln -s "${xyzfile}" train.xyz

   nepexe=$4
   check_file "${nepexe}"
   nep > out.pre.nep
   cd ..
}

xyzdir="XYZ"
nepdir="NEPs"
nepexe="nep"

echo "#XYZ NEP energy force stress"
for valxyz in $(cd "${xyzdir}" ; ls *xyz) ; do
    xyzname=$(echo ${valxyz} | cut -d '.' -f1)
    xyzfile="${xyzdir}/${valxyz}"

    for ni in $(cd "${nepdir}" ; ls *txt) ; do

        nepname=$(echo ${ni} | cut -d '.' -f1)
        dirname=${xyzname}-${nepname}
        echo -e "${xyzname} ${nepname} \c"
        nepfile="${nepdir}/${ni}"
        predict_NEP_XYZ "${dirname}" "${nepfile}" "${xyzfile}" "${nepexe}"
        cd "${dirname}"
        python ../plot_predict.py 3
        cp train.png ../${dirname}.png
        cd ..
        # rm -rf "${dirname}"
        echo ""

    done
done
