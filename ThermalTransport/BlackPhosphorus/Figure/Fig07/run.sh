#!/bin/sh
set -e

Home=`pwd`
PyFile="proc-nemd.py"
TTF="Times-New-Roman.ttf"

boundary="Fix"
length="500"

cd ${Home}
if [ ! -d ./pic ] ; then
	mkdir pic 
else
	rm -rf pic
	mkdir pic 
fi

for percent in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 ; do
	percent1=${percent}
	percent2=`echo "${percent} + 0.1" | bc -l`
	percent2=0${percent2}
	for chirality in arm zig ; do
		cd ${Home}/${boundary}-${chirality}-${length}
		cp ${Home}/${PyFile} ${Home}/${TTF} ./
		echo "# -------------------------------------"
		echo "Start "${boundary}-${chirality}-${length}
		python ${PyFile} ${percent1} ${percent2}
		mv NEMD.eps ${Home}/pic/${boundary}-${chirality}-${length}-${percent1}-${percent2}.eps
		rm ${PyFile} ${TTF}
		cd ${Home}
	done
done