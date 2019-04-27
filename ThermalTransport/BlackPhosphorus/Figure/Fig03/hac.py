import os
import sys
import numpy as np
from matplotlib.pylab import *
from matplotlib.font_manager import FontProperties   
font_song=FontProperties(fname=os.path.join(os.getcwd(),'Times-New-Roman.ttf'),size=16)

AddName=(sys.argv[1])
Chirality=(sys.argv[2])
# Add name: Jiang, Xu-2ns, Xu-5ns
# Add name: arm, zig
print('The add name is:',AddName,', and the chirality is:',Chirality)

TimeMax=2000  # 'ps'
TimeInt=500   # 'ps'
KapaAve=100   # 'W/mK'
KapaInt=50    # 'W/mK'

if Chirality=='arm':
    column=[8,9,10]
    if AddName=='Jiang':
        KapaAve=25    # 'W/mK'
        KapaInt=10    # 'W/mK'
    elif AddName=='Xu-2ns':
        pass
    elif AddName=='Xu-5ns':
        TimeMax=5000  # 'ps'
        TimeInt=1000  # 'ps'
    else:
        raise 'Wrong input add name!'
elif Chirality=='zig':
    column=[11,12,13]
    if AddName=='Jiang':
        pass
    elif AddName=='Xu-2ns':
        KapaAve=400   # 'W/mK'
        KapaInt=200   # 'W/mK'
    elif AddName=='Xu-5ns':
        TimeMax=5000  # 'ps'
        TimeInt=1000  # 'ps'
        KapaAve=400   # 'W/mK'
        KapaInt=200   # 'W/mK'
    else:
        raise 'Wrong input add name!'
else:
    raise 'Wrong input add name!'

frun=open('run-'+AddName+'.in','r')
for line in frun.readlines():
    str=line.split()
    if str and str[0]=='compute_hac' :
        hac_para=list(map(int,str[1:]))
frun.close()

DATA=np.loadtxt('hac-'+AddName+'.out')

N_freq=int(hac_para[1]/hac_para[2])
N_fram=int(len(DATA)/N_freq)
interval=100
print('Number of data lines per frame:',N_freq,', Number of frames:',N_fram,', Data sampling interval:',interval)

TIME=DATA[0:N_freq:interval,0]

fig,ax=plt.subplots()
plt.xlabel('Correlation time (ps)',fontproperties=font_song)
plt.ylabel(r'$\kappa$ $(Wm^{-1}K^{-1}$)',fontproperties=font_song)

ave_rtc=[0 for i in range(N_freq//interval)]

for i in range(N_fram):
    start=i*N_freq
    end =(i+1)*N_freq
    rtc_i=DATA[start:end:interval,column[0]]+DATA[start:end:interval,column[1]]+DATA[start:end:interval,column[2]]
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

xlim(xmin=0.,xmax=TimeMax)
ylim(ymin=0.,ymax=KapaAve*2)
xticks(range(0,TimeMax+1,TimeInt),fontproperties=font_song)
yticks(range(0,KapaAve*2+1,KapaInt),fontproperties=font_song)
#font_dict={'family':font_song.get_family(),'size':16}
#gca().set_xticklabels(gca().get_xticks(),font_dict)
#gca().set_xticklabels([],font_dict)       # set the xticks is none.
#leg1=legend(['RTC'],loc='upper left',handlelength=1,fontsize=14)
leg=legend(loc='upper left',fontsize=14)
leg.get_frame().set_linewidth(0.)

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
print ('Average of the last 25% TC data:',result_rtc,', Its standard seviation:',result_std)

plt.tight_layout()
fig.savefig('RTC-'+Chirality+'-'+AddName+'.eps')
