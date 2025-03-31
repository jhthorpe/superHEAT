# make_standard_constants.py
#
# This is a script that generates and modifies the standard set of constants contained in this archive
#
# March 31, 2025 @ ANL : JHT created
#
# NOTE:
# the main function is contained at the bottom of the file

from superHEAT.archive_manager import constarc
from superHEAT.archive_manager import constants
import os

ARCHIVE_PATH = "/Users/l00332323/superHEAT/archive"

CFOUR_OLD = constants.Constants_Set(set_name = "CFOUR_OLD", 
                                    set_date = "2025-03-31", 
                                    set_note = "CFOUR_OLD constants set used when CONSTANTS=OLD is specified. Values may be found at https://cfour.uni-mainz.de/cfour/index.php?n=Main.ListOfUsedPhysicalConstants, and are otherwise taken from either (QUANTITIES, UNITS, AND SYMBOLS IN PHYSICAL CHEMISTRY, I. Mills et al. Blackwell Science, Oxford, 1993, 2nd Ed.) or (https://physics.nist.gov/cuu/Constants/)")

CFOUR_OLD.add_constant(constants.Constant(name = "a0".upper(), 
                                          date = "2017-02-15", 
                                          value = 0.5291772083e-10, 
                                          unc = 0.0000000019e-10,
                                          rel_unc = 3.7e-9,
                                          unit = "m",
                                          is_exact = False,
                                          note = "Atomic unit of length in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "e".upper(), 
                                          date = "2017-02-15", 
                                          value = 1.602176462e-19, 
                                          unc = 0.000000063e-19, 
                                          rel_unc = 3.9e-8, 
                                          unit = "C",
                                          is_exact = False,
                                          note = "Elementary charge in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "u".upper(), 
                                          date = "2017-02-15", 
                                          value = 1.66053873e-27, 
                                          unc = 0.00000013e-27, 
                                          rel_unc = 7.9E-8, 
                                          unit = "kg",
                                          is_exact = False,
                                          note = "Unified atomic mass unit in SI, from CFOUR_OLD, defined as 1/12 the mass of the C-12 atom"))

CFOUR_OLD.add_constant(constants.Constant(name = "muN", 
                                          date = "2017-02-15", 
                                          value = 5.05078317e-27, 
                                          unc = 0.00000020e-27, 
                                          rel_unc = 4.0e-8,
                                          unit = "J T-1", 
                                          is_exact = False,
                                          note = "Nuclear Magneton in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "me", 
                                          date = "2017-02-15", 
                                          value = 9.10938188e-31, 
                                          unc = 0.00000072e-31, 
                                          rel_unc = 7.9e-8, 
                                          unit = "kg", 
                                          is_exact = False,
                                          note = "Electron Mass in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "mp", 
                                          date = "2017-02-15", 
                                          value = 1.67262158e-27, 
                                          unc = 0.00000013e-27, 
                                          rel_unc = 7.9e-8, 
                                          unit = "kg", 
                                          is_exact = False,
                                          note = "Proton mass in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "Hbar", 
                                          date = "2017-02-15", 
                                          value = 1.054571596e-34, 
                                          unc = 0.000000082e-32, 
                                          rel_unc = 7.8e-8, 
                                          unit = "J s", 
                                          is_exact = False,
                                          note = "Planck constant over 2 pi in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "mp/me", 
                                          date = "2017-02-15", 
                                          value = 1836.1526675, 
                                          unc = 0.0000039, 
                                          rel_unc = 2.1e-9, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "Proton-electron mass ratio, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "c", 
                                          date = "2017-02-15", 
                                          value = 299792458, 
                                          unc = 0, 
                                          rel_unc = 0, 
                                          unit = "m s-1", 
                                          is_exact = True,
                                          note = "Speed of light in vacuum in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "NA", 
                                          date = "2017-02-15", 
                                          value = 6.02214199e23, 
                                          unc = 0.00000047e23, 
                                          rel_unc = 7.9e-8, 
                                          unit = "mol-1", 
                                          is_exact = False,
                                          note = "Avogadro's constant in SI, from CFOUR_OLD"))
                                          
CFOUR_OLD.add_constant(constants.Constant(name = "ea0", 
                                          date = "2017-02-15", 
                                          value = 8.47835267e-30, 
                                          unc = 0.00000033e-30, 
                                          rel_unc = 3.9e-8, 
                                          unit = "C m", 
                                          is_exact = False,
                                          note = "Atomic unit of electric dipole moment in SI, from CFOUR_OLD"))
                                          
CFOUR_OLD.add_constant(constants.Constant(name = "au v", 
                                          date = "2017-02-15", 
                                          value = 2.1876912633e6, 
                                          unc = 0.0000000073e6, 
                                          rel_unc = 3.3e-9, 
                                          unit = "m s-1", 
                                          is_exact = False,
                                          note = "atomic unit of velocity in SI, from CFOUR_OLD"))
                                          
