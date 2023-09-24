#*************************************************************
# HEAT456Qp.py 
#
#       JHT, September 24, 2023, Dallas, TX
#       -- created
# 
# An example of how to use this repository to generate 
# CFOUR input and runscript files for a HEAT-456Q(P) 
# calculation
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
"""HEAT456Qp

Usage:
    HEAT456Qp.py --name=<name> --ZMAT=<zmat> --runfile=<run.sh> 
    HEAT456Qp.py --joblist 
    HEAT456Qp.py --abrvs
    HEAT456Qp.py (-h | --help)
    HEAT456Qp.py --version

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

    #-------------------------------------
    # CCSD(T) calcs 
    for s in ['aCTZ', 'aCQZ', 'aC5Z', 'aC6Z']:
        zopts = copy.deepcopy(ZMAT_OPTIONS)
        ropts = copy.deepcopy(RUN_OPTIONS)
        set_calc(CALCS.get('pT'), zopts)
        set_basis(BASIS.get(s), zopts)
        ropts.set('jobname', molecule + "_t_" + s.lower())
        joblist.append(name="ae-CCSD(T)/" + BASIS.get(s).proper_name,
                       zmat_options = zopts,
                       run_options  = ropts)

    #-------------------------------------
    # CCSDT - CCSD(T) calcs 
    for b in ['TZ', 'QZ']:
        for c in ['T','pT']:
            zopts = copy.deepcopy(ZMAT_OPTIONS)
            ropts = copy.deepcopy(RUN_OPTIONS)
            set_calc(CALCS.get(c), zopts)
            set_basis(BASIS.get(b), zopts)
            zopts.set('frzcore', 'ON')
            ropts.set('jobname', molecule + "_" + c + "_" + b.lower()) 
            joblist.append(name="fc-" + CALCS.get(c).proper_name + "/" + BASIS.get(b).proper_name,
                           zmat_options = zopts,
                           run_options  = ropts)
 
    #-------------------------------------
    # CCSDT(Q) - CCSDT calcs 
    for c in ['pP','Q','pQ','T']:
        zopts = copy.deepcopy(ZMAT_OPTIONS)
        ropts = copy.deepcopy(RUN_OPTIONS) 
        set_calc(CALCS.get(c), zopts)
        set_basis(BASIS.get('DZ'), zopts)
        zopts.set('frzcore', 'ON')
        ropts.set('jobname', molecule + "_" + c + "_" + "dz") 
        joblist.append(name="fc-" + CALCS.get(c).proper_name + "/" + BASIS.get('DZ').proper_name,
                       zmat_options = zopts,
                       run_options  = ropts)
        
    #-------------------------------------
    # MVD2 calc
    zopts = copy.deepcopy(ZMAT_OPTIONS)
    ropts = copy.deepcopy(RUN_OPTIONS)
    set_calc(CALCS.get('pT'), zopts)
    set_basis(BASIS.get('aCTZ'), zopts)
    zopts.set('rel', 'MVD2')
    ropts.set('jobname', molecule + "_mvd2_pT_actz")
    joblist.append(name='MVD2 ae-' + CALCS.get('pT').proper_name + "/" + BASIS.get('aCTZ').proper_name,
                   zmat_options = zopts,
                   run_options = ropts)
    
    #-------------------------------------
    # DBOC calc 
    zopts = copy.deepcopy(ZMAT_OPTIONS)
    ropts = copy.deepcopy(RUN_OPTIONS)
    set_calc(CALCS.get('D'), zopts)
    set_basis(BASIS.get('aCQZ'), zopts)
    zopts.set('dboc', 'ON')
    ropts.set('jobname', molecule + "_dboc_D_aCQZ")
    joblist.append(name="DBOC ae-" + CALCS.get('D').proper_name + "/" + BASIS.get('aCTZ').proper_name,
                   zmat_options = zopts,
                   run_options = ropts)

    return joblist


#*************************************************************
# Main function. Don't modify this except to rename your script 
if __name__ == '__main__':

    #Process Docopts input
    args = docopt(__doc__, version="HEAT456Qp 1.0")

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

