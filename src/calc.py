#*************************************************************
#
# calc.py
#       JHT, July 9, 2023, Dallas, TX
#       -- created
# 
# This module defined the Calc and Calcs classes, and construsts the global
# CALCS object which defines all default calculations tracked within this package
# 
# Calc:
#       Defines a particular calculation
#
# Calcs:
#       A collection of calculations, with select function to return a new
#       Calc object that matches some set of constaints
#
# CALCS:
#       A global Calc object that contains all the 
#       Calc sets registered by default in this package 
#
#*************************************************************

#*************************************************************
# Calc
#
# Calc class, which consists of different information about various 
# type of calculations. 
#
# Member variables:
# proper_name           - true name of the calculation
# ZMAT_name             - what needs to go with the CALC= section of ZMAT
# short_name            - shorthand for this calc
# rhf_cc                - CC_PROG subroutine to use in RHF case
# uhf_cc                - CC_PROG subroutine to use in UHF case
# rohf_cc               - CC_PROG subroutine to use in ROHF case
#
class Calc:
  
    #NOTE
    # If you change or add parameters here, be sure to update Calcs.select member function
    #   to match!!
    def __init__(self, proper_name, ZMAT_name, short_name, rhf_cc, uhf_cc, rohf_cc, nbody):
        self.proper_name = proper_name
        self.ZMAT_name   = ZMAT_name
        self.short_name  = short_name
        self.rhf_cc      = rhf_cc
        self.uhf_cc      = uhf_cc
        self.rohf_cc     = rohf_cc
        self.nbody       = nbody

    def print(self):
        print(proper_name, ZMAT_name, short_name, rhf_cc, uhf_cc, rohf_cc, nbody)


#*************************************************************
# Calcs
#
# Calcs class, which contains a dict of the various calcs contained. 
#
class Calcs:

    def __init__(self):
        self.dict = {}

    #adds a calculation to dict with short_name as key
    def add(self, calc):
        self.dict.update({calc.short_name:calc})

    #prints all calculations
    def print(self):
        for key, calc in self.dict.items():
            calc.print()

    #prints all short names (keys)
    def short_names(self):
        for key, calc in self.dict.items():
            print(calc.short_name)

    #gets a calculation via it's short name)
    def get(self, short_name):
        return self.dict[short_name]

    #this returns a new Calc object, with only the calcs that match those requested by the user
    # for example:
    #   t2_calcs = CALCS.select(nbody=2) 
    # 
    # NOTE: if a new parameter for the Calc class is added, it should also be updated here
    def select(self, proper_name=None, ZMAT_name=None, short_name=None, rhf_cc=None, uhf_cc=None,
               rohf_cc=None, nbody=None):
        new_calcs = Calcs()
        for key, calc in self.dict.items():
            if ( proper_name != None ) and ( calc.proper_name != proper_name ): continue
            if (   ZMAT_name != None ) and (   calc.ZMAT_name != ZMAT_name   ): continue
            if (  short_name != None ) and (  calc.short_name != short_name  ): continue
            if (      rhf_cc != None ) and (      calc.rhf_cc != rhf_cc      ): continue
            if (      uhf_cc != None ) and (      calc.uhf_cc != uhf_cc      ): continue
            if (     rohf_cc != None ) and (     calc.rohf_cc != rohf_cc     ): continue
            if (       nbody != None ) and (       calc.nbody != nbody       ): continue
            new_calcs.add(calc)
        return new_calcs

#*************************************************************
#
# CALCS
#
#	Global Calcs object that tracks all calculations typically used in this package.
#
CALCS = Calcs()

CALCS.add( Calc(proper_name = "SCF",          ZMAT_name = "SCF",                    short_name = "scf",
                     rhf_cc = "NCC",             uhf_cc = "NCC",                       rohf_cc = "VCC",
                      nbody = 1) )

CALCS.add( Calc(proper_name = "MP2",          ZMAT_name = "MP2",                    short_name = "mp2",
                     rhf_cc = "VCC",             uhf_cc = "VCC",                       rohf_cc = "VCC",
                      nbody = 2) )

CALCS.add( Calc(proper_name = "SDQ-MP4",      ZMAT_name = "SDQ-MP4",                short_name = "sdqmp4",
                     rhf_cc = "VCC",             uhf_cc = "VCC",                       rohf_cc = "VCC",
                      nbody = 2) )

