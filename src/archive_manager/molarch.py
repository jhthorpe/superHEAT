# molarch.py 
#
# A python module for managing the molecular archive. This contains 
# the following classes:
#
# Geometry:
#   x,y,z coordinates of each atom
#
# Molecule:
#   Features of each molecule plus a dictionary of geometries
#
# Molecule_Archive:
#   Manages the archive of molecules
#
# NOTES:
# March 25, 2025 : JHT, created 
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
        return math.sqrt((self.xyz[i,0] - self.xyz[j,0])**2.0 + (self.xyz[i,1] - self.xyz[j,1])**2.0 + (self.xyz[i,2] - self.xyz[j,2])**2.0) 

    #Returns the angle in radians (use np.degrees() to convert)
    # Note: 
    def angle(self, i, j, k):
        ij = np.array([self.xyz[j,0] - self.xyz[i,0], self.xyz[j,1] - self.xyz[i,1], self.xyz[j,2] - self.xyz[i, 2]]) 
        jk = np.array([self.xyz[k,0] - self.xyz[j,0], self.xyz[k,1] - self.xyz[j,1], self.xyz[k,2] - self.xyz[j, 2]]) 
        ij = ij / np.linalg.norm(ij)
        jk = jk / np.linalg.norm(jk)
        return np.arccos(np.clip(np.dot(ij, jk), -1.0, 1.0))

    #Returns the dihedral angle in radians 
    def dihedral(self, i, j, k, l):
        ij = np.array([self.xyz[j,0] - self.xyz[i,0], self.xyz[j,1] - self.xyz[i,1], self.xyz[j,2] - self.xyz[i, 2]]) 
        jk = np.array([self.xyz[k,0] - self.xyz[j,0], self.xyz[k,1] - self.xyz[j,1], self.xyz[k,2] - self.xyz[j, 2]])
        kl = np.array([self.xyz[l,0] - self.xyz[k,0], self.xyz[l,1] - self.xyz[k,1], self.xyz[l,2] - self.xyz[k, 2]])
        xijk = np.array([ij[1]*jk[2] - ij[2]*jk[1], ij[0]*jk[2] - ij[2]*jk[0], ij[0]*jk[1] - ij[1]*jk[0]])
        xjkl = np.array([jk[1]*kl[2] - jk[2]*kl[1], jk[0]*kl[2] - jk[2]*kl[0], jk[0]*kl[1] - jk[1]*kl[0]])
#        xijk = np.array([-ij[1]*jk[2] + ij[2]*jk[1], -ij[0]*jk[2] + ij[2]*jk[0], -ij[0]*jk[1] + ij[1]*jk[0]])
#        xjkl = np.array([-jk[1]*kl[2] + jk[2]*kl[1], -jk[0]*kl[2] + jk[2]*kl[0], -jk[0]*kl[1] + jk[1]*kl[0]])
        return np.arccos(np.clip(np.dot(xijk, xjkl)/(np.linalg.norm(xijk) * np.linalg.norm(xjkl)), -1., 1.))


#Molecule Class


#Molecule_Archive Class




#testing
geom = Geometry('test', ['C','H', 'H', 'H'], np.array([[-0.05447514, 0.00843423,0.00000000],[ 0.22598679, 1.81988597, 0.00000000],[ 0.21131969,-0.96015546,-1.53336343],[ 0.21131969,-0.96015546, 1.53336343]], dtype=np.float64))

print(geom.name)
print(geom.atoms)
print(geom.xyz)
print("distance is :", geom.dist(0, 1))
print("distance is :", geom.dist(1, 2))
print("angle is :", geom.angle(1, 0, 2), np.degrees(geom.angle(1, 0, 2)))
print("dehedral is :", geom.dihedral(1,0,2,3), np.degrees(geom.dihedral(1, 0, 2, 3)))
print("dehedral is :", geom.dihedral(1,2,0,3), np.degrees(geom.dihedral(1, 2, 0, 3)))
print("dehedral is :", geom.dihedral(1,3,0,2), np.degrees(geom.dihedral(1, 3, 0, 2)))
print("dehedral is :", geom.dihedral(1,3,2,0), np.degrees(geom.dihedral(1, 3, 2, 0)))
