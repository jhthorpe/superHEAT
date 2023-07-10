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
# You should NEVER modify these globals, instead make a copy of them and modify from there
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
    simple.py --abrvs
    simple.py (-h | --help)
    simple.py --version

Options:
    --joblist     Print all predetermined jobs.
    --abrvs       Print the list of default abbreviations
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
from utility import *


#*************************************************************
# make_joblist 
#
# This is the function you (the user) modify to generate whatever
# set of jobs you want constructed. The Job-id numbers will be 
# constructed automatically for you, in the order that you 
# append the jobs to the list
#
# NOTE: DO NOT modify any pre-defined global variables
#
def make_joblist(molecule=None, zmat=None, run=None):
    joblist = Joblist(molecule=molecule, zmat=zmat, run=run)

   if (zmat != None):
       ZMAT_OPTIONS.set('ref', zmat.get_ref().strip())

    #--------------------------------
    # JOB 1: SCF/cc-pVTZ
    # Using mostly default options, and basic interface
    zopts = ZMAT_OPTIONS
    ropts = RUN_OPTIONS

    #You can specify non-default options as you want 
    zopts.set('calc', 'SCF') 
    zopts.set('basis', 'PVTZ') 

    #specify the runoptions
    ropts.set('jobname', molecule + '_scf_tz')

    #add it to the current joblist!
    joblist.append(name='SCF/cc-pVTZ', zmat_options=zopts, run_options=ropts)

    #--------------------------------
    # JOB 2: [fc] MP2/cc-pVDZ 
    # Using some of the helper functions
    zopts = ZMAT_OPTIONS
    ropts = RUN_OPTIONS
    set_calc(CALCS.get('mp2'), zopts)
    set_basis(BASIS.get('DZ'), zopts)
    zopts.set('frzcore', 'ON')
    ropts.set('jobname', molecule+"_mp2_dz")
    joblist.append(name='[fc] MP2/cc-pVTZ', zmat_options=zopts, run_options=ropts)

    return joblist


#*************************************************************
# Main function. Don't modify this except to rename your script 
if __name__ == '__main__':

    #Process Docopts input
    args = docopt(__doc__, version="simple 1.0")

    #if printing joblist
    if args['--joblist']:
        joblist = make_joblist(molecule="")
        joblist.print_names() #printing for now, save to file later

    #print options
    elif args['--abrvs']:
        joblist = make_joblist(molecule="")

        print("ZMAT variables")
        ZMAT_OPTIONS.print()

        print("run.dummy variables")
        RUN_OPTIONS.print()

    #generating job files
    else:
        #Read ZMAT
        zmat = Zmat(args['--ZMAT'])

        #Read run.dummy
        rundummy = Runscript(args['--runfile'])

        #Generate the basic joblist
        joblist = make_joblist(args['--name'], zmat, rundummy)
        joblist.print_names()

        #generate the jobs with a particula
        joblist.generate() #testing

