import numpy as np
import matplotlib.pyplot as plt
from thermo.gpumd.data import load_kappa, load_shc
from thermo.gpumd.calc import running_ave, hnemd_spectral_kappa
import sys

def calc_shc_hnemd(path, Fe=0.0001, Nc=[100], num_omega=[100], T=300, V=1, rnum=1):
    shc = load_shc(Nc=Nc, num_omega=num_omega, directory=path)
    if V == 'self':
        V = read(f"{path}/model.xyz", format="extxyz").get_volume()
    for keys in shc:
        hnemd_spectral_kappa(shc[keys], Fe, T, V)
        shc[keys]['kwi'][shc[keys]['kwi'] < 0] = 0
        shc[keys]['kwo'][shc[keys]['kwo'] < 0] = 0
        shc[keys]['kw'] = shc[keys]['kwi'] + shc[keys]['kwo']
    shc_tol = np.zeros((len(shc["run0"]["kw"]), rnum))
    i = 0
    for keys in shc:
        shc_tol[:,i] = shc[keys]['kw']
        i += 1
    shc_tol_ave = np.average(shc_tol, axis = 1)
    shc_output = dict()
    shc_output["nu"] = shc["run0"]["nu"]
    shc_output["tol"] = shc_tol
    shc_output["tol_ave"] = shc_tol_ave
    return shc_output


run = { "temp":           300,
        "compute_hnemd": [1000,0,0.00001,0],
        "compute_shc":   [2,250,1,1000,400],
        "run":            1000000 }


ver = sys.argv[1]

plt.figure(figsize=(7, 3))
cl = ['r', 'g', 'b', 'k']

for gn in [0, 1]:

    shc1 = calc_shc_hnemd(f"ver-{ver}/k_shc_{gn}", Fe=run['compute_hnemd'][2],
              Nc=[run['compute_shc'][1]]*1,
              num_omega=[run['compute_shc'][3]]*1,
              T=run['temp'], V=245.951*255.6*3.35, rnum=1)

    shc2 = calc_shc_hnemd(f"ver-{ver}/o_shc_{gn}", Fe=run['compute_hnemd'][2],
              Nc=[run['compute_shc'][1]]*1,
              num_omega=[run['compute_shc'][3]]*1,
              T=run['temp'], V=245.951*255.6*3.35, rnum=1)

    shc3 = calc_shc_hnemd(f"ver-{ver}/shc_-1_{gn}", Fe=run['compute_hnemd'][2],
              Nc=[run['compute_shc'][1]]*1,
              num_omega=[run['compute_shc'][3]]*1,
              T=run['temp'], V=245.951*255.6*3.35, rnum=1)

    plt.subplot(1, 2, gn+1)
    plt.plot(shc1['nu'], shc1['tol_ave'], linewidth=3, color='r', label=f"modify {ver}: group 0 {gn}")
    plt.plot(shc2['nu'], shc2['tol_ave'], linewidth=2, color='b', label=f"origin {ver}: group 0 {gn}")
    plt.plot(shc3['nu'], shc3['tol_ave'], linewidth=1, color='g', label=f"modify {ver}: group 0 -1 ({gn})")
    #plt.xlim([0, 60])
    #gca().set_xticks(linspace(0, 25, 6))
    #plt.ylim([0, 0.8])
    #gca().set_yticks(linspace(0, 0.8, 5))
    plt.ylabel(r'$\kappa$($\omega$) (W m$^{-1}$ K$^{-1}$ THz$^{-1}$)')
    plt.xlabel(r'$\omega$/2$\pi$ (THz)')
    plt.legend()

plt.tight_layout()
plt.savefig(f'gn-{ver}.png', dpi=300)
