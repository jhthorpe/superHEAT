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
# -------------------------------------------
# USER NOTES 
#
#
#
#  
# -------------------------------------------
# DEVELOPER NOTES 
#
# The script proceeds as follows:
#	1. Docopt generates keywords and arguments from command line. 
#
#	If listing jobs:
#	2. Job_List is created, and then queried via constraints from user
#	
#	If generating jobs:
#	2. The ZMAT class is initialized from disk
#	3. The Run  class is init
#	4. The Job_List class is initialized
#	5. user request recipies and jobs are generated 
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
    superHEAT.py --name=<name> --ZMAT=<zmat> --runfile=<run.sh>
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
import sys

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
        self.update('calc'    , Option(abrv = 'XXX', default = None       ) )
        self.update('basis'   , Option(abrv = 'YYY', default = None       ) )
        self.update('frzcore' , Option(abrv = 'ZZZ', default = None       ) )
        self.update('ccprog'  , Option(abrv = 'CCC', default = 'VCC'      ) )
        self.update('abcd'    , Option(abrv = 'AAA', default = 'STANDARD' ) )
        self.update('dboc'    , Option(abrv = 'DDD', default = 'OFF'      ) )
        self.update('rel'     , Option(abrv = 'RRR', default = 'OFF'      ) )
        self.update('newnorm' , Option(abrv = 'NNN', default = 'ON'       ) )
        self.update('multi'   , Option(abrv = None , default = 1          ) )
        self.update('ref'     , Option(abrv = None , default = 'UHF'      ) )

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
    #initialize from file
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
                if opt.abrv is None:
                    continue
                if opt.value is None:
                    print("Option ", name, "had ", None, "as it's value")
                    sys.exit()
                self.all_lines[idx] = self.all_lines[idx].replace(opt.abrv, opt.value)


    #write this zmat to a file
    def to_file(self, file):
        with open(file, "w") as f:
            for line in self.all_lines:
                f.write(line)
        f.close()

    #returns the reference supplied in the file, or 'UHF' if none is found
    def get_ref(self):
        ref = 'UHF'
  
        for line in self.all_lines:
            csv_line = line.split(",")
            for csv in csv_line:
                if 'REF=' in csv:
                    ref = line.split("=")[-1]
        return ref

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
        self.jobs    = []
        self.zmat    = copy.deepcopy(zmat)
        self.run     = copy.deepcopy(run)
        self.options = Option_List()
  
        #basis set lists
        self.XZ_list   = [     'PVDZ',      'PVTZ',      'PVQZ',      'PV5Z', 
                               'PV6Z',      'PV7Z',      'PV8Z'              ]   

        self.aXZ_list  = ['AUG-PVDZ' ,  'AUG-PVTZ',  'AUG-PVQZ',  'AUG-PV5Z', 
                          'AUG-PV6Z' ,  'AUG-PV7Z',  'AUG-PV8Z'              ]

        self.CXZ_list  = [    'PCVDZ',     'PCVTZ',     'PCVQZ',     'PCV5Z', 
                              'PCV6Z',     'PCV7Z',     'PCV8Z'              ]

        self.aCXZ_list = ['AUG-PCVDZ', 'AUG-PCVTZ', 'AUG-PCVQZ', 'AUG-PCV5Z', 
                          'AUG-PCV6Z', 'AUG-PCV7Z', 'AUG-PCV8Z'              ]

        self.make()


    #print all jobs
    def print(self):
        for idx in range(len(self.jobs)):
            self.jobs[idx].print()


    #print all job names and ids
    def print_names(self):
        for job in self.jobs:
            print(str(job.num).zfill(3), job.name)  


    #given a set of job ids, generate the jobs
    #note that the job ids begin at 1
    def generate(self):
        for job in self.jobs:
            job.generate()


    #appends a new job with some set of options 
    def append(self, name, options):
        self.jobs.append(Job( len(self.jobs),
                                        name, 
                                   self.zmat, 
                                    self.run,
                                     options ))

    #checks the ZMAT for the reference value 
    def set_ref(self):
        if (self.zmat != None):
            self.options.set('ref', zmat.get_ref())
        

    #This is called at the end of init, and generates the actual list of jobs
    #At the moment, this generates a HUGE list of jobs, which can 
    def make(self):

        self.set_ref()

        #SCF
        SCF_opts = copy.deepcopy(self.options) 
        SCF_opts.set(   'calc', 'SCF')
        SCF_opts.set('frzcore', 'OFF')
        for basis_set in [self.XZ_list, self.aXZ_list, self.CXZ_list, self.aCXZ_list]:
            for basis in basis_set:
                SCF_opts.set('basis', basis)
                self.append('ae-SCF/' + basis, SCF_opts)

        #SDQ-MP4

        #CCSD

        #CCSD(T)

        #CCSDT

        #CCSDT(Q)_L

        #CCSDTQ(P)_L

        #SFDC

        #DBOC


#*************************************************************
# Main function 
if __name__ == '__main__':
    
    #Process Docopts input
    args = docopt(__doc__, version="superHEAT 1.0")

    #if printing job ids
    if args['--joblist']:
        joblist = Job_List(None, None)
        joblist.print_names() 

    #generating job files
    else:
        #Read ZMAT
        zmat = ZMAT(args['--ZMAT'])
        zmat.print()

        #Read run.dummy
        rundummy = None

        joblist = Job_List(zmat, rundummy)

        #Generate users from constrained 
        print("\n joblist is...") #testin
        joblist.print_names() #testing
        joblist.print()

        joblist.generate() #testing

