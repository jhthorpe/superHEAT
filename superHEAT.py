#*************************************************************
# superHEAT.py
#
# 	JHT, June 28, 2023, Dallas, TX
#	-- created
#
# 
# .py script to generate the multitudes of ZMATs needed for
# testing or performing thermochemical calculations
#
# HOW TO USE
#
#  
# ADDING JOBS
#   To add a new job follow these steps
#	1. In the 
#
# ADDING OPTIONS
#   Sometimes you need to add a new option for this script to 
#   track. To do so, follow these steps:
# 
# 	1. In the Options_List constructor, add a call to self.update to inlclude the new required option 
#
#
#
#*************************************************************

#*************************************************************
# DOCOPT input string
"""superHEAT

Usage:
    superHEAT.py --ZMAT=<zmat> --runfile=<run.sh>
    superHEAT.py --joblist
    superHEAT.py (-h | --help)
    superHEAT.py --version

Options:
    --joblist     Print all predetermined jobs.
    -h --help     Show this screen.
    --version     Show version.

"""

from docopt import docopt
import copy

#*************************************************************
# Option class
#
# The option class is a wrapper around three things
#
# abrv		-- abbreviation for this option, used for substitution in ZMAT
# default	-- default value for this option
# value		-- actual value for this option, what will be substituted in 
#
class Option:

    def __init__(self, abrv, default):
        self.abrv    = abrv
        self.default = default
        self.value   = self.default

#*************************************************************
# Option list
#
# Contains a list of options.
#
class Option_List:
    
    def __init__(self):
        self.dict = {}

        #The following are "required" options that must be tracked
        self.update('calc'    , Option(abrv='XXX', default=None       ) )
        self.update('basis'   , Option(abrv='YYY', default=None       ) )
        self.update('frzcore' , Option(abrv='ZZZ', default=None       ) )
        self.update('ccprog'  , Option(abrv='CCC', default='VCC'       ) )
        self.update('abcd'    , Option(abrv='AAA', default='STANDARD' ) )
        self.update('dboc'    , Option(abrv='DDD', default='OFF'      ) )
        self.update('rel'     , Option(abrv='RRR', default='OFF'      ) )
        self.update('newnorm' , Option(abrv='NNN', default='ON'       ) )

    #print the options
    def print(self):
        print("Current list of options")
        for name, option in self.dict.items():
            print(name, option.abrv, option.default, option.value) 

    #update an option, which ADDS the option if it doesn't currently exist 
    def update(self, name, option):
        self.dict.update({name:option})

    #set an option's value
    def set(self, name, value):
        self.dict[name].value = value
    

#*************************************************************
# ZMAT class
# 
# This contains all the lines of the user-supplied ZMAT
#
class ZMAT:
    def __init__(self, file):

        print("Reading ZMAT from ", file)

        #strings that indicate we are at start of options section
        self.opt_start_strs = ['*CFOUR', '*CRAPS', '*ACES2']

        #read file from disk
        f = open(file, "r")
        self.all_lines = f.readlines()
        f.close()

    #print the line strings
    def print(self):
        print(self.all_lines)

    #replace substring with new string
    def replace(self, old_str, new_str):
        for idx in range(len(self.all_lines)):
            self.all_lines[idx] = self.all_lines[idx].replace(old_str, new_str)

    #Given an Options_List, replace all matching abrv in the ZMAT with the appropriate
    # values 
    def set_options(self, opt_list):
        for idx in range(len(self.all_lines)):
            for name, opt in opt_list.dict.items():
                if opt.value is None:
                    print("Option ", name, "had ", None, "as it's value")
                    exit
                self.all_lines[idx] = self.all_lines[idx].replace(opt.abrv, opt.value)

    #write this zmat to a file
    def to_file(self, file):
        with open(file, "w") as f:
            for line in self.all_lines:
                f.write(line)
        f.close()

#*************************************************************
# Job class
#
# This class contains information about a particular job (calculation)
# that the script should generate. Note that the initialization does 
# specifically deepcopy only, in order to prevent any unfortunate 
# accidents overwritting the orginal data
#
# Member variables:
#	num		: unique identifier for the job
#	name		: string name for the job
#	zmat		: ZMAT class object
#	run		: Run  class object 
#       options		: Options list for this job
#	zmat_name	: file to save zmat to
#       run_name  	: file to save runscript to
#
class Job:
    
    def __init__(self, num, name, zmat, run, options):
        self.num       = copy.deepcopy(num)
        self.name      = copy.deepcopy(name)
        self.zmat      = copy.deepcopy(zmat) #make sure we can't do anything bad
        self.run       = copy.deepcopy(run)
        self.options   = copy.deepcopy(options)
        self.zmat_name = "zmat." + str(num).zfill(3)
        self.run_name  = "run."  + str(num).zfill(3) 

    #print the job options
    def print(self):
        print("Job ", str(self.num).zfill(3), ":", self.name)
        self.options.print()
        print()

    #generate the run.xxx and zmat.xxx files
    def generate(self):
        self.zmat.set_options(self.options) 
        self.zmat.to_file(self.zmat_name)
        #TODO: add runfile support here

#*************************************************************
# Job_List
#
# This class is "just" a dictionary of Job class objects. The 
# user requests specific instances of jobs from within this list
#
# NOTE
# It is very important that any reordering of the job ids is done
# EXTREMELY carefully, as many users might write scripts that 
# process the output of these calculations based upon job ids 
#
class Job_List:

    def __init__(self, zmat, run):
        self.jobs = []
        self.zmat = copy.deepcopy(zmat)
        self.run  = copy.deepcopy(run)

        #Here we add the list of jobs. Note is it really important that you only 
        # APPEND to this list
        opts = Option_List()
        opts.set('calc'   , 'SCF')
        opts.set('basis'  , 'PVDZ')
        opts.set('frzcore', 'OFF')
        self.jobs.append(Job(num = len(self.jobs)+1, name = 'SCF/cc-pVDZ', 
                             zmat = self.zmat, run = self.run, options = opts)) 

    #print all jobs
    def print(self):
        for idx in range(len(self.jobs)):
            self.jobs[idx].print()

    #given a set of job ids, generate the jobs
    #note that the job ids begin at 1
    def generate(self, jobs):
        for idx in jobs:
            self.jobs[idx-1].generate()

#*************************************************************
# Main function 

#Global joblist
#JOB_LIST = Job_List()

if __name__ == '__main__':
    
    #Process Docopts input
    args = docopt(__doc__, version="superHEAT 1.0")
    print(args)
    print(args['--ZMAT'])

    #Read ZMAT
    zmat = ZMAT(args['--ZMAT'])
    zmat.print()

    joblist = Job_List(zmat, None)
    joblist.generate([1])
    print("\n joblist is...")
    joblist.print()

    zmat.print()


