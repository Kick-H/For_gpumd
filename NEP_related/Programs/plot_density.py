from ase.io import read, write
import numpy as np
import sys

def density_SI():

    Na = 6.02214076 * 10**23 # Avogadro constant
    A3tocm3 = 1e8**3       # A^3 to cm^3
    return A3tocm3/Na

fxyz = "../PRL-1888"
fram = read(f"{fxyz}/train.xyz", ":")
element = {'H':1, 'O':8, 'Mo':42, 'S':16}

den_str = "#nframe densitys"
for i, fi in enumerate(fram):
    nat = fi.get_global_number_of_atoms()
    volume = fi.get_volume()
    masses = fi.get_masses()
    atypes = fi.get_chemical_symbols()
    density = np.sum(masses) / volume * density_SI()
    for i in range(nat):
        den_str += f"\n{i} {density} {element[atypes[i]]}"

fout = open(f"den-liquid.dat", 'w')
fout.write(den_str)
fout.close()
