#*************************************************************
# template.py 
#
#       JHT, July 10, 2023, Dallas, TX
#       -- created
# 
# An example of how to use this repository to generate 
# CFOUR input and runscript files for a template, two-step 
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
"""template

Usage:
    template.py --name=<name> --ZMAT=<zmat> --runfile=<run.sh> 
    template.py --joblist 
    template.py (-h | --help)
    template.py --version

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
# set of jobs you want constructed. The Job-id numbers will be 
# constructed automatically for you, in the order that you 
# append the jobs to the list
#
# NOTE: DO NOT modify any pre-defined global variables
#
def make_joblist(molecule=None, zmat=None, run=None):
    joblist = Joblist(molecule=molecule, zmat=zmat, run=run)

    #add your job construction here
    #see examples for more detail

    return joblist


#*************************************************************
# Main function. Don't modify this except to rename your script 
if __name__ == '__main__':

    #Process Docopts input
    args = docopt(__doc__, version="template 1.0")

    #if printing joblist
    if args['--joblist']:
        joblist = make_joblist()
        joblist.print_names() #printing for now, save to file later

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

