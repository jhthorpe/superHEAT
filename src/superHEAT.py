#*************************************************************
# superHEAT.py
#
#       JHT, June 28, 2023, Dallas, TX
#       -- created
# 
# .py script to generate the multitudes of ZMATs needed for
# testing or performing thermochemical calculations
#
# This is the primary driver for the script. 
#
# Note that the default object lists (like CALCS, BASIS, etc), 
# are defined in the appropriate .py files. If you want to modify 
# them, you must do so there
#
#*************************************************************

#*************************************************************
# DOCOPT input string
# Please don't modify unless you know exactly what you are doing...
"""superHEAT

Usage:
    superHEAT.py --name=<name> --ZMAT=<zmat> --runfile=<run.sh> --recipe=<recipe> 
    superHEAT.py --joblist [--recipe=<recipie>]
    superHEAT.py --show [--basis] [--calcs]  [--ZMATopts] [--runopts] 
    superHEAT.py --recipes
    superHEAT.py (-h | --help)
    superHEAT.py --version

Options:
    --joblist     Print all predetermined jobs.
    -h --help     Show this screen.
    --version     Show version.

"""

from docopt import docopt
import copy
import sys
from basis import *
from calc import * 
from zmat import *
from runscript import *

if __name__ == '__main__':

    #Process Docopts input
    args = docopt(__doc__, version="superHEAT 1.0")

    #if printing job ids
    if args['--joblist']:
        print("Joblist not defined yet")
        '''
        joblist = Job_List(None, None, None)

        joblist.print_names()
        '''

    elif args['--show']:
        if args['--basis'   ]:
            print("Default defined Basis Sets")
            BASIS.print()

        if args['--calcs'   ]:
            print("Default defined Calculations")
            CALCS.print()

        if args['--ZMATopts']:
            print("ZMAT options not implemented yet")
            '''
            print("Modifiable options in ZMAT")
            zmatopts = Option_List()
            zmatopts.set_ZMAT_default()
            zmatopts.print()
            '''

        if args['--runopts']:
            print("Runscript options not implemented yet")
            '''
            print("Modifiable options in runfile")
            runopts = Option_List()
            runopts.set_run_default()
            runopts.print()
            '''


    #generating job files
    else:
        #Read ZMAT
        zmat = ZMAT(args['--ZMAT'])

        #Read run.dummy
        rundummy = Runscript(args['--runfile'])

        #Generate the basic joblist
#        joblist = Job_List(args['--name'], zmat, rundummy)

        #Generate the recipe

        #generate the jobs with a particular recipe
#        joblist.generate() #testing

