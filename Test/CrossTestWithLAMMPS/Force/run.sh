#!/bin/bash
set -e

# Warning ! Please confirm the file you should replace.
lmpfl="pair_sw.cpp"
gpufl="makefile"

pkdoc="package"
lmppk="lammps-stable.tar.gz"
gpupk="GPUMD-SW2016.zip"

indoc="infiles"
modfl="mos2.cpp"
runpr="gcc"
runin="run.in"
potgp="mos2_sw3_2016.txt"
potla="mos2.sw"
pyfil="format.py"

doc11="preparation"
doc12="gpumd"
doc13="lammps"
doc14="pic"

set +e
rm -r ${doc11} ${doc12} ${doc13} ${doc14}
set -e

echo "Copyright by Kick, 2018-5"
echo "!!! Before run this sprit, you must confirm these
 >> python3
 >> cuda
 >> tar
 >> unzip
 >> ${runpr}
!!! programs have been added to system PATH."
echo "Running check processors. Well, you must confirm the version of your two package (lammps and gpumd)."
docmain=`pwd`

if [ ! -d ${pkdoc} ] ; then
	echo "Wrong preparation. You should confirm the folder of bash sprit is same as the package folder."
	exit 1
elif [ ! -f ./${pkdoc}/${lmppk} ] ; then
	echo "Error! The lammps stable package is not in the package floder!
		Download it from: https://drive.google.com/open?id=1JIiboNduDAvGhasgSD5LB4S7_959nxS5
		And copy it to ./${pkdoc}"
	exit 1
elif [ ! -f ./${pkdoc}/${gpupk} ] ; then
	echo "Error! The gpumd package is not in the package floder! Please check it.
		Download it from: https://drive.google.com/open?id=1OeNA0QdhMfYcDKOZx2jySu8n-BIKo5y-
		And copy it to ./${pkdoc}"
	exit 1
elif [ ! -f ./${pkdoc}/${lmpfl} ] ; then
	echo "Error! The file of modifing lammps is not in the package floder! Please check it."
	exit 1
elif [ ! -f ./${pkdoc}/${gpufl} ] ; then
	echo "Error! The modifing makefile of gpumd is not in the package floder! Please check it."
	exit 1
fi

if [ ! -d ${indoc} ] ; then
	echo "Wrong preparation. You should confirm the folder of bash sprit is same as the infiles folder."
	exit 1
elif [ ! -f ./${indoc}/${modfl} ] ; then
	echo "Error! The program to create xyz.in is not in infiles folder! Please check it."
	exit 1
elif [ ! -f ./${indoc}/${runin} ] ; then
	echo "Error! The file of run.in is not in the infiles floder! Please check it."
	exit 1
elif [ ! -f ./${indoc}/${potgp} ] ; then
	echo "Error! The potential of gpumd is not in the infiles floder! Please check it."
	exit 1
elif [ ! -f ./${indoc}/${potla} ] ; then
	echo "Error! The potential of lammps is not in the infiles floder! Please check it."
	exit 1
fi
echo "Check over. Now start 'One-click testing'."

echo "Make master folder"
for i in ${doc11} ${doc12} ${doc13} ${doc14} ; do
	if [ ! -d ${i} ] ; then
		mkdir ${i}
		echo "./"${i}" has been created."
	else
		echo "./"${i}" exist, continue bash."
	fi
done

echo "### Step 1 ###"
echo "Make lammps"
cd ${doc11}
i="MakeLammps"
if [ ! -d ${i} ] ; then
	mkdir ${i}
	echo "./"${doc11}/${i}" has been created. Making lammps, you can check it with file ./${doc11}/${i}/lamp_make.out"
	tar -xvf ../${pkdoc}/${lmppk} -C ./${i}
	cp ../${pkdoc}/${lmpfl} ./${i}/lammps-31Mar17/src
	cd ./${i}/lammps-31Mar17/src
	make mpi -j4
	lammps=`pwd`/lmp_mpi
	cd ../../../../
else
	echo "./"${doc11}/${i}" exist, recall your replacement file, continue bash."
	cd ./${i}/lammps-31Mar17/src
	lammps=`pwd`/lmp_mpi
	cd ../../../../
fi

echo "### Step 2 ###"
echo "Make gpumd"
cd ${doc11}
i="MakeGpumd"
if [ ! -d ${i} ] ; then
	mkdir ${i}
	echo "./"${doc11}/${i}" has been created. Making gpumd, you can check it with file ./${doc11}/${i}/gpu_make.out"
	unzip ../${pkdoc}/${gpupk} -d ./${i}
	cp ../${pkdoc}/${gpufl} ./${i}/GPUMD-master/src
	cd ./${i}/GPUMD-master/src
	make
	gpumd=`pwd`/gpumd
	cd ../../../../
