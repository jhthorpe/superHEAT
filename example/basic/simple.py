#*************************************************************
# simple.py 
#
#       JHT, July 10, 2023, Dallas, TX
#       -- created
# 
# An example of how to use this repository to generate 
# CFOUR input and runscript files for a simple, two-step 
# composite recipe
#
# To make a new recipe, do the following:
# 1. Modify the Docopt string to reflect your script's name
# 2. Modify the make_joblist function to generate whatever jobs you want 
#
# The following is a list of global objects (in all caps)
# that can be used to generate your joblist:
# 
# BASIS 	-- lists all basis functions, see basis.py
# CALCS		-- lists all calculations, see calc.py
# OPTIONS	-- lists default options, see option.py
#
#*************************************************************

#*************************************************************
# DOCOPT input string
#
# To modify to your new script, ONLY change the name. 
#
"""simple

Usage:
    simple.py --name=<name> --ZMAT=<zmat> --runfile=<run.sh> 
    simple.py --joblist 
    simple.py (-h | --help)
    simple.py --version

Options:
    --joblist     Print all predetermined jobs.
    -h --help     Show this screen.
    --version     Show version.

"""

#*************************************************************
# Import statements. Those below are required. Import whatever
# else you might need  
#
from docopt import docopt
import copy
import sys
from basis import *
from calc import * 
from zmat import *
from runscript import *
from option import *
from job import *


#*************************************************************
# make_joblist 
#
# This is the function you (the user) modify to generate whatever
# set of jobs you want constructed
#
# NOTE: DO NOT modify any pre-defined global variables
#
def make_joblist(molecule=None, zmat=None, run=None):
    joblist = Joblist()

    #First job, SCF/cc-pVDZ
    #Using mostly default options:
    zopts = ZMAT_OPTIONS
    ropts = RUN_OPTIONS

    #Calc and Basis need to be specified via the global variables
    zopts.set('calc', CALCS.get('scf').ZMAT_name)
    zopts.set('basis', BASIS.get('DZ').GENBAS_name)

    #add it to the current joblist!
    joblist.append(molecule, zmat, zopts, run, ropts)

    return joblist


#*************************************************************
# Main function. Don't modify this except to rename your script 
if __name__ == '__main__':

    #Process Docopts input
    args = docopt(__doc__, version="simple 1.0")

    #if printing joblist
    if args['--joblist']:
        print("Joblist not defined yet")
        joblist = make_joblist()
        joblist.print() #printing for now, save to file later

    #generating job files
    else:
        #Read ZMAT
        zmat = ZMAT(args['--ZMAT'])

        #Read run.dummy
        rundummy = Runscript(args['--runfile'])

        #Generate the basic joblist
        joblist = make_joblist(args['--name'], zmat, rundummy)
        joblist.print()

        #generate the jobs with a particula
#        joblist.generate() #testing

