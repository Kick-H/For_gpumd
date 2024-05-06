from gpyumd.load import load_thermo
from ase.io import read
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_dens(vol, nat):
    mol_mass = 1.008*2+15.999    # H_2O
    N_A = 6.02214076e23
    nm_cm_3 = 1e-7**3            # nm to cm
    n_mols = nat/3
    #      _________g_________   _____cm^3____
    dens = n_mols*mol_mass/N_A / (vol*nm_cm_3)
    return dens     # g/nm^3


def proc_thermo(dirs, delt_block=500, fin='thermo.out'):

    data = load_thermo(filename=fin, directory=dirs)
    if delt_block != 0:
        db = delt_block
        nb = round(len(data['U'])/db)
    else:
        db = data.shape[0]
        nb = 1
    atom = read(f'{dirs}/model.xyz', format='extxyz')
    natoms = atom.get_global_number_of_atoms()
    data['Volume'] = data['Lx']*data['Ly']*data['Lz']/1000
    data['Energy'] = data['U'] # + data['K']
    data['Density'] = get_dens(data['Volume'], natoms)

    out_data = {}
    for i in range(nb):
        sta = i * db
        end = (i+1) * db
        if i == nb-1:
            end = len(data['U'])
        out_data[i] = {}
        for ks in data:
            out_data[i][ks] = data[ks][sta:end]

    return out_data


def get_ave_data(data):
    out_data = dict()
    for ti in data:
        out_data[ti] = {}
        for dn in data[ti].keys():
            data_dn = data[ti][dn]
            sta = int(len(data_dn)/2)
            end = len(data_dn)
            out_data[ti][dn] = np.mean(data_dn[sta:end])
            out_data[ti][f"{dn}_std"] = np.std(data_dn[sta:end])
    return out_data
    #labels = open()


def plot_thermo(ave_data, plist=['temperature'], out_data=True):
    plot_data = {'num':[]}
    for i, pi in enumerate(plist):
        plot_data[pi] = []
        pstd = f"{pi}_std"
        plot_data[pstd] = []
        for di in ave_data:
            plot_data[pi].append(ave_data[di][pi])
            plot_data[pstd].append(ave_data[di][pstd])
            if len(plot_data['num']) < len(plot_data[pi]):
                plot_data['num'].append(di)

    #nx = int(np.sqrt(plist)) + 1
    #ny = int(len(plist)/nx) + 1
    # fig, axs = plt.subplots(nx, ny) #, figsize=(12,10)
    # for i, pi in enumerate(plist):
    #     ax, ay = i%nx, i//nx
    #     axs[0, 0].errorbar(datax, datay, yerr=stdy, fmt="o",
    #         ecolor='k', elinewidth=2, mfc=color_list[ci], ms=10,
    #         mec='k', mew=1, alpha=1, label=f"NEP-MB-pol({i})",
    #         capsize=5, capthick=3, linestyle="none")
    #     axs[ax, ay]
    with open(out_data, 'w') as fo:
        out_str = "num"
        for pi in plist:
            pstd = f"{pi}_std"
            out_str += f" {pi} {pstd}"
        out_str += "\n"
        for i, ni in enumerate(plot_data['num']):
            out_str += f"{ni}"
            for pi in plist:
                pstd = f"{pi}_std"
                out_str += f" {round(plot_data[pi][i], 6)} {round(plot_data[pstd][i], 8)}"
            out_str += "\n"
        fo.write(out_str)


for mi in [6]:
    name = f"{mi}-300"
    fdir = f"../{name}"
    outfile = f"{name}.dat"
    out_data = proc_thermo(fdir, delt_block=500, fin='thermo.out')
    ave_data = get_ave_data(out_data)
    plist = ['temperature', 'Energy', 'Volume', 'Density']
    plist = ['temperature', 'Density']
    plot_thermo(ave_data, plist=plist, out_data=outfile)
