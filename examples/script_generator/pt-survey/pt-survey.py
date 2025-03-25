#*************************************************************
# pt-survery.py 
#
#       JHT, March 25, 2024, Dallas, TX
#
# Generates a series of tests for various perturbative methods
# of treating T/Q in CC theory
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
"""ptsurvey

Usage:
    ptsurvey.py --name=<name> --ZMAT=<zmat> --runfile=<run.sh> 
    ptsurvey.py --joblist 
    ptsurvey.py --abrvs
    ptsurvey.py (-h | --help)
    ptsurvey.py --version

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

ZMAT_OPTIONS.update('1_basis' , Option(abrv = '1YY', default = None      , description="First row basis"        ) )
ZMAT_OPTIONS.update('2_basis' , Option(abrv = '2YY', default = None      , description="Second row basis"       ) )
ZMAT_OPTIONS.update('3_basis' , Option(abrv = '3YY', default = None      , description="Third row basis"        ) )

def make_joblist(molecule=None, zmat=None, run=None):
    joblist = Joblist(molecule=molecule, zmat=zmat, run=run)

    if (zmat != None):
        ZMAT_OPTIONS.set('ref', zmat.get_ref().strip())

    #Add some nonstandard options
    ZMAT_OPTIONS.update('mem', Option(abrv = 'MMM', default = '118', description="memory"  ) )

    RUN_OPTIONS.update('mem'     , Option(abrv = 'SMM'  , default = '128' , description="job memory") )
    RUN_OPTIONS.update('cpu'     , Option(abrv = 'SPU'  , default = '32' , description="cpus") )
    RUN_OPTIONS.update('xcfour', Option(abrv = 'XC4', default = 'source ~/settblis.sh\n    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n    export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK\n    xjoda\n    xnmol\n    xnscf\n    xncc' , description="runs cfour"))
    
    #-------------------------------------
    # all tests, we're using (Q)_L as the reference (well, potentially (P)_L...) 
    # Note: (T-n), n=2,3,4,5 is all calculated at once
    # Note: (Q-n), n=2,3,4,5,6 is all calculated at once
    # Note: (TQ-n), n=2,3,4 is all calculated at once
    # Note: (TQf) calculates (TQ), (TQf), +TQ and +TQ* all at once
    # Note: (T)_L calculates (T) as well
    # Note: (Q)_L calculates (Q) as well
    # Note: (P)_L calculates (P) as well 
    for c in ['D', 'pQL', 'Q', 'pPL', 'pTL', 'T-1', 'T-1b', 'T-2', 'T-3', 'T-4', 'pT-5', 'Q-1a', 'Q-1b', 'Q-3', 'pQ-6', 'pTQ-4', 'pTQ']:
        for s in ['DZ', 'TZ', 'QZ']:
            zopts = copy.deepcopy(ZMAT_OPTIONS)
  
            H_name = s.replace('C', '')

            zopts.set('1_basis', BASIS.get(H_name).GENBAS_name)
            zopts.set('2_basis', BASIS.get(s).GENBAS_name)
            zopts.set('3_basis', BASIS.get(s).GENBAS_name)

            #SET FROZEN CORE ON FOR THESE BASIS
            zopts.set('frzcore', 'ON')

            set_calc(CALCS.get(c), zopts)
            set_basis(BASIS.get(s), zopts)

            ropts = copy.deepcopy(RUN_OPTIONS)
            ropts.set('jobname', molecule + "_" + c.lower() + "_" +  s.lower())

            joblist.append(name=CALCS.get(c).proper_name + "/" + BASIS.get(s).proper_name,
                           zmat_options = zopts,
                           run_options  = ropts)

    
    return joblist


#*************************************************************
# Main function. Don't modify this except to rename your script 
if __name__ == '__main__':

    #Process Docopts input
    args = docopt(__doc__, version="PT-survery 1.0")

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

