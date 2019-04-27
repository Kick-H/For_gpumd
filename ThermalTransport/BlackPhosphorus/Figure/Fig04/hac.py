import os
import sys
import numpy as np
from matplotlib.pylab import *
from matplotlib.font_manager import FontProperties   
font_song=FontProperties(fname=os.path.join(os.getcwd(),'Times-New-Roman.ttf'),size=9)

DATA=np.loadtxt('kappa-HNEMD.txt')
TIME=[]
interval=10
for i in range(int(len(DATA)/interval)):
    TIME.append((i+1)*(10/len(DATA)*interval))  # the run time is 10 ns.

# SW1 armchair and zigzag.
plt.subplot(221)
plt.xlabel('Time (ns)',fontproperties=font_song)
plt.ylabel(r'$\kappa$ $(Wm^{-1}K^{-1}$)',fontproperties=font_song)
plt.plot(TIME,DATA[0:len(DATA):interval,0],'Gray',linewidth=0.5,label='TC_SW1_arm')
plt.plot(TIME,DATA[0:len(DATA):interval,1],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,2],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,3],'Gray',linewidth=0.5)
ave_rtc=(DATA[0:len(DATA):interval,0]+DATA[0:len(DATA):interval,1]+DATA[0:len(DATA):interval,2]+DATA[0:len(DATA):interval,3])/4
plt.plot(TIME,ave_rtc,'k',linewidth=2,label=r'TC_SW1_arm$_{ave}$')
print ('TC_SW1_arm',ave_rtc[len(ave_rtc)-1])
plt.plot(TIME,DATA[0:len(DATA):interval,4],'Gray',linewidth=0.5,label='TC_SW1_zig')
plt.plot(TIME,DATA[0:len(DATA):interval,5],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,6],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,7],'Gray',linewidth=0.5)
ave_rtc=(DATA[0:len(DATA):interval,4]+DATA[0:len(DATA):interval,5]+DATA[0:len(DATA):interval,6]+DATA[0:len(DATA):interval,7])/4
plt.plot(TIME,ave_rtc,'r',linewidth=2,label=r'TC_SW1_zig$_{ave}$')
xlim(xmin=0.,xmax=10)
ylim(ymin=0.,ymax=200)
xticks(range(0,11,2),fontproperties=font_song)
yticks(range(0,201,50),fontproperties=font_song)
leg=legend(loc='upper right',fontsize=6)
leg.get_frame().set_linewidth(0.)
print ('TC_SW1_zig',ave_rtc[len(ave_rtc)-1])

# SW1 kappa_xy.
plt.subplot(222)
plt.xlabel('Time (ns)',fontproperties=font_song)
plt.ylabel(r'$\kappa$ $(Wm^{-1}K^{-1}$)',fontproperties=font_song)
plt.plot(TIME,DATA[0:len(DATA):interval,16],'Gray',linewidth=0.5,label='TC_SW1_xy')
plt.plot(TIME,DATA[0:len(DATA):interval,17],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,18],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,19],'Gray',linewidth=0.5)
ave_rtc=(DATA[0:len(DATA):interval,16]+DATA[0:len(DATA):interval,17]+DATA[0:len(DATA):interval,18]+DATA[0:len(DATA):interval,19])/4
plt.plot(TIME,ave_rtc,'b',linewidth=2,label=r'TC_SW1_xy$_{ave}$')
xlim(xmin=0.,xmax=10)
ylim(ymin=-50,ymax=50)
xticks(range(0,11,2),fontproperties=font_song)
yticks([-50,0,50],fontproperties=font_song)
leg=legend(loc='upper right',fontsize=6)
leg.get_frame().set_linewidth(0.)
print ('TC_SW1_arm',ave_rtc[len(ave_rtc)-1])

