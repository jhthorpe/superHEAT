#*************************************************************
# utility.py
#	JHT, July 10, 2023, Dallas, TX
#		- created
#
# Defines some utility functions that help the setting 
# of various variables using the global structures 
# defined in this repository
#
# set_calc:
#	Given a Calc object, sets the zmat options 
#	to the correct ones for that calculation
#
# set_basis:
#	Given a Basis object, sets the zmat options
# 	to the correct ones for that basis
#*************************************************************

import copy
import sys

#*************************************************************
# set_calc
#
# calc		- Calc object defined in calc.py
# zopts		- Options object, copied from ZMAT_OPTIONS in option.py
#
def set_calc(calc, zopts):
    
    #set the calculation name
    zopts.set('calc', calc.ZMAT_name)

  
    #set CC_PROG
    ref = zopts.get('ref').strip().lower()
    if ('RHF'.lower() == ref):
        zopts.set('ccprog', calc.rhf_cc)
    elif ('UHF'.lower() == ref):
        zopts.set('ccprog', calc.uhf_cc)
    elif ('ROHF'.lower() == ref): 
        zopts.set('ccprog', calc.rohf_cc)
    else:
        print("set_calc did not recognize the reference type")
        sys.exit(1)

    #Set ABCD to AOBASIS if possible
    if (                 3 > calc.nbody    or
          'CCSD(T)' == calc.proper_name    or
        'CCSD(T)_L' == calc.proper_name    
       ):
        zopts.set('abcd', 'AOBASIS')

#*************************************************************
# set_basis
# 
# This will eventually do more, given basis functions on particular 
# atoms, but for now is simple
#
# basis		- Basis object defined in basis.py
# zopts		= Options object, copied from ZMAT_OPTIONS in option.py
#
def set_basis(basis, zopts):
    zopts.set('basis',basis.GENBAS_name)

