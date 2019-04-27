import os
import numpy as np
from matplotlib.pylab import *
from matplotlib.font_manager import FontProperties   
font_song=FontProperties(fname=os.path.join(os.getcwd(),'Times-New-Roman.ttf'),size=16)

percent=0.8
per_grand1=0.2
per_grand2=0.8
data_interval=100

frun=open('run.in','r')
for line in frun.readlines():
    str=line.split() 
    if str and str[0]=='time_step' :
        timestep=list(map(int,str[1:]))
    if str and str[0]=='compute_temp' :
        out_freq=list(map(int,str[1:]))
    if str and str[0]=='run' :
        out_step=list(map(int,str[1:]))
dt = 0.000001*timestep[0]   # ns
run_step = out_step[0]
interval=out_freq[0]
frun.close()

DATA=np.loadtxt('temperature.out')
N_frame=len(DATA)
N_group=len(DATA[0])-2
print('# > Data sampling interval:',interval,'Number of frames:',N_frame,'Number of group:',N_group)
if run_step//interval > N_frame:
    print('The run is not over yet, but the calculation continues')
else:
    print('# > End of operation, continue to calculate')

# get the center for each group.
fxyz=open('xyz.in','r')
codr=[[0,0,0] for i in range(N_group)]
codr_num=[0 for i in range(N_group)]
for i,line in enumerate(fxyz.readlines()):
    if i==1:
        width=float(line.split()[4])
        high=float(line.split()[5])
    if i<2:            # Skip the first two lines of 'xyz.in'
        continue
    str=line.split()
    for j in range(3):
        codr[int(str[1])][j] += list(map(float,str[3:]))[j]
    codr_num[int(str[1])] += 1
codr=[[line[i]/codr_num[j] for i in range(3)] for j,line in enumerate(codr)]
fxyz.close()
area=high*width     # nm^2
print('# # The cross-sectional area used for the calculation is:',area,'(Angstrom^2)')

