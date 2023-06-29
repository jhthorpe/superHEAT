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
# The various options one might want are described Option class. The ZMAT and run files
# contain abreviated codes that are then substituted out for the correct strings
#
# ADDING OPTIONS
#   Sometimes you need to add a new option for this script to 
#   track. If it is a ZMAT option, add it to the set_ZMAT_default 
#   function in the Options class. If it is a runfile option, add it 
#   to the set_run_default function.  
# 
#   
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

    #print the options
    def print(self):
        for name, option in self.dict.items():
            print(name, option.abrv, option.default, option.value) 

    #update an option, which ADDS the option if it doesn't currently exist 
    def update(self, name, option):
        self.dict.update({name:option})

    #set an option's value
    def set(self, name, value):
        self.dict[name].value = value

    #set default options for ZMAT
    def set_ZMAT_default(self):
        #The following are "required" options that must be tracked
        self.update('calc'    , Option(abrv = 'XXX', default = None       ) )
        self.update('basis'   , Option(abrv = 'YYY', default = None       ) )
        self.update('frzcore' , Option(abrv = 'ZZZ', default = None       ) )
        self.update('ccprog'  , Option(abrv = 'CCC', default = 'VCC'      ) )
        self.update('abcd'    , Option(abrv = 'AAA', default = 'STANDARD' ) )
        self.update('dboc'    , Option(abrv = 'DDD', default = 'OFF'      ) )
        self.update('rel'     , Option(abrv = 'RRR', default = 'OFF'      ) )
        self.update('newnorm' , Option(abrv = 'NNN', default = 'ON'       ) )
        self.update('multi'   , Option(abrv =  None, default = 1          ) )
        self.update('ref'     , Option(abrv =  None, default = 'UHF'      ) )

    #set default options for runfile
    def set_run_default(self):
        #the following are the required options that must be tracked
        self.update('jobname'    , Option(abrv = 'JJJ', default = None       ) )
        self.update('jobid'      , Option(abrv = 'XXX', default = None       ) )
        self.update('xcfour'     , Option(abrv = 'XC4', default = None       ) )
        
