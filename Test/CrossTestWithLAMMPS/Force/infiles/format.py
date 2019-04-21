#!/usr/bin/python3
with open('thermo.out','r') as f0, open('xyz.in','r') as f1, open('xyz.out','r') as f2, open('out.xyz','w') as f3, open('gpumd.in','w') as f4, open('read.data','w') as f5:
	l0=f0.readlines()
	l1=f1.readlines()
	l2=f2.readlines()
	nat=int(l1[0].split()[0])
	box=[l0[len(l0)-1].split()[6],l0[len(l0)-1].split()[7],l0[len(l0)-1].split()[8]]
	for i in range(len(l2)):
		if i%nat==0:
			print(nat,file=f3)
			print(box[0],box[1],box[2],file=f3)
		print(int(l1[i%nat+2].split()[0])+1,float(l2[i].split()[0]),float(l2[i].split()[1]),float(l2[i].split()[2]),file=f3)
	for i in range(len(l1)):
		ll4=l1[i].split()
		if i==0:
			print(ll4[0],ll4[1],ll4[2],file=f4)
			continue
		if i==1:
			print(ll4[0],ll4[1],ll4[2],box[0],box[1],box[2],file=f4)
			continue
		ll3=l2[int(len(l2))-nat+i-2].split()
		print(ll4[0],ll4[1],ll4[2],float(ll3[0]),float(ll3[1]),float(ll3[2]),file=f4)

	print('LAMMPS data file (atomic). Create by python3. Copyright Kick 2018-5-20',file=f5)
	print('',file=f5)
	print(nat,'atoms',file=f5)
	print('',file=f5)
	print(3,'atom types',file=f5)
	print('',file=f5)
	print(0.0,box[0],'xlo xhi',file=f5)
	print(0.0,box[1],'ylo yhi',file=f5)
	print(-3.0,float(box[2])-3,'zlo zhi',file=f5)
	print('',file=f5)
	print('Masses',file=f5)
	print('',file=f5)
	print(1,96.0,'# Mo',file=f5)
	print(2,32.0,'# S',file=f5)
	print(3,32.0,'# C',file=f5)
	print('',file=f5)
	print('Atoms # atomic',file=f5)
	print('',file=f5)
	for i in range(len(l1)):
		if i<2:
			continue
		ll4=l1[i].split()
		ll3=l2[int(len(l2))-nat+i-2].split()
		print(i-1,int(ll4[0])+1,float(ll3[0]),float(ll3[1]),float(ll3[2]),file=f5)