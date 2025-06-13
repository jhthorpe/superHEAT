# geometry.py 
#
# Defines the molecular geometry class and methods 
# 
#
#
# NOTES:
# March 25, 2025 @ ANL : JHT created. Discrepancy between dihedral here and in CFOUR? 
# 
#

import numpy as np
import math

#---------------------------------------
# Geometry Class
#
# NOTE: these values are always in Bohr
# 
# Key User Features:
#   Return list of atoms: atom_list()
#   Distance between two atoms : dist(i,j)
#   Angle between three atoms  : angle(i,j,k)
#   Diheydral between four atoms : diheydral(i,j,k,l)
#
# Datastructure:
#   name  - string 
#   atoms - array of atom names (case insensitive)
#   xyz   - np array of the x,y,z coordinates of each atom in Bohrs 
#
class Geometry:

    def __init__(self, name=None, atoms=None, xyz=None):
        self.name = name
        self.atoms = atoms
        self.xyz = np.array(xyz)

        for i, atom in enumerate(self.atoms): 
            self.atoms[i] = atom.upper() 

    #Returns the distance in Bohrs
    def dist(self, i, j):
        ij = np.subtract(self.xyz[i], self.xyz[j])
        return np.linalg.norm(ij) 


    #Returns the angle in radians (use np.degrees() to convert)
    # Note: 
    def angle(self, i, j, k):
        ji = np.subtract(self.xyz[i], self.xyz[j])
        jk = np.subtract(self.xyz[k], self.xyz[j])
        return angle_(ji, jk) 

    #Returns the dihedral angle in radians 
    def dihedral(self, i, j, k, l):
        ji = -1.0 * np.subtract(self.xyz[j], self.xyz[i])
        ji = np.subtract(self.xyz[j], self.xyz[i])
        jk = np.subtract(self.xyz[k], self.xyz[j])
        kl = np.subtract(self.xyz[l], self.xyz[k])
        return dihedral_(ji, jk, kl)


#angle between two vectors
def angle_(v, w):
    return np.arccos(np.clip(np.dot(v, w)/(np.linalg.norm(v) * np.linalg.norm(w)), -1.0, 1.0)) 

#dihedral between three vectors assuming b contains a common point with a and c
def dihedral_(a, b, c):
    axb = np.cross(a, b)
    bxc = np.cross(b, c)
    return angle_(axb, bxc)
        

