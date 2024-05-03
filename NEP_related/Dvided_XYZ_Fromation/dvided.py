from ase.formula import Formula
from ase.io import read, write
import numpy as np
import sys

def get_atom_symble(atom):
    atom_symb = atom.symbols
    form_symb = atom_symb.formula
    form_keys = list(form_symb.count().keys())
    form_name = "".join(form_keys)
    return form_name

if __name__=='__main__':

    in_xyz = "DEEP2XYZ.xyz"
    atoms = read(in_xyz, index=':', format='extxyz')

    dvi_atoms = {}
    for atom in atoms:
        label = get_atom_symble(atom)
        try:
            dvi_atoms[label].append(atom)
        except:
            dvi_atoms[label] = [atom]

    for label in dvi_atoms:
        write(f"{label}.xyz", dvi_atoms[label],
              format="extxyz")
