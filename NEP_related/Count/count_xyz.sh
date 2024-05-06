#!/bin/base
set -e
set -u


for fxyz in $(ls *xyz) ; do

    echo -e "${fxyz}: \c"
    echo $(wc -l ${fxyz} | cut -d ' ' -f1) $(grep energy ${fxyz} | wc -l) | awk '{print $1-$2*2 " atoms,", $2 " frames"}'

done