CALCS.add( Calc(proper_name = "CCSD",         ZMAT_name = "CCSD",                   short_name = "D",
                     rhf_cc = "NCC",             uhf_cc = "ECC",                       rohf_cc = "VCC",
                      nbody = 2) )

CALCS.add( Calc(proper_name = "CCSDTQ(P)",    ZMAT_name = "CC(n-1)(n), EXCITE=5",   short_name = "pP",
                     rhf_cc = "MRCC",            uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 5) )

CALCS.add( Calc(proper_name = "CCSDTQP",      ZMAT_name = "CC(n), EXCITE=5",        short_name = "P",
                     rhf_cc = "MRCC",            uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 5) )

CALCS.add( Calc(proper_name = "CCSDTQ(P)_L",  ZMAT_name = "CC(n-1)(n)_L, EXCITE=5", short_name = "pPL",
                     rhf_cc = "MRCC",            uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 5) )

CALCS.add( Calc(proper_name = "CCSDTQP(H)_L", ZMAT_name = "CC(n-1)(n)_L, EXCITE=6", short_name = "pHL",
                     rhf_cc = "MRCC",            uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 6) )

# T3 methods
CALCS.add( Calc(proper_name = "CCSD(T)",      ZMAT_name = "CCSD(T)",                short_name = "pT",
                     rhf_cc = "NCC",             uhf_cc = "ECC",                       rohf_cc = "VCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSD(T)_L",    ZMAT_name = "CCSD(T)_L",              short_name = "pTL",
                     rhf_cc = "NCC",             uhf_cc = "ECC",                       rohf_cc = "VCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT",        ZMAT_name = "CCSDT",                  short_name = "T",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "VCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT-1",      ZMAT_name = "CCSDT-1",                short_name = "T-1",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT-1b",      ZMAT_name = "CCSDT-1b",                short_name = "T-1b",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT-2",      ZMAT_name = "CCSDT-2",                short_name = "T-2",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT-3",      ZMAT_name = "CCSDT-3",                short_name = "T-3",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT-4",      ZMAT_name = "CCSDT-4",                short_name = "T-4",
                     rhf_cc = "VCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSD(T-2)",      ZMAT_name = "CCSD(T-2)",               short_name = "pT-2",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSD(T-3)",      ZMAT_name = "CCSD(T-3)",               short_name = "pT-3",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSD(T-4)",      ZMAT_name = "CCSD(T-4)",               short_name = "pT-4",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSD(T-5)",      ZMAT_name = "CCSD(T-5)",               short_name = "pT-5",
                     rhf_cc = "NCC",             uhf_cc = "VCC",                       rohf_cc = "MRCC",
                      nbody = 3) )

# T4 methods
CALCS.add( Calc(proper_name = "CCSDT(Q)",     ZMAT_name = "CCSDT(Q)",               short_name = "pQ",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDT(Q)_L",   ZMAT_name = "CCSDT(Q)_L",             short_name = "pQL",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDTQ",       ZMAT_name = "CCSDTQ",                 short_name = "Q",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDTQ-1a",       ZMAT_name = "CCSDTQ-1a",                 short_name = "Q-1a",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDTQ-1b",       ZMAT_name = "CCSDTQ-1b",                 short_name = "Q-1b",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDTQ-3",       ZMAT_name = "CCSDTQ-3",                 short_name = "Q-3",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDT(Q-2)",       ZMAT_name = "CCSDT(Q-2)",                 short_name = "pQ-2",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDT(Q-3)",       ZMAT_name = "CCSDT(Q-3)",                 short_name = "pQ-3",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDT(Q-4)",       ZMAT_name = "CCSDT(Q-4)",                 short_name = "pQ-4",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDT(Q-5)",       ZMAT_name = "CCSDT(Q-5)",                 short_name = "pQ-5",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDT(Q-6)",       ZMAT_name = "CCSDT(Q-6)",                 short_name = "pQ-6",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

#simul T3 T3 methods
CALCS.add( Calc(proper_name = "CCSD(TQ)",     ZMAT_name = "CCSD(TQ)",               short_name = "pTQ",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSD(TQf)",     ZMAT_name = "CCSD(TQf)",               short_name = "pTQf",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSD(TQ-2)",     ZMAT_name = "CCSD(TQ-2)",               short_name = "pTQ-2",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSD(TQ-3)",     ZMAT_name = "CCSD(TQ-3)",               short_name = "pTQ-3",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSD(TQ-4)",     ZMAT_name = "CCSD(TQ-4)",               short_name = "pTQ-4",
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC",
                      nbody = 4) )