x_time=[i*dt*data_interval*interval for i in range(N_frame//data_interval)]
DATA_ave=[[0 for i in range(len(DATA[0]))] for j in range(N_frame//data_interval)]
for i in range((N_frame//data_interval)*data_interval):
    for j in range(N_group+2):
        DATA_ave[i//data_interval][j] += DATA[i,j]/data_interval
del(DATA)
DATA_ave=list(zip(*DATA_ave))

figure(figsize=(15,11))
subplot(2,2,1)
for i,line in enumerate(DATA_ave[:N_group]):
    if i==1:
        plot(x_time,line,linewidth=0.5,label='temp-each-group')
    else:
        plot(x_time,line,linewidth=0.5)
xlim(xmin=0.,xmax=20)
ylim(ymin=260,ymax=340)
xticks(range(0,21,5),fontproperties=font_song)
yticks(range(260,341,20),fontproperties=font_song)
leg=legend(loc='upper left',fontsize=14)
leg.get_frame().set_linewidth(0.)
plt.xlabel('Time (ns)',fontproperties=font_song)
plt.ylabel('Temperature (K)',fontproperties=font_song)

subplot(2,2,2)
t_rang=[[0,N_group],[int(len(DATA_ave[0])*percent1),int(len(DATA_ave[0])*percent2)]]
data_grand=[0 for i in range(N_group)]
x_codr=[sublist[0] for sublist in codr]
for i in range(N_group):
    for j in range(t_rang[1][0],t_rang[1][1]):
        data_grand[i] += DATA_ave[i][j]/(t_rang[1][1]-t_rang[1][0])
plot(x_codr,data_grand,linewidth=2,label='temp-grandient')
min_temp_codr=data_grand.index(min(data_grand))
max_temp_codr=data_grand.index(max(data_grand))
if abs(max_temp_codr-min_temp_codr) < N_group*0.75:
    print('# > Calculate the temperature gradient according to the NEMD-Periodic method.')
    first_temp_ther=0
    print('# > The first thermo is set as:',first_temp_ther)
    slice_left=[first_temp_ther+N_group*0.5*per_grand1,first_temp_ther+N_group*0.5*per_grand2+1]
    slice_left=list(map(int,slice_left))
    fit_left_x=x_codr[slice_left[0]:slice_left[1]]
    fit_left_t=data_grand[slice_left[0]:slice_left[1]]
    poly_left=np.polyfit(fit_left_x,fit_left_t,deg=1)
    slice_righ=[first_temp_ther+N_group*0.5*(1+per_grand1),first_temp_ther+N_group*0.5*(1+per_grand2)+1]
    slice_righ=list(map(int,slice_righ))
    fit_righ_x=x_codr[slice_righ[0]:slice_righ[1]]
    fit_righ_t=data_grand[slice_righ[0]:slice_righ[1]]
    poly_righ=np.polyfit(fit_righ_x,fit_righ_t,deg=1)
    plot(fit_left_x,np.polyval(poly_left,fit_left_x),linewidth=3,label='fit-left')
    plot(fit_righ_x,np.polyval(poly_righ,fit_righ_x),linewidth=3,label='fit-right')
    temp_grandient=(abs(poly_left[0])+abs(poly_righ[0]))*0.5
else:
    print('# > Calculate the temperature gradient according to the NEMD-Fix method.')
    first_temp_ther=0
    print('# > The first thermo is set as:',first_temp_ther)
    slice_temp=[first_temp_ther+N_group*per_grand1,first_temp_ther+N_group*per_grand2+1]
    slice_temp=list(map(int,slice_temp))
    fit_temp_x=x_codr[slice_temp[0]:slice_temp[1]]
    fit_temp_t=data_grand[slice_temp[0]:slice_temp[1]]
    poly_temp=np.polyfit(fit_temp_x,fit_temp_t,deg=1)
    plot(fit_temp_x,np.polyval(poly_temp,fit_temp_x),label='fit-temp')
    temp_grandient=abs(poly_temp[0])
print('# # The temperature grandient is:',temp_grandient,'(K/Angstrom)')
#xlim(xmin=0.,xmax=1500)
#xticks(range(0,1501,300),fontproperties=font_song)
ylim(ymin=265,ymax=335)
yticks(range(265,336,20),fontproperties=font_song)
leg=legend(loc='upper center',fontsize=14)
leg.get_frame().set_linewidth(0.)
plt.xlabel('Coordinates (Angstrom)',fontproperties=font_song)
plt.ylabel('Temperature (K)',fontproperties=font_song)

subplot(2,2,3)
plot(x_time,DATA_ave[N_group],linewidth=2,label='flux-heat-source')
plot(x_time,DATA_ave[N_group+1],linewidth=2,label='flux-heat-sink')

start_fit=int(len(x_time)*percent)
fit_flux_t1=x_time[start_fit:]
fit_flux1=DATA_ave[N_group][start_fit:]
poly_flux1=np.polyfit(fit_flux_t1,fit_flux1,deg=1)
fit_flux2=DATA_ave[N_group+1][start_fit:]
poly_flux2=np.polyfit(fit_flux_t1,fit_flux2,deg=1)
plot(fit_flux_t1,np.polyval(poly_flux1,fit_flux_t1),linewidth=3,label='fit-left')
plot(fit_flux_t1,np.polyval(poly_flux2,fit_flux_t1),linewidth=3,label='fit-right')

heat_flux=(abs(poly_flux1[0])+abs(poly_flux2[0]))*0.5
if abs(max_temp_codr-min_temp_codr) < N_group*0.75:   # If periodic, Heat flux should devided by 2.
    heat_flux=heat_flux*0.5
print('# # The average heat flux is:',heat_flux,'(eV/ns)')
xlim(xmin=0.,xmax=20)
#ylim(ymin=-40000,ymax=40000)
xticks(range(0,21,5),fontproperties=font_song)
#yticks(range(-40000,40001,10000),fontproperties=font_song)
leg=legend(loc='upper left',fontsize=14)
leg.get_frame().set_linewidth(0.)
plt.xlabel('Time (ns)',fontproperties=font_song)
plt.ylabel('Flux (eV)',fontproperties=font_song)

subplot(2,2,4)
x_time_unzero=[]
flux_time1=[]
flux_time2=[]
for i in range(len(x_time)):
    if x_time[i]!=0:
        flux_time1.append(DATA_ave[N_group][i]/x_time[i])
        flux_time2.append(DATA_ave[N_group+1][i]/x_time[i])
        x_time_unzero.append(x_time[i])
plot(x_time_unzero,flux_time1,linewidth=2,label='flux-heat-source')
plot(x_time_unzero,flux_time2,linewidth=2,label='flux-heat-sink')
xlim(xmin=0.,xmax=20)
#ylim(ymin=-10000,ymax=10000)
xticks(range(0,21,5),fontproperties=font_song)
#yticks(range(-10000,10001,2000),fontproperties=font_song)
leg=legend(loc='upper right',fontsize=14)
leg.get_frame().set_linewidth(0.)
plt.xlabel('Time (ns)',fontproperties=font_song)
plt.ylabel('Flux/time (eV/ns)',fontproperties=font_song)

plt.tight_layout()
plt.savefig('NEMD.eps')

kappa=1.60217662*heat_flux/temp_grandient/area
print('Thermo conductivity is:',kappa,'(W/m/K)')
