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

CFOUR_OLD.add_constant(constants.Constant(name = "amu".upper(), 
                                          date = "2017-02-15", 
                                          value = 1.66053873e-27, 
                                          unc = 0.00000013e-27, 
                                          rel_unc = 7.9E-8, 
                                          unit = "kg",
                                          is_exact = False,
                                          note = "Unified atomic mass unit in SI, from CFOUR_OLD"))

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

                                          
#TODO ATOMIC MASSES


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

