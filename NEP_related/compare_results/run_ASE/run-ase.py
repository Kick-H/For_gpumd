from pynep.calculate import NEP
from ase.io import read, write
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
#from ase.Atoms import get_stress

def get_nep_predict(file):
    data = np.loadtxt(file)
    use_cloumn = int(data.shape[1]/2)
    return data[:, :use_cloumn].reshape(-1)


def plot_compare(d1, d2, fstr):
    fig = plt.figure()
    #plt.xticks(fontname="Arial", weight='bold')
    plt.title(f"ASE {fstr} vs NEP {fstr}", fontsize=16)
    # d1 = d1 - np.mean(d1)
    # d2 = d2 - np.mean(d2)
    ax = plt.gca()
    ax.set_aspect(1)
    xmajorLocator = ticker.MaxNLocator(5)
    ymajorLocator = ticker.MaxNLocator(5)
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.yaxis.set_major_locator(ymajorLocator)
    ymajorFormatter = ticker.FormatStrFormatter('%.2f')
    xmajorFormatter = ticker.FormatStrFormatter('%.2f')
    ax.xaxis.set_major_formatter(xmajorFormatter)
    ax.yaxis.set_major_formatter(ymajorFormatter)

    ax.set_xlabel(f'ASE {fstr} (*/atom)', fontsize=14)
    ax.set_ylabel(f'NEP {fstr} (*/atom)', fontsize=14)

    ax.spines['bottom'].set_linewidth(3)
    ax.spines['left'].set_linewidth(3)
    ax.spines['right'].set_linewidth(3)
    ax.spines['top'].set_linewidth(3)
    ax.tick_params(labelsize=16)

    plt.plot([np.min(d1), np.max(d1)], [np.min(d1), np.max(d1)],
            color='black',linewidth=3,linestyle='--',)
    plt.scatter(d1, d2, zorder=200)
    m1 = min(np.min(d1), np.min(d2))
    m2 = max(np.max(d1), np.max(d2))
    ax.set_xlim(m1, m2)
    ax.set_ylim(m1, m2)

    rmse = np.sqrt(np.mean((d1-d2)**2))
    plt.text(np.min(d1) * 0.85 + np.max(d1) * 0.15,
             np.min(d2) * 0.15 + np.max(d1) * 0.85,
             "RMSE: {:.3f} eV/atom".format(rmse), fontsize=14)
    plt.savefig(f'{fstr}.png')
    return fig

dname = '../run_NEP'
a = read(f'{dname}/train.xyz', ':', format='extxyz')
calc = NEP(f'{dname}/nep.txt')

e_ase, f_ase, v_ase, s_ase = [], [], [], []
e_dft, f_dft, v_dft, s_dft = [], [], [], []
e_nep, f_nep, v_nep, s_nep = [], [], [], []

for i, ai in enumerate(a):

    vol = ai.get_volume()
    ai.set_calculator(calc)

    e_ase.append(ai.get_potential_energy() / len(ai))
    f_ase.append(ai.get_forces().reshape(-1))
    v_ase.append(ai.get_stress() * vol / len(ai))
    s_ase.append(ai.get_stress())

    e_dft.append(ai.info['energy'] / len(ai))
    f_dft.append(ai.get_array('forces').reshape(-1))
    vv = ai.info['virial'].reshape(-1) / -len(ai)
    v_dft.append([vv[0], vv[4], vv[8], vv[1], vv[5], vv[2]])

    #print(f_ase[0]-f_dft[0])
    #print(e_ase[0]-e_dft[0])
    #print(v_ase[0]-v_dft[0])
    #v_ase.append(ai.get_stress() * v / len(ai))

e_ase = np.array(e_ase)
f_ase = np.concatenate(f_ase)
v_ase = np.concatenate(v_ase)*-1
s_ase = np.concatenate(s_ase)*160.21766208*-1

e_dft = np.array(e_dft)
f_dft = np.concatenate(f_dft)
v_dft = np.concatenate(v_dft)
# s_dft = np.concatenate(s_dft)

e_nep = get_nep_predict(f'{dname}/energy_train.out')
f_nep = get_nep_predict(f'{dname}/force_train.out')
v_nep = get_nep_predict(f'{dname}/virial_train.out')
s_nep = get_nep_predict(f'{dname}/stress_train.out')

plot_compare(e_ase, e_nep, "energy")
plot_compare(f_ase, f_nep, "force")
plot_compare(v_ase, v_nep, "virial")
plot_compare(s_ase, s_nep, "stress")

print(s_ase[:10], s_nep[:10], s_nep[:10]/s_ase[:10])