#!/bin/sh
set -e

#--------------------select gpumd_software--------------------
gpumd=gpumd-1.6-D0
#gpumd=gpumd-1.6-D1
#gpumd=gpumd-1.6-D3
#gpumd=gpumd-1.6-D4

#-----------------------select timestep-----------------------
#timestep=1
timestep=2

#-----------------------select potential----------------------
#poten="jiang-nt.sw"
poten="xu-jap.sw"

pat=`pwd`

case ${poten} in
	jiang-nt.sw)
	echo "sw_1985_2
3.626   33.354  3.449  0.809  1.000
3.626   33.354  3.449  0.809  1.000
3.626   33.354  3.449  0.809  1.000
35.701  -0.16262
32.006  -0.20952
32.006  -0.20952
0.000    0.000
0.000    0.000
32.006  -0.20952
32.006  -0.20952
35.701  -0.16262" > ${poten}
;;
	xu-jap.sw)
	echo "sw_1985_2
4.3807  3045.2  13.3143  0.2103  2.1707
4.0936 10164.1  17.9602  0.1559  2.9282
4.3807  3045.2  13.3143  0.2103  2.1707
9.2660    -0.1045
11.4510   -0.2419
11.4510   -0.2419
0          0     
0          0     
11.4510   -0.2419
11.4510   -0.2419
9.2660    -0.1045" > ${poten}
;;
esac

echo "potential   ${pat}/${poten}
velocity    300

ensemble        nvt_ber 300 300 0.1
fix             22
time_step       ${timestep}
dump_thermo     100
run             1000000

ensemble        heat_nhc 300 100 30 0 21
fix             22
time_step       ${timestep}
compute_temp    100
dump_thermo     1000
dump_force      5000000
dump_position   5000000
dump_potential  5000000
run             10000000" > run.in

for i in 800.0 700.0 600.0 500.0 400.0 300.0 200.0 ; do
	job="job"${i}
	echo "1
./${job}" > input${i}.txt
	cp run.in ./${job}/run.in
	${gpumd} < input${i}.txt > ./${job}/out${i}
	rm input${i}.txt
done