else
	echo "./"${doc11}/${i}" exist, recall your replacement file, continue bash."
	cd ./${i}/GPUMD-master/src
	gpumd=`pwd`/gpumd
	cd ../../../../
fi

echo "### Step 3 ###"
echo "Create file of read.data and in.xyz."
cd ${doc11}
i="Run"
if [ ! -d ${i} ] ; then
	mkdir ${i}
	echo "./"${i}" has been created."
else
	echo "./"${i}" exist, continue bash."
fi
cd ${i}
cp ../../${indoc}/${modfl} ./
cp ../../${indoc}/${runin} ./
cp ../../${indoc}/${potgp} ./
cp ../../${indoc}/${pyfil} ./
echo "Warning, you should check this command under me in the bash sprit."
${runpr} ${modfl} && ./a.out
rm ./a.out

echo "1
./" > input
${gpumd} < input > out

python3 ${pyfil}
cp gpumd.in  ../../${doc12}/xyz.in
cp read.data ../../${doc13}/read.data
cd ../../
echo "######################################
This sprit is Done.
Keeping you waiting, but waiting is worth it
Tips: The speed of gpumd is related to cut-off in xyz.in,
        but you should be careful when changing it.
######################################
            Compare now"
#gedit out  # to check the gpumd run by yourself

echo "### Step 4 Run gpumd ###"
cd ${doc12}
echo "potential       ./${potgp}
velocity        300
ensemble        nve
neighbor        1
time_step       1
dump_force      10000
run             0
" > run.in
cp ../${indoc}/${potgp} ./
echo "1
./" > input
${gpumd} < input > out
cd ../

echo "### Step 5 Run lammps ###"
cd ${doc13}
echo "dimension   3
boundary    p  p  s
units       metal
atom_style  atomic
read_data   read.data
pair_style  sw
pair_coeff  * * ./mos2.sw Mo S C
neighbor    1.0        bin
dump        Strj all  custom  1  force.lammpstrj id type x y z fx fy fz
dump_modify Strj format line \"%10d %5d %16.10g %16.10g %16.10g %16.10g %16.10g %16.10g\" sort id 
fix         1 all nve
run         0" > in.compare
cp ../${indoc}/${potla} ./
${lammps} < in.compare > out
cd ../

echo "#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

with open('./gpumd/f.out','r') as f0, open('./lammps/force.lammpstrj','r') as f1, open('./pic/compare.dat','w') as f2:
	l0=f0.readlines()
	l1=f1.readlines()
	nat=int(len(l0))
	df=[[0 for i in range(nat)] for i in range(7)]
	for i in range(nat):
		fl0=l0[i].split()
		fl1=l1[i+9].split()
		df[0][i]=i
		df[1][i]=float(fl0[0])-float(fl1[5])
		df[2][i]=float(fl0[1])-float(fl1[6])
		df[3][i]=float(fl0[2])-float(fl1[7])
		df[4][i]=float(fl0[0])
		df[5][i]=float(fl0[1])
		df[6][i]=float(fl0[2])
	fig = plt.figure()  
	ax1 = fig.add_subplot(111) 
	ax1.set_title('Compare force between lammps and gpumd') 
	plt.xlabel('Atom ID')
	plt.ylabel('Force errors')
	ym=[min([min(df[1]),min(df[3]),min(df[2])]),max([max(df[1]),max(df[3]),max(df[2])])]
	dm=[ym[0]-(ym[1]-ym[0])*0.1,ym[1]+(ym[1]-ym[0])*0.1]
	plt.ylim([dm[0],dm[1]]) 
	ax1.scatter(df[0],df[1],s=10,c = '',marker = 'o',edgecolors='b')
	ax1.scatter(df[0],df[2],s=10,c = '',marker = 'o',edgecolors='r')
	ax1.scatter(df[0],df[3],s=10,c = '',marker = 'o',edgecolors='k')
	fig.savefig('./pic/result.png',dpi=300)

	fig1 = plt.figure()  
	ax2 = fig1.add_subplot(111) 
	ax2.set_title('Gpumd force') 
	plt.xlabel('Atom ID')
	plt.ylabel('Force')
	ym=[min([min(df[4]),min(df[5]),min(df[6])]),max([max(df[4]),max(df[5]),max(df[6])])]
	dm=[ym[0]-(ym[1]-ym[0])*0.1,ym[1]+(ym[1]-ym[0])*0.1]
	plt.ylim([dm[0],dm[1]]) 
	ax2.scatter(df[0],df[4],s=10,c = '',marker = 'o',edgecolors='b')
	ax2.scatter(df[0],df[5],s=10,c = '',marker = 'o',edgecolors='r')
	ax2.scatter(df[0],df[6],s=10,c = '',marker = 'o',edgecolors='k')
	fig1.savefig('./pic/origin.png',dpi=300)" > plot.py

python3 plot.py
rm plot.py