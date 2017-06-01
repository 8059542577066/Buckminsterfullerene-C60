import os
from fetch import *


fileName = "c60.txt"

if os.path.isfile(fileName):
    pass
else:
    getFileAs(fileName)

with open(fileName, "r") as file:
    lines = file.readlines()


i = 0
c = 0

while lines[i] != len(lines):
    if len(lines[i]) >= 5 and lines[i][:5] == "loop_":
        i += 1
        while len(lines[i]) >= 16 and lines[i][:16] == "_chem_comp_atom.":
            i += 1
            c += 1
        break
    i += 1

atoms = []

while len(lines[i].split()) == c:
    atoms.append(lines[i].split()[12:15])
    i += 1


c = 0

while lines[i] != len(lines):
    if len(lines[i]) >= 5 and lines[i][:5] == "loop_":
        i += 1
        while len(lines[i]) >= 16 and lines[i][:16] == "_chem_comp_bond.":
            i += 1
            c += 1
        break
    i += 1

bonds = []

while len(lines[i].split()) == c:
    bonds.append(lines[i].split()[1:3])
    i += 1


c60_atoms = [tuple([float(xyz) for xyz in atom]) for atom in atoms]
c60_bonds = [tuple([int(atom[1:]) - 1 for atom in bond]) for bond in bonds]