CFOUR_OLD.add_constant(constants.Constant(name = "au t", 
                                          date = "2017-02-15", 
                                          value = 2.418884326505e-17, 
                                          unc = 0.000000000016e-17, 
                                          rel_unc = 6.6e-12, 
                                          unit = "s", 
                                          is_exact = False,
                                          note = "atomic unit of time in SI, from CFOUR_OLD"))
                                          
CFOUR_OLD.add_constant(constants.Constant(name = "g", 
                                          date = "2017-02-15", 
                                          value = -2.0023193043718e0, 
                                          unc = 0.0000000000075e0, 
                                          rel_unc = 3.8e-12, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "electron g value in SI, from CFOUR_OLD"))

CFOUR_OLD.add_constant(constants.Constant(name = "kB", 
                                          date = "2017-02-15", 
                                          value = 1.3806504e-23, 
                                          unc = 0.0000024e-23, 
                                          rel_unc = 1.7e-6,
                                          unit = "J K-1", 
                                          is_exact = False,
                                          note = "Boltzman Constant in SI, from CFOUR_OLD"))

                                          
#TODO ATOMIC MASSES in unified atomic mass units, from joda/pertable.f
CFOUR_MASSES = [ 1.007825035E+00,  4.00260324E+00,  7.0160030E+00,
   9.0121822E+00,  11.0093054E+00, 12.0000000E+00,
14.003074002E+00, 15.99491463E+00,18.99840322E+00,
  19.9924356E+00,  22.9897677E+00, 23.9850423E+00,
  26.9815386E+00,  27.9769271E+00, 30.9737620E+00,
 31.97207070E+00,34.968852721E+00, 39.9623837E+00,
  38.9637074E+00,  39.9625906E+00, 44.9559100E+00,
  47.9479473E+00,  50.9439617E+00, 51.9405098E+00,
  54.9380471E+00,  55.9349393E+00, 58.9331976E+00,
  57.9353462E+00,  62.9295989E+00, 63.9291448E+00,
   68.925580E+00,  73.9211774E+00, 74.9215942E+00,
  79.9165196E+00,  78.9183361E+00,  83.911507E+00,
   84.911794E+00,  87.9056188E+00,  88.905849E+00,
  89.9047026E+00,  92.9063772E+00, 97.9054073E+00,
   97.907215E+00, 101.9043485E+00, 102.905500E+00,
  105.903478E+00,  106.905092E+00, 113.903357E+00,
  114.903882E+00, 119.9021991E+00, 120.9038212E+00,
  129.906229E+00,  126.904473E+00, 131.904144E+00,
  132.905429E+00,  137.905232E+00, 138.906347E+00,
  139.905433E+00,  140.907647E+00, 141.907719E+00,
  144.912743E+00,  151.919728E+00, 152.921225E+00,
  157.924019E+00,  158.925342E+00, 163.929171E+00,
  164.930319E+00,  165.930290E+00, 168.934212E+00,
  173.938859E+00,  174.940770E+00,179.9465457E+00,
  180.947462E+00,  183.950928E+00, 186.955744E+00,
  191.961467E+00,  192.962917E+00, 194.964766E+00,
  196.966543E+00,  201.970617E+00, 204.974401E+00,
  207.976627E+00,  208.980374E+00, 208.982404E+00,
  209.987126E+00,  222.017571E+00, 223.019736E+00,
  226.025410E+00,  227.027752E+00, 232.038055E+00,
  231.035884E+00,  238.050788E+00, 237.048173E+00,
  244.064204E+00,  243.061381E+00, 247.070354E+00,
  247.074987E+00,  251.079587E+00, 252.082980E+00,
  257.095105E+00,  258.098431E+00,  259.10103E+00,
   262.10963E+00,   265.11670E+00,  268.12545E+00,
   271.13347E+00,   272.13803E+00,  270.13465E+00,
   276.15116E+00,   281.16206E+00,  280.16447E+00,
   285.17411E+00]

ATOM_NAMES = ['hydrogen','helium','lithium','beryllium','boron','carbon','nitrogen','oxygen','fluorine','neon','sodium','magnesium','Aluminium','silicon','phosphorus','sulfur','chlorine','argon','potassium','calcium','scandium','titanium','vanadium','chromium','manganese','iron','cobalt','nickel','copper','zinc','gallium','germanium','arsenic','selenium','bromine','krypton','rubidium','strontium','yttrium','zirconium','niobium','molybdenum','technetium','ruthenium','rhodium','palladium','silver','cadmium','indium','tin','antimony','tellurium','iodine','xenon','cesium','barium','lanthanum','cerium','praseodymium','neodymium','promethium','samarium','europium','gadolinium','terbium','dysprosium','holmium','erbium','thulium','ytterbium','lutetium','hafnium','tantalum','tungsten','rhenium','osmium','iridium','platinum','gold','mercury','thallium','lead','bismuth','polonium','astatine','radon','Francium','Radium','Actinium','Thorium','Protactinium','Uranium','Neptunium','Plutonium','Americium','Curium','Berkelium','Californium','Einsteinium','Fermium','Mendelevium','Nobelium','Lawrencium','Rutherfordium','Dubnium','Seaborgium','Bohrium','Hassium','Meitnerium','Darmstadtium','Roentgenium','Copernicium']

