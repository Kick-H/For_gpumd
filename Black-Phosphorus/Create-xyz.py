#!/usr/bin/python3

Nzig=10 ; Narm=10

natom=Nzig*Narm*4
mass=31.0
lat_zig=3.284 ; lat_arm=4.590
b1=0.8089 ; b2=lat_arm/2-b1 ; h=2.1090
unitcell=[[0.,0.,lat_zig/2,lat_zig/2],[b2,lat_arm/2,0.,lat_arm-b1],[0.,h,0.,h]]
typecell=[0,1,0,1]
Lx=Nzig*lat_zig ; Ly=Narm*lat_arm ; Lz=5.25

fgpumd=open('xyz.in','w') ; fxyz=open('vmd.xyz','w')
print(natom,3,2.8,file=fgpumd) ; print(natom,file=fxyz)
print(1,1,1,Lx,Ly,Lz,file=fgpumd) ; print('',file=fxyz)

xyz=[] ; type=[] ; label=[0 for i in range(natom)]
for nx in range(Nzig):
    for ny in range(Narm):
        for i in range(4):
            x=nx*lat_zig+unitcell[0][i]
            y=ny*lat_arm+unitcell[1][i]
            z=unitcell[2][i]
            xyz.append([x,y,z])
            type.append(typecell[i])

for n in range(natom):
    label[n]=int(xyz[n][0]*5/Lx)

for n in range(natom):
    print(type[n],label[n],mass,xyz[n][0],xyz[n][1],xyz[n][2],file=fgpumd)
    print(label[n],xyz[n][0],xyz[n][1],xyz[n][2],file=fxyz)

fgpumd.close()
fxyz.close()