#*************************************************************
# Basis
#
# Basis class, which contains information about some basis function
class Basis:
    
    def __init__(self, proper_name, GENBAS_name, short_name):
        self.proper_name = proper_name
        self.GENBAS_name = GENBAS_name
        self.short_name  = short_name
    

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
# runscript
# 
# Class that manages the generation of runscripts for the jobs.
#
# Upon initialization, it reads run.dummy from disk
#
class Runscript:
  
    #initialize from disk
    def __init__(self, file):
        print("Reading run.dummy from ", file)
        f = open(file, "r")
        self.all_lines = f.readlines()
        f.close()


    #print lines
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
    
    def __init__(self, num, name, zmat, zmat_options, run, run_options):
        self.num            = copy.deepcopy(num)
        self.name           = copy.deepcopy(name)
        self.zmat           = copy.deepcopy(zmat) #make sure we can't do anything bad
        self.zmat_options   = copy.deepcopy(zmat_options)
        self.run            = copy.deepcopy(run)
        self.run_options    = copy.deepcopy(run_options)
        self.zmat_name      = "zmat." + str(num).zfill(3)
        self.run_name       = "run."  + str(num).zfill(3) 

    #print the job options
    def print(self):
        print("Job ", str(self.num).zfill(3), ":", self.name)
        self.zmat_options.print()
        self.run_options.print()
        print()

    #generate the run.xxx and zmat.xxx files
    def generate(self):
        self.run_options.set('jobid', str(self.num).zfill(3))
        self.zmat.set_options(self.zmat_options) 
        self.zmat.to_file(self.zmat_name)
        self.run.set_options(self.run_options) 
        self.run.to_file(self.run_name)

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

    def __init__(self, molecule, zmat, run):
        self.jobs         = []
        self.molecule     = copy.deepcopy(molecule)
        self.zmat         = copy.deepcopy(zmat)
        self.run          = copy.deepcopy(run)
        self.zmat_options = Option_List()
        self.run_options  = Option_List()

        self.zmat_options.set_ZMAT_default()
        self.run_options.set_run_default()
  
        #basis set lists
        self.XZ_list   = [ Basis(proper_name='cc-pVDZ', GENBAS_name='PVDZ', short_name = 'DZ'),
                           Basis(proper_name='cc-pVTZ', GENBAS_name='PVTZ', short_name = 'TZ'),
                           Basis(proper_name='cc-pVQZ', GENBAS_name='PVQZ', short_name = 'QZ'),
                           Basis(proper_name='cc-pV5Z', GENBAS_name='PV5Z', short_name = '5Z'),
                           Basis(proper_name='cc-pV6Z', GENBAS_name='PV6Z', short_name = '6Z'),
                           Basis(proper_name='cc-pV7Z', GENBAS_name='PV7Z', short_name = '7Z'),
                           Basis(proper_name='cc-pV8Z', GENBAS_name='PV8Z', short_name = '8Z')
                         ]

        self.aXZ_list  = [ Basis(proper_name='aug-cc-pVDZ', GENBAS_name='AUG-PVDZ', short_name = 'aDZ'),
                           Basis(proper_name='aug-cc-pVTZ', GENBAS_name='AUG-PVTZ', short_name = 'aTZ'),
                           Basis(proper_name='aug-cc-pVQZ', GENBAS_name='AUG-PVQZ', short_name = 'aQZ'),
                           Basis(proper_name='aug-cc-pV5Z', GENBAS_name='AUG-PV5Z', short_name = 'a5Z'),
                           Basis(proper_name='aug-cc-pV6Z', GENBAS_name='AUG-PV6Z', short_name = 'a6Z'),
                           Basis(proper_name='aug-cc-pV7Z', GENBAS_name='AUG-PV7Z', short_name = 'a7Z'),
                           Basis(proper_name='aug-cc-pV8Z', GENBAS_name='AUG-PV8Z', short_name = 'a8Z')
                         ]

        self.CXZ_list  = [ Basis(proper_name='cc-pCVDZ', GENBAS_name='PCVDZ', short_name = 'CDZ'),
                           Basis(proper_name='cc-pCVTZ', GENBAS_name='PCVTZ', short_name = 'CTZ'),
                           Basis(proper_name='cc-pCVQZ', GENBAS_name='PCVQZ', short_name = 'CQZ'),
                           Basis(proper_name='cc-pCV5Z', GENBAS_name='PCV5Z', short_name = 'C5Z'),
                           Basis(proper_name='cc-pCV6Z', GENBAS_name='PCV6Z', short_name = 'C6Z'),
                           Basis(proper_name='cc-pCV7Z', GENBAS_name='PCV7Z', short_name = 'C7Z'),
                           Basis(proper_name='cc-pCV8Z', GENBAS_name='PCV8Z', short_name = 'C8Z')
                         ]

        self.aCXZ_list = [ Basis(proper_name='aug-cc-pCVDZ', GENBAS_name='AUG-PCVDZ', short_name = 'aCDZ'),
                           Basis(proper_name='aug-cc-pCVTZ', GENBAS_name='AUG-PCVTZ', short_name = 'aCTZ'),
                           Basis(proper_name='aug-cc-pCVQZ', GENBAS_name='AUG-PCVQZ', short_name = 'aCQZ'),
                           Basis(proper_name='aug-cc-pCV5Z', GENBAS_name='AUG-PCV5Z', short_name = 'aC5Z'),
                           Basis(proper_name='aug-cc-pCV6Z', GENBAS_name='AUG-PCV6Z', short_name = 'aC6Z'),
                           Basis(proper_name='aug-cc-pCV7Z', GENBAS_name='AUG-PCV7Z', short_name = 'aC7Z'),
                           Basis(proper_name='aug-cc-pCV8Z', GENBAS_name='AUG-PCV8Z', short_name = 'aC8Z')
                         ]
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
    def append(self, name, zmat_options, run_options):
        self.jobs.append(Job( len(self.jobs),
                                        name, 
                                   self.zmat, 
                                zmat_options,
                                    self.run,
                                 run_options 
                          ))

    #checks the ZMAT for the reference value 
    def set_ref(self):
        if (self.zmat != None):
            self.zmat_options.set('ref', zmat.get_ref())
        

    #This is called at the end of init, and generates the actual list of jobs
    #At the moment, this generates a HUGE list of jobs, which can 
    def make(self):

        if self.molecule == None:
            self.molecule = ''

        #parse the reference from ZMAT
        self.set_ref()

        #run options
        run_opts = copy.deepcopy(self.run_options)

        #SCF
        SCF_opts = copy.deepcopy(self.zmat_options) 
        SCF_opts.set(   'calc', 'SCF')
        SCF_opts.set('frzcore', 'OFF')
        for basis_set in [self.XZ_list, self.aXZ_list, self.CXZ_list, self.aCXZ_list]:
            for basis in basis_set:
                SCF_opts.set('basis', basis.GENBAS_name)
                run_opts.set('jobname' , self.molecule + "_ae-SCF_" + basis.short_name) 
                run_opts.set('xcfour'  , 'xcfour')
                self.append('ae-SCF/' + basis.proper_name, SCF_opts, run_opts)

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
        joblist = Job_List(None, None, None)
        joblist.print_names() 

    #generating job files
    else:
        #Read ZMAT
        zmat = ZMAT(args['--ZMAT'])
        zmat.print()

        #Read run.dummy
        rundummy = Runscript(args['--runfile'])
        rundummy.print()

        joblist = Job_List(args['--name'], zmat, rundummy)

        #Generate users from constrained 
        print("\n joblist is...") #testin
        joblist.print_names() #testing
        joblist.print()

        joblist.generate() #testing

