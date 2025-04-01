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
from geometry import *

#testing
geom = Geometry('test', ['C','H', 'H', 'H'], dtest) 

#geom_d120 = Geometry('test', ['C','H', 'H', 'H'], np.array([[-0.05447514, 0.00843423,0.00000000],[ 0.22598679, 1.81988597, 0.00000000],[ 0.21131969,-0.96015546,-1.53336343],[ 0.21131969,-0.96015546, 1.53336343]], dtype=np.float64))



print(geom.name)
print(geom.atoms)
print(geom.xyz)
print("distance is :", geom.dist(0, 1))
print("distance is :", geom.dist(0, 2))
print("distance is :", geom.dist(0, 3))
print("distance is :", geom.dist(1, 2))
print("distance is :", geom.dist(1, 3))
print("distance is :", geom.dist(2, 3))
print("angle is :", np.degrees(geom.angle(1, 0, 2)))
print("angle is :", np.degrees(geom.angle(1, 0, 3)))
print("angle is :", np.degrees(geom.angle(2, 0, 3))) 
print("dehedral is :", np.degrees(geom.dihedral(1, 0, 2, 3)))
print("dehedral is :", np.degrees(geom.dihedral(1, 0, 3, 2)))
