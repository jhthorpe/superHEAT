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

#Molecule Class


#Molecule_Archive Class

d80_xyz = np.array([[-0.14063595,    -0.08271057,    -0.00000000], [ 0.78861218,    -1.66274672,    -0.00000000], [ 0.44295800,    1.32378367,     1.02039617], [ 0.44295800,     1.32378367,    -1.02039617]])

d150_xyz = np.array([[-0.05447514, 0.00843423,0.00000000],[ 0.22598679, 1.81988597, 0.00000000],[ 0.21131969,-0.96015546,-1.53336343],[ 0.21131969,-0.96015546, 1.53336343]])

dtest = np.array([[-0.01426719251500,        -0.05324588734734,        -0.00000000000000], [-0.01426719251500,        -0.05324588734734,         1.83303472504763],  [ 1.57318744539527,        -0.05324588734734,        -0.91651736252381], [-1.38904323630072,         0.74048143160779,        -0.91651736252381]])

#angle between two vectors
def angle_(v, w):
    return np.arccos(np.clip(np.dot(v, w)/(np.linalg.norm(v) * np.linalg.norm(w)), -1.0, 1.0)) 

#dihedral between three vectors assuming b contains a common point with a and c
def dihedral_(a, b, c):
    axb = np.cross(a, b)
    bxc = np.cross(b, c)
    return angle_(axb, bxc)
        

