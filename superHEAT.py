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
#
# ADDING OPTIONS
#   Sometimes you need to add a new option for this script to 
#   track. To do so, follow these steps:
# 
# 	1. In the Options_List constructor, add a call to self.update to inlclude the new required option 
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
#        self.update('calc'    , Option(abrv='XXX', default=None       ) )
#        self.update('calc'    , Option(abrv='XXX', default=None       ) )
#        self.update('basis'   , Option(abrv='YYY', default=None       ) )
#        self.update('frzcore' , Option(abrv='ZZZ', default=None       ) )
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

    #update an option
    def update(self, name, option):
        self.dict.update({name:option})

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
# that the script should generate. 
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
        self.num       = num
        self.name      = name
        self.zmat      = zmat
        self.run       = run
        self.options   = options 
        self.zmat_name = "zmat." + str(num).zfill(3)
        self.run_name  = "run."  + str(num).zfill(3) 

    #print the job options
    def print(self):
        print("Job ", str(num).zfill(3), ":", self.name)
        self.options.print()
        print()

    #generate the run.xxx and zmat.xxx files
    def generate(self):
        self.zmat.set_options(self.options) 
        self.zmat.to_file(self.zmat_name)


#*************************************************************
# Main function 

if __name__ == '__main__':
    
    #Process Docopts input
    args = docopt(__doc__, version="superHEAT 1.0")
    print(args)
    print(args['--ZMAT'])

    #Read ZMAT
    zmat = ZMAT(args['--ZMAT'])
    zmat.print()

    job001 = Job(1, "test", zmat, None, Option_List()) 
    job001.generate()


