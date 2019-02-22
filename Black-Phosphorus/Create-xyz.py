#!/usr/bin/python3

Nx=10 ; Ny=10

N=Nx*Ny*4
m=31.0
a=3.284 ; b=4.590
b1=0.8089 ; b2=b/2-b1 ; h=2.1090
unitcell=[[0.,0.,a/2,a/2],[b2,b/2,0.,b-b1],[0.,h,0.,h]]
typecell=[0,1,0,1]
Lx=Nx*a ; Ly=Ny*b ; Lz=5.25

fgpumd=open('xyz.in','w') ; fxyz=open('vmd.xyz','w')
print(N,3,2.8,file=fgpumd) ; print(N,file=fxyz)
print(1,1,1,Lx,Ly,Lz,file=fgpumd) ; print('',file=fxyz)

xyz=[] ; type=[] ; label=[0 for i in range(N)]
for nx in range(Nx):
    for ny in range(Ny):
        for i in range(4):
            x=nx*a+unitcell[0][i]
            y=ny*b+unitcell[1][i]
            z=unitcell[2][i]
            xyz.append([x,y,z])
            type.append(typecell[i])

for n in range(N):
    label[n]=int(xyz[n][0]*100/Lx)

for n in range(N):
    print(type[n],label[n],m,xyz[n][0],xyz[n][1],xyz[n][2],file=fgpumd)
    print(label[n],xyz[n][0],xyz[n][1],xyz[n][2],file=fxyz)

fgpumd.close()
fxyz.close()
