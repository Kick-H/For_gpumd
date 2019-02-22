import os
import numpy as np
from matplotlib.pylab import *
from matplotlib.font_manager import FontProperties   
font_song=FontProperties(fname=os.path.join(os.getcwd(),'Times-New-Roman.ttf'),size=16)

frun=open('run.in','r')
for line in frun.readlines():
    str=line.split() 
    if str and str[0]=='compute_hac' :
        hac_para=list(map(int,str[1:]))
frun.close()

DATA=np.loadtxt('hac.out')

N_freq=int(hac_para[1]/hac_para[2])
print('Number of data lines per frame:',N_freq)
N_fram=int(len(DATA)/N_freq)
print('Number of frames:',N_fram)
interval=100
print('Data sampling interval:',interval)

TIME=DATA[0:N_freq:interval,0]

fig,ax=plt.subplots()
plt.xlabel('Correlation time (ps)',fontproperties=font_song)
plt.ylabel(r'$\kappa$ (W/mK)',fontproperties=font_song)

ave_rtc=[0 for i in range(N_freq//interval)]

for i in range(N_fram):
    start=i*N_freq
    end =(i+1)*N_freq
    rtc_i=DATA[start:end:interval,8]+DATA[start:end:interval,9]+DATA[start:end:interval,10]
    if i==0:
        ax.plot(TIME,rtc_i,'Gray',linewidth=1,label='RTC')
    else:
        ax.plot(TIME,rtc_i,'Gray',linewidth=1)
    ave_rtc+=rtc_i
ave_rtc=ave_rtc/N_fram
ax.plot(TIME,ave_rtc,'r',linewidth=4,label=r'RTC$_{ave}$')

std_rtc=[]
for j in range(N_freq//interval):
    stdat=[]
    for k in range(N_fram):
        stdat.append(DATA[k*N_freq+j*interval,8]+DATA[k*N_freq+j*interval,9]+DATA[k*N_freq+j*interval,10])
    std_rtc.append(np.std(stdat,ddof=0)/math.sqrt(N_fram))
ax.plot(TIME,ave_rtc+std_rtc,'k--',linewidth=2,label=r'RTC$_{stdev}$')
ax.plot(TIME,ave_rtc-std_rtc,'k--',linewidth=2)

xlim(xmin=0.,xmax=5000.)
ylim(ymin=0.,ymax=200.)
xticks(range(0,5001,1000),fontproperties=font_song)
yticks(range(0,201,50),fontproperties=font_song)
leg=legend(loc='upper left',fontsize=14)
leg.get_frame().set_linewidth(0.)
fig.savefig('RTC.eps')

# Get the average of the last 25% data
percent=0.75
result_rtc=0.
result_std=0.
flag=0
for i in range(int(len(ave_rtc)*percent),len(ave_rtc)):
    result_rtc+=ave_rtc[i]
    flag+=1
result_rtc=result_rtc/flag

flag=0
for i in range(int(len(std_rtc)*percent),len(std_rtc)):
    result_std+=std_rtc[i]
    flag+=1
result_std=result_std/flag
print ('Average of the last 25% TC data:',result_rtc)
print ('Its standard seviation:',result_std)
