#*************************************************************
#
# basis.py 
#	JHT, July 9, 2023, Dallas, TX
#	-- created
# 
# This module defined the basis and basis_set classes, and construsts the global
# BASIS object which defines all default basis tracked within this package
# 
# Basis_Set:
#	Defines a particular basis set, with extra info for sorting as requested
#
# Basis:
#	A collection of basis_set objects.
#
# BASIS:
# 	A global Basis object that contains all the 
#       basis sets registered by default in this package 
#
#*************************************************************

#*************************************************************
# Basis_Set
#
# Basis_Set class, which contains information about some basis set. 
#
# Member variables:
# proper_name           - name you would see in the lit. ex: cc-pVDZ, 6-31G, etc.
# GENBAS_name           - name to find in the GENBAS file
# short_name            - name to identify in this script
# zeta                  - cannonical order of the basis
# type                  - type of basis set. ex: Dunning, Pople, ANO, etc.
#
class Basis_Set:

    # NOTE: 
    # If you modify the member variables, make sure to modify the "select" function in 
    # Basis as well!
    def __init__(self, proper_name, GENBAS_name, short_name, zeta, style):
        self.proper_name = proper_name
        self.GENBAS_name = GENBAS_name
        self.short_name  = short_name
        self.zeta        = zeta
        self.style       = style

    def print(self):
        print("Proper Name:", self.proper_name, ", GENBAS name:", self.GENBAS_name,
              ", short_name:", self.short_name, ", zeta:", self.zeta, ", style:", self.style)

#*************************************************************
# Basis
#
# A container for Basis_Set. Using Basis.select(...) will create a NEW 
# Basis object with only those basis sets that match the input constraints 
#
class Basis:

    def __init__(self):
        self.dict =  {}

    #add a basis with it's short-name as key
    def add(self, basis_set):
        self.dict.update({basis_set.short_name : basis_set})

    #print all basis
    def print(self):
        for key, basis in self.dict.items():
            basis.print()

    #print all short names (keys)
    def short_names(self):
        for key, basis in self.dict.items():
            print(basis.short_name)

    #get a basis via it's short name (key)
    def get(self, short_name):
        return self.dict[short_name]

    #this returns a new Basis object, with only the basis sets that match those requested by the user
    def select(self, proper_name=None, GENBAS_name=None, short_name=None, zeta=None, style=None):
        new_basis = Basis()
        for key, basis in self.dict.items():
            if ( proper_name != None ) and ( basis.proper_name != proper_name ): continue
            if ( GENBAS_name != None ) and ( basis.GENBAS_name != GENBAS_name ): continue
            if (  short_name != None ) and (  basis.short_name != short_name  ): continue
            if (        zeta != None ) and (        basis.zeta != zeta        ): continue
            if (       style != None ) and (       basis.style != style       ): continue
            new_basis.add(basis)
        return new_basis

# Global basis variable set
# To add a new basis to be tracked, append it in the style you see below. 
#
# NOTE: 
#       1. This is a dictionary update, so adding a collision will overwrite
BASIS = Basis()
BASIS.add( Basis_Set(proper_name='cc-pVDZ', GENBAS_name='PVDZ', short_name = 'DZ', zeta = 2, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pVTZ', GENBAS_name='PVTZ', short_name = 'TZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pVQZ', GENBAS_name='PVQZ', short_name = 'QZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV5Z', GENBAS_name='PV5Z', short_name = '5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV6Z', GENBAS_name='PV6Z', short_name = '6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV7Z', GENBAS_name='PV7Z', short_name = '7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV8Z', GENBAS_name='PV8Z', short_name = '8Z', zeta = 8, style = 'Dunning') )

BASIS.add( Basis_Set(proper_name='aug-cc-pVDZ', GENBAS_name='AUG-PVDZ', short_name = 'aDZ', zeta = 2, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pVTZ', GENBAS_name='AUG-PVTZ', short_name = 'aTZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pVQZ', GENBAS_name='AUG-PVQZ', short_name = 'aQZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV5Z', GENBAS_name='AUG-PV5Z', short_name = 'a5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV6Z', GENBAS_name='AUG-PV6Z', short_name = 'a6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV7Z', GENBAS_name='AUG-PV7Z', short_name = 'a7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV8Z', GENBAS_name='AUG-PV8Z', short_name = 'a8Z', zeta = 8, style = 'Dunning') )

BASIS.add( Basis_Set(proper_name='cc-pCVDZ', GENBAS_name='PCVDZ', short_name = 'CDZ', zeta = 2, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCVTZ', GENBAS_name='PCVTZ', short_name = 'CTZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCVQZ', GENBAS_name='PCVQZ', short_name = 'CQZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV5Z', GENBAS_name='PCV5Z', short_name = 'C5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV6Z', GENBAS_name='PCV6Z', short_name = 'C6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV7Z', GENBAS_name='PCV7Z', short_name = 'C7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV8Z', GENBAS_name='PCV8Z', short_name = 'C8Z', zeta = 8, style = 'Dunning') )

BASIS.add( Basis_Set(proper_name='aug-cc-pCVDZ', GENBAS_name='AUG-PCVDZ', short_name = 'aCDZ', zeta = 2, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCVTZ', GENBAS_name='AUG-PCVTZ', short_name = 'aCTZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCVQZ', GENBAS_name='AUG-PCVQZ', short_name = 'aCQZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV5Z', GENBAS_name='AUG-PCV5Z', short_name = 'aC5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV6Z', GENBAS_name='AUG-PCV6Z', short_name = 'aC6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV7Z', GENBAS_name='AUG-PCV7Z', short_name = 'aC7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV8Z', GENBAS_name='AUG-PCV8Z', short_name = 'aC8Z', zeta = 8, style = 'Dunning') )