ATOM_SYMBOLS = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn']

# Register the atoms and names from the list
for idx in range(len(CFOUR_MASSES) - 1):
#    print('{name}({sym}) : {mass}'.format(name = ATOM_NAMES[idx], sym = ATOM_SYMBOLS[idx], mass = CFOUR_MASSES[idx]))    
    CFOUR_OLD.add_constant(constants.Constant(name = "{sym} u".format(sym = ATOM_SYMBOLS[idx]), 
                                              date = "2017-02-15", 
                                              value = CFOUR_MASSES[idx], 
                                              unc = None, 
                                              rel_unc = None, 
                                              unit = "u", 
                                              is_exact = False,
                                              note = "Mass of {atm} in unified atomic mass units from CFOUR_OLD.".format(atm = ATOM_NAMES[idx])))


#Add some conversions

CFOUR_OLD.add_constant(constants.Constant(name = "Eh to eV", 
                                          date = "2017-02-15", 
                                          value = 27.2113834, 
                                          unc = 0.000011, 
                                          rel_unc = 4.0e-7, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "Conversion from Eh to eV in SI, from CFOUR_OLD, equation 1 Eh = x * eV, x = { 2 Rhc / e}"))

CFOUR_OLD.add_constant(constants.Constant(name = "Eh to J", 
                                          date = "2017-02-15", 
                                          value = 4.35974381e-18, 
                                          unc = 0.00000034e-18, 
                                          rel_unc = 7.8e-8, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "Conversion from Eh to J in SI, from CFOUR_OLD, equation 1 Eh = x * J, x = {2 Rhc}"))
                                          
CFOUR_OLD.add_constant(constants.Constant(name = "Eh to cm-1", 
                                          date = "2017-02-15", 
                                          value = 219474.6313710e0, 
                                          unc = 0.0000017e0, 
                                          rel_unc = 7.7e-12, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "Conversion from Eh to cm-1 (wavenumbers) in SI, from CFOUR_OLD, equation (1 Eh)/hc = x * cm-1, x = {2R}"))

CFOUR_OLD.add_constant(constants.Constant(name = "cm-1 to kcal/mol", 
                                          date = "2017-02-15", 
                                          value = 2.85914e-3, 
                                          unc = None, 
                                          rel_unc = None, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "Conversion from cm-1 (wavefunumbers) to kcal/mol in SI, from CFOUR_OLD, equation 1 cm-1 = x * kcal mol-1"))

CFOUR_OLD.add_constant(constants.Constant(name = "cm-1 to kJ/mol", 
                                          date = "2017-02-15", 
                                          value = 11.96266e-3, 
                                          unc = None, 
                                          rel_unc = None, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "Conversion from cm-1 (wavenumbers) to kJ/mol  in SI, from CFOUR_OLD, equation 1 cm-1 = x * kJ mol-1"))
                                          
CFOUR_OLD.add_constant(constants.Constant(name = "D to C m", 
                                          date = "2017-02-15", 
                                          value = 3.33564e-30, 
                                          unc = None, 
                                          rel_unc = None, 
                                          unit = "", 
                                          is_exact = False,
                                          note = "Conversion from D (Debye) to C m in SI, from CFOUR_OLD, equation 1 D = x * C m"))
                                          
                                          
'''
CFOUR_OLD.add_constant(constants.Constant(name = "", 
                                          date = "2017-02-15", 
                                          value = , 
                                          unc = , 
                                          rel_unc = , 
                                          unit = "", 
                                          is_exact = False,
                                          note = " in SI, from CFOUR_OLD"))
                                          
'''



# Dictionary of the standard sets of constants that need to be included in the archive
STANDARD_SETS = {'CFOUR_OLD' : CFOUR_OLD}

#######################################################################
# MAIN
#
if __name__ == '__main__':
        
    assert(os.path.exists(ARCHIVE_PATH)), "Could not find the archive path, perhaps it was not upzipped?"

    carc = constarc.Constants_Archive(ARCHIVE_PATH)

    #Check that each of the constants sets is in the archive
    for key, value in STANDARD_SETS.items():
        
        #It exists, let's check that it matches
        print("Validating {name}...".format(name = value.set_name), end='')
        if key in carc.constants_sets:
            print(" found in Archive...", end='')

        #It does not exist, we need to add
        else:
            print(" not found in Archive...", end='')
            carc.add_constants_set(value)

        #Validate the set
        cset = carc.load_constants_set(key)
        if value != cset:
            print(" validation FAILED")
        else:
            print(" validated!")

