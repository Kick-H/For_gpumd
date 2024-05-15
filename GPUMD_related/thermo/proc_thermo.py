from ase.io import read
import os
import numpy as np
import matplotlib.pyplot as plt


def load_thermo(filename: str = "thermo.out", directory: str = None) -> dict[str, np.ndarray]:
    """
    Loads data from thermo.out GPUMD output file.

    Args:
        filename: Name of thermal data file
        directory: Directory to load thermal data file from

    Returns:
        Dict containing the data from thermo.out. Units are [temperature
         -> K], [K, U -> eV], [Px, Py, Pz, Pyz, Pxz, Pxy -> GPa],
         [Lx, Ly, Lz, ax, ay, az, bx, by, bz, cx, cy, cz -> A]
    """
    thermo_path = os.path.join(directory, filename)
    data = np.loadtxt(thermo_path)
    labels = ['temperature', 'K', 'U', 'Px', 'Py', 'Pz', 'Pyz', 'Pxz', 'Pxy']
    if data.shape[1] == 12:  # orthogonal
        labels += ['Lx', 'Ly', 'Lz']
    elif data.shape[1] == 18:  # triclinic
        labels += ['ax', 'ay', 'az', 'bx', 'by', 'bz', 'cx', 'cy', 'cz']
    else:
        raise ValueError(f"The file {filename} is not a valid thermo.out file.")

    out_data = dict()
    for i in range(data.shape[1]):
        out_data[labels[i]] = data[:,i]

    return out_data


def get_dens(vol, mol_mass):
    N_A = 6.02214076e23
    nm_cm_3 = 1e-7**3            # nm to cm
    #      _________g_________   _____cm^3____
    dens = mol_mass/N_A / (vol*nm_cm_3)
    return dens     # g/nm^3


def proc_thermo(dirs, delt_block=500, fin='thermo.out', jump_line=100):

    data = load_thermo(filename=fin, directory=dirs)
    atom = read(f'{dirs}/model.xyz', format='extxyz')
    natoms = atom.get_global_number_of_atoms()
    data['Volume'] = data['Lx']*data['Ly']*data['Lz']/1000
    data['Energy'] = data['U'] # + data['K']
    data['Masses'] = np.array([np.sum(atom.get_masses())] * len(data['Volume']))
    data['Density'] = get_dens(data['Volume'], data['Masses'])
    for ndir in data:
        data[ndir] = data[ndir][jump_line:]

    # display keys of the data.
    # print(data.keys())

    if delt_block != 0:
        db = delt_block
        nb = round(len(data['U'])/db)
    else:
        db = data['temperature'].shape[0]
        nb = 1

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


def output_data(ave_data, plist=['temperature'], out_data=True):
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

for mi in [1]:
    name = f"MBpol-{mi}-280"
    fdir = f"../{name}"
    outfile = f"{name}.dat"
    out_data = proc_thermo(fdir, delt_block=500, fin='thermo.out', jump_line=0)
    ave_data = get_ave_data(out_data)
    plist = ['temperature', 'Energy', 'Volume', 'Density']
    plist = ['temperature', 'Density']
    output_data(ave_data, plist=plist, out_data=outfile)

