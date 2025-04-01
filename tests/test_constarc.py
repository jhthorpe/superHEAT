# test_constarc.py 
#
# Contains unit tests for the constants archive in the 
# format which may be used by pytest
#
# NOTE:
#   The list of unit tests are at the bottom

from superHEAT.archive_manager import constarc
from superHEAT.archive_manager import constants

import shutil
import os

#test feature of the archive. Es
def test_constarc():

    print('{name} WAS CALLED!'.format(name = __name__))

    arcname = 'constarc_test_dir'
    #If the example archive exists, delete it
    if os.path.exists(arcname):
        shutil.rmtree(arcname)

    #The top level directory is NOT automatically generated
    os.mkdir(arcname)

    #generate constants archive
    arc = constarc.Constants_Archive(arcname)

    #create a set
    au_set = constants.Constants_Set(set_name = "my_AU_set", set_date = "yyyy-mm-dd", set_note = "This will contain a set of constants in atomic units") 
    si_set = constants.Constants_Set(set_name = "my_SI_set", set_date = "yyyy-mm-dd", set_note = "This will contain a set of constants in SI units") 

    #add a constant
    hbar_au = constants.Constant(name = "hbar", note = "Hbar in atomic units", value = 1, unc = 0, rel_unc = 0, unit = "", is_exact = True, date='Alw    ays')
    a0_au   = constants.Constant(name = "a0", note = "Bohr Radius in atomic units", value = 1, unc = 0, rel_unc = 0, unit = "", is_exact = True, date    ='Always')
    hbar_si = constants.Constant(name = "hbar", note = "Hbar in SI, CODATA 2022", value = 1.054571817E-34, unc = 0, rel_unc = 0, unit = "J s", is_exact = True, date='2022-??-??')
    a0_si   = constants.Constant(name = "a0", note = "Bohr Radius in SI units", value = 5.29177210544E-11, unc = 0.00000000082E-11, rel_unc = 1.6E-10, is_exact = False, date='2022-??-??', unit="m")

    #add these constants to the set
    au_set.add_constant(hbar_au)
    au_set.add_constant(a0_au)
    si_set.add_constant(hbar_si)
    si_set.add_constant(a0_si)

    #add the set to archive (this forces a write)
    arc.add_constants_set(au_set)
    arc.add_constants_set(si_set)

    #create a new archive!
    newarc = constarc.Constants_Archive(arcname)

    #read in the set
    newset = newarc.load_constants_set('my_AU_set')

    #test succeeds if all the above executed without and exception, and if the loaded set matches the stored set 
    print("old set of units :", au_set.print_string())
    print("new set of units :", newset.print_string())

    #cleanup at the end
    if os.path.exists(arcname):
        shutil.rmtree(arcname)

    #test that the two sets are equal
    assert(newset == au_set)    

    #test that two constants that are NOT equal are, in fact, not equal 
    assert(not(a0_si == a0_au))
    assert(a0_si == a0_si)
    assert(a0_si == a0_si)
