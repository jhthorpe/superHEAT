# create_archive.py
#
#   March 28, 2025 @ ANL : JHT added
# 
# Example for how to use this directory to generate, 
# populate, and retrieve data from an archive
#
# This will 
#   1. create an archive at this level
#   2. create the constants subarchive
#   3. Fill it with an example
#   4. Recover this same archive
#

from superHEAT.archive_manager import constarc
from superHEAT.archive_manager import constants
import shutil
import os

#If the example archive exists, delete it
if os.path.exists("new_archive"):
    shutil.rmtree("new_archive")

#The top level directory is NOT automatically generated
os.mkdir("new_archive")

#Create the constants archive via the top level directory path
my_constarc = constarc.Constants_Archive("new_archive")

#Create a set of constants to keep in the archive
au_set = constants.Constants_Set(set_name = "my_AU_set", set_date = "yyyy-mm-dd", set_note = "This will contain a set of constants in atomic units")
si_set = constants.Constants_Set(set_name = "my_SI_set", set_date = "yyyy-mm-dd", set_note = "This will contain a set of constants in SI units")

#Add some constants to each set
au_set.add_constant(constants.Constant(name = "hbar", note = "Hbar in atomic units", value = 1, unc = 0, rel_unc = 0, unit = "", is_exact = True, date='Always'))
au_set.add_constant(constants.Constant(name = "a0", note = "Bohr Radius in atomic units", value = 1, unc = 0, rel_unc = 0, unit = "", is_exact = True, date='Always'))

si_set.add_constant(constants.Constant(name = "hbar", note = "Hbar in SI, CODATA 2022", value = 1.054571817E-34, unc = 0, rel_unc = 0, unit = "J s", is_exact = True, date='2022-??-??'))
si_set.add_constant(constants.Constant(name = "a0", note = "Bohr Radius in SI units", value = 5.29177210544E-11, unc = 0.00000000082E-11, rel_unc = 1.6E-10, is_exact = False, date='2022-??-??', unit="m"))

#Register these constants sets in the archive
my_constarc.add_constants_set(au_set)
my_constarc.add_constants_set(si_set)


#Print the constants sets
print(my_constarc.print_string())

for constants_set in my_constarc.constants_sets.values():
    print(constants_set.print_string())
