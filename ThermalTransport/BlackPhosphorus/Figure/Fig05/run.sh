#!/bin/sh
set -e

Home=`pwd`
PyFile="proc-nemd.py"
TTF="Times-New-Roman.ttf"

cd ${Home}
if [ ! -d ./pic ] ; then
	mkdir pic 
else
	rm -rf pic
	mkdir pic 
fi

for boundary in Fix Per ; do
	for chirality in arm zig ; do
		for length in 200.0 300.0 400.0 500.0 600.0 700.0 800.0 ; do
			cd ${Home}/${boundary}/${chirality}/job${length}
			cp ${Home}/${PyFile} ${Home}/${TTF} ./
			echo "# -------------------------------------"
			echo "Start "${boundary}-${chirality}-${length}
			python ${PyFile}
			mv NEMD.eps ${Home}/pic/${boundary}-${chirality}-${length}.eps
			rm ${PyFile} ${TTF}
			cd ${Home}
		done
	done
done