# SW1 armchair and zigzag.
plt.subplot(223)
plt.xlabel('Time (ns)',fontproperties=font_song)
plt.ylabel(r'$\kappa$ $(Wm^{-1}K^{-1}$)',fontproperties=font_song)
plt.plot(TIME,DATA[0:len(DATA):interval,8],'Gray',linewidth=0.5,label='TC_SW1_arm')
plt.plot(TIME,DATA[0:len(DATA):interval,9],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,10],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,11],'Gray',linewidth=0.5)
ave_rtc=(DATA[0:len(DATA):interval,8]+DATA[0:len(DATA):interval,9]+DATA[0:len(DATA):interval,10]+DATA[0:len(DATA):interval,11])/4
plt.plot(TIME,ave_rtc,'k',linewidth=2,label=r'TC_SW2_zig$_{ave}$')
print ('TC_SW2_zig',ave_rtc[len(ave_rtc)-1])
plt.plot(TIME,DATA[0:len(DATA):interval,12],'Gray',linewidth=0.5,label='TC_SW2_zig')
plt.plot(TIME,DATA[0:len(DATA):interval,13],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,14],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,15],'Gray',linewidth=0.5)
ave_rtc=(DATA[0:len(DATA):interval,12]+DATA[0:len(DATA):interval,13]+DATA[0:len(DATA):interval,14]+DATA[0:len(DATA):interval,15])/4
plt.plot(TIME,ave_rtc,'r',linewidth=2,label=r'TC_SW2_arm$_{ave}$')
xlim(xmin=0.,xmax=10)
ylim(ymin=0.,ymax=600)
xticks(range(0,11,2),fontproperties=font_song)
yticks(range(0,601,200),fontproperties=font_song)
leg=legend(loc='upper right',fontsize=6)
leg.get_frame().set_linewidth(0.)
print ('TC_SW2_arm',ave_rtc[len(ave_rtc)-1])

# SW1 armchair and zigzag.
plt.subplot(224)
plt.xlabel('Time (ns)',fontproperties=font_song)
plt.ylabel(r'$\kappa$ $(Wm^{-1}K^{-1}$)',fontproperties=font_song)
plt.plot(TIME,DATA[0:len(DATA):interval,20],'Gray',linewidth=0.5,label='TC_SW1_InPlane')
plt.plot(TIME,DATA[0:len(DATA):interval,21],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,22],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,23],'Gray',linewidth=0.5)
ave_rtc=(DATA[0:len(DATA):interval,20]+DATA[0:len(DATA):interval,21]+DATA[0:len(DATA):interval,22]+DATA[0:len(DATA):interval,23])/4
plt.plot(TIME,ave_rtc,'g',linewidth=2,label=r'TC_SW1_InPlane$_{ave}$')
print ('TC_SW1_InPlane',ave_rtc[len(ave_rtc)-1])
plt.plot(TIME,DATA[0:len(DATA):interval,24],'Gray',linewidth=0.5,label='TC_SW1_OutOfPlane')
plt.plot(TIME,DATA[0:len(DATA):interval,25],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,26],'Gray',linewidth=0.5)
plt.plot(TIME,DATA[0:len(DATA):interval,27],'Gray',linewidth=0.5)
ave_rtc=(DATA[0:len(DATA):interval,24]+DATA[0:len(DATA):interval,25]+DATA[0:len(DATA):interval,26]+DATA[0:len(DATA):interval,27])/4
plt.plot(TIME,ave_rtc,'y',linewidth=2,label=r'TC_SW1_OutOfPlane$_{ave}$')
xlim(xmin=0.,xmax=10)
ylim(ymin=0.,ymax=120)
xticks(range(0,11,2),fontproperties=font_song)
yticks(range(0,120,50),fontproperties=font_song)
leg=legend(loc='upper right',fontsize=6)
leg.get_frame().set_linewidth(0.)
print ('TC_SW1_OutOfPlane',ave_rtc[len(ave_rtc)-1])
plt.tight_layout()
plt.savefig('TC-SW1-HNEMD-InOut.eps')
plt.close()
