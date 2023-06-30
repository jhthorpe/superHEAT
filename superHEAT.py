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
# TODO: modify Job_List to do different xcfour commands
#
# -------------------------------------------
# USER NOTES 
#
#
# In order to generate a set of jobs, you need to know which jobs to make. Here you have a few options.
# 	1. You can use a preconstructed recipe
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
# -------------------------------------------
# ADDING A BASIS
#     1. Go to the Basis class. Below it are a list of globally defined basis functions. Add yours there. 
#        Its global name should start with b_, to indicate this is a basis
#
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
        self.update('jobname'    , Option(abrv = 'JJJ'  , default = None       ) )
        self.update('jobid'      , Option(abrv = 'xxxxx', default = None       ) )
        self.update('xcfour'     , Option(abrv = 'XC4'  , default = None       ) )

    def print(self):
        for key, option in self.dict.items():
            print("Option:", key, ", abrv:", option.abrv, ", default:", option.default)
        
#*************************************************************
# Basis_Set
#
# Basis_Set class, which contains information about some basis set. 
#
# Member variables:
# proper_name		- name you would see in the lit. ex: cc-pVDZ, 6-31G, etc.
# GENBAS_name		- name to find in the GENBAS file
# short_name		- name to identify in this script
# zeta			- cannonical order of the basis
# type			- type of basis set. ex: Dunning, Pople, ANO, etc.
#
class Basis_Set:
    
    # NOTE: 
    # If you modify the member variables, make sure to modify the "select" function in 
    # Basis as well!
    def __init__(self, proper_name, GENBAS_name, short_name, zeta, style):
        self.proper_name = proper_name
        self.GENBAS_name = GENBAS_name
        self.short_name  = short_name
        self.zeta        = zeta
        self.style       = style

    def print(self):
        print("Proper Name:", self.proper_name, ", GENBAS name:", self.GENBAS_name, 
              ", short_name:", self.short_name, ", zeta:", self.zeta, ", style:", self.style)

#*************************************************************
# Basis
#
# A container for Basis_Set.
#
class Basis:

    def __init__(self):
        self.dict =  {}

    def add(self, basis_set):
        self.dict.update({basis_set.short_name : basis_set})

    def print(self):
        for key, basis in self.dict.items():
            basis.print()

    def short_names(self):
        for key, basis in self.dict.items():
            print(basis.short_name)

    def get(self, short_name):
        return self.dict[short_name]

    #this returns a new Basis object, with only the basis sets that match those requested by the user
    # for example:
    #   dunning_basis = Basis.select(style='Dunning') 
    # will contain ONLY dunning basis sets
    def select(self, proper_name=None, GENBAS_name=None, short_name=None, zeta=None, style=None):
        new_basis = Basis()
        for key, basis in self.dict.items():
            if ( proper_name != None ) and ( basis.proper_name != proper_name ): continue
            if ( GENBAS_name != None ) and ( basis.GENBAS_name != GENBAS_name ): continue
            if (  short_name != None ) and (  basis.short_name != short_name  ): continue
            if (        zeta != None ) and (        basis.zeta != zeta        ): continue
            if (       style != None ) and (       basis.style != style       ): continue
            new_basis.add(basis)
        return new_basis
 
   
# Global basis variable set
# To add a new basis to be tracked, append it in the style you see below. 
#
# NOTE: 
# 	1. This is a dictionary update, so adding a collision will overwrite
# 	2. Changing ANYTHING here will cause jobid numbers to change, and thus should be done very very carefully

BASIS = Basis()
BASIS.add( Basis_Set(proper_name='cc-pVDZ', GENBAS_name='PVDZ', short_name = 'DZ', zeta = 2, style = 'Dunning') ) 
BASIS.add( Basis_Set(proper_name='cc-pVTZ', GENBAS_name='PVTZ', short_name = 'TZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pVQZ', GENBAS_name='PVQZ', short_name = 'QZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV5Z', GENBAS_name='PV5Z', short_name = '5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV6Z', GENBAS_name='PV6Z', short_name = '6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV7Z', GENBAS_name='PV7Z', short_name = '7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pV8Z', GENBAS_name='PV8Z', short_name = '8Z', zeta = 8, style = 'Dunning') )
 
BASIS.add( Basis_Set(proper_name='aug-cc-pVDZ', GENBAS_name='AUG-PVDZ', short_name = 'aDZ', zeta = 2, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pVTZ', GENBAS_name='AUG-PVTZ', short_name = 'aTZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pVQZ', GENBAS_name='AUG-PVQZ', short_name = 'aQZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV5Z', GENBAS_name='AUG-PV5Z', short_name = 'a5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV6Z', GENBAS_name='AUG-PV6Z', short_name = 'a6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV7Z', GENBAS_name='AUG-PV7Z', short_name = 'a7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pV8Z', GENBAS_name='AUG-PV8Z', short_name = 'a8Z', zeta = 8, style = 'Dunning') )

BASIS.add( Basis_Set(proper_name='cc-pCVDZ', GENBAS_name='PCVDZ', short_name = 'CDZ', zeta = 2, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCVTZ', GENBAS_name='PCVTZ', short_name = 'CTZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCVQZ', GENBAS_name='PCVQZ', short_name = 'CQZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV5Z', GENBAS_name='PCV5Z', short_name = 'C5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV6Z', GENBAS_name='PCV6Z', short_name = 'C6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV7Z', GENBAS_name='PCV7Z', short_name = 'C7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='cc-pCV8Z', GENBAS_name='PCV8Z', short_name = 'C8Z', zeta = 8, style = 'Dunning') )

BASIS.add( Basis_Set(proper_name='aug-cc-pCVDZ', GENBAS_name='AUG-PCVDZ', short_name = 'aCDZ', zeta = 2, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCVTZ', GENBAS_name='AUG-PCVTZ', short_name = 'aCTZ', zeta = 3, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCVQZ', GENBAS_name='AUG-PCVQZ', short_name = 'aCQZ', zeta = 4, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV5Z', GENBAS_name='AUG-PCV5Z', short_name = 'aC5Z', zeta = 5, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV6Z', GENBAS_name='AUG-PCV6Z', short_name = 'aC6Z', zeta = 6, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV7Z', GENBAS_name='AUG-PCV7Z', short_name = 'aC7Z', zeta = 7, style = 'Dunning') )
BASIS.add( Basis_Set(proper_name='aug-cc-pCV8Z', GENBAS_name='AUG-PCV8Z', short_name = 'aC8Z', zeta = 8, style = 'Dunning') )

#*************************************************************
# Calc
#
# Calc class, which consists of different information about various 
# type of calculations. 
#
# Member variables:
# proper_name		- true name of the calculation
# ZMAT_name		- what needs to go with the CALC= section of ZMAT
# short_name		- shorthand for this calc
# rhf_cc		- CC_PROG subroutine to use in RHF case
# uhf_cc		- CC_PROG subroutine to use in UHF case
# rohf_cc		- CC_PROG subroutine to use in ROHF case
# 
#
class Calc:
    
    #NOTE
    # If you change or add parameters here, be sure to update Calcs.select member function
    #   to match!!
    def __init__(self, proper_name, ZMAT_name, short_name, rhf_cc, uhf_cc, rohf_cc, nbody):
        self.proper_name = proper_name
        self.ZMAT_name   = ZMAT_name
        self.short_name  = short_name
        self.rhf_cc      = rhf_cc
        self.uhf_cc      = uhf_cc
        self.rohf_cc     = rohf_cc         
        self.nbody       = nbody

    def print(self):
        print(proper_name, ZMAT_name, short_name, rhf_cc, uhf_cc, rohf_cc, nbody)

#*************************************************************
# Calcs
#
# Calcs class, which contains a dict of the various calcs contained. 
#
class Calcs:

    def __init__(self):
        self.dict = {}

    def add(self, calc):
        self.dict.update({calc.short_name:calc})

    def print(self):
        for key, calc in self.dict.items():
            calc.print()

    def short_names(self):
        for key, calc in self.dict.items():
            print(calc.short_name)

    def get(self, short_name):
        return seld.dict[short_name]

    #this returns a new Calc object, with only the calcs that match those requested by the user
    # for example:
    #   t2_calcs = CALCS.select(nbody=2) 
    # 
    # NOTE: if a new parameter for the Calc class is added, it should also be updated here
    def select(self, proper_name=None, ZMAT_name=None, short_name=None, rhf_cc=None, uhf_cc=None,
               rohf_cc=None, nbody=None):
        new_calcs = Calcs()
        for key, calc in self.dict.items():
            if ( proper_name != None ) and ( calc.proper_name != proper_name ): continue
            if (   ZMAT_name != None ) and (   calc.ZMAT_name != ZMAT_name   ): continue
            if (  short_name != None ) and (  calc.short_name != short_name  ): continue
            if (      rhf_cc != None ) and (      calc.rhf_cc != rhf_cc      ): continue
            if (      uhf_cc != None ) and (      calc.uhf_cc != uhf_cc      ): continue
            if (     rohf_cc != None ) and (     calc.rohf_cc != rohf_cc     ): continue
            if (       nbody != None ) and (       calc.nbody != nbody       ): continue
            new_calcs.add(calc)
        return new_calcs

#Calcs global variable
CALCS = Calcs()

CALCS.add( Calc(proper_name = "SCF",          ZMAT_name = "SCF",                    short_name = "scf",
                     rhf_cc = "NCC",             uhf_cc = "NCC",                       rohf_cc = "VCC",
                      nbody = 1) )
    
CALCS.add( Calc(proper_name = "MP2",          ZMAT_name = "MP2",                    short_name = "mp2",
                     rhf_cc = "VCC",             uhf_cc = "VCC",                       rohf_cc = "VCC",
                      nbody = 2) )

CALCS.add( Calc(proper_name = "SDQ-MP4",      ZMAT_name = "SDQ-MP4",                short_name = "sdqmp4",
                     rhf_cc = "VCC",             uhf_cc = "VCC",                       rohf_cc = "VCC",
                      nbody = 2) )

CALCS.add( Calc(proper_name = "CCSD",         ZMAT_name = "CCSD",                   short_name = "D", 
                     rhf_cc = "NCC",             uhf_cc = "ECC",                       rohf_cc = "VCC",
                      nbody = 2) )

CALCS.add( Calc(proper_name = "CCSD(T)",      ZMAT_name = "CCSD(T)",                short_name = "pt", 
                     rhf_cc = "NCC",             uhf_cc = "ECC",                       rohf_cc = "VCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSD(T)_L",    ZMAT_name = "CCSD(T)_L",              short_name = "ptL", 
                     rhf_cc = "NCC",             uhf_cc = "ECC",                       rohf_cc = "VCC",
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT",        ZMAT_name = "CCSDT",                  short_name = "T", 
                     rhf_cc = "NCC",             uhf_cc = "ECC",                       rohf_cc = "VCC", 
                      nbody = 3) )

CALCS.add( Calc(proper_name = "CCSDT(Q)",     ZMAT_name = "CCSDT(Q)",               short_name = "pq", 
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC", 
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDT(Q)_L",   ZMAT_name = "CCSDT(Q)_L",             short_name = "pqL", 
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC", 
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDTQ",       ZMAT_name = "CCSDTQ",                 short_name = "Q", 
                     rhf_cc = "NCC",             uhf_cc = "MRCC",                      rohf_cc = "MRCC", 
                      nbody = 4) )

CALCS.add( Calc(proper_name = "CCSDTQ(P)_L",  ZMAT_name = "CC(n-1)(n)_L, EXCITE=5", short_name = "ppL", 
                     rhf_cc = "MRCC",            uhf_cc = "MRCC",                      rohf_cc = "MRCC", 
                      nbody = 5) )

CALCS.add( Calc(proper_name = "CCSDTQP(H)_L", ZMAT_name = "CC(n-1)(n)_L, EXCITE=6", short_name = "phL", 
                     rhf_cc = "MRCC",            uhf_cc = "MRCC",                      rohf_cc = "MRCC", 
                      nbody = 6) )

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
        self.zmat_name      = "zmat." + str(num).zfill(4)
        self.run_name       = "run."  + str(num).zfill(4) 

    #print the job options
    def print(self):
        print("Job ", str(self.num).zfill(4), ":", self.name)
        self.zmat_options.print()
        self.run_options.print()
        print()

    #generate the run.xxx and zmat.xxx files
    def generate(self):
        self.run_options.set('jobid', str(self.num).zfill(4))
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
        self.make()


    #print all jobs
    def print(self):
        for idx in range(len(self.jobs)):
            self.jobs[idx].print()


    #print all job names and ids
    def print_names(self):
        for job in self.jobs:
            print(str(job.num).zfill(4), job.name)  


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
        zmat_opts = copy.deepcopy(self.zmat_options) 
        zmat_opts.set(   'calc', 'SCF')
        zmat_opts.set('frzcore', 'OFF')
        scf_basis = BASIS.select(style='Dunning')
        for key, basis in scf_basis.dict.items(): 
            zmat_opts.set('basis', basis.GENBAS_name)
            run_opts.set('jobname' , self.molecule + "_ae-scf_" + basis.short_name) 
            run_opts.set('xcfour'  , 'xcfour')
            self.append('ae-SCF/' + basis.proper_name, zmat_opts, run_opts)

        '''
        #SDQ-MP4
        zmat_opts = copy.deepcopy(self.zmat_options) 
        zmat_opts.set(   'abcd', 'AOBASIS')
        zmat_opts.set(   'calc', 'SDQ-MP4')
        zmat_opts.set( 'ccprog', 'VCC')

        zmat_opts.set('frzcore', 'OFF')
        for basis_set in [b_XZ_list, b_aXZ_list, b_CXZ_list, b_aCXZ_list]:
            for basis in basis_set:
                zmat_opts.set('basis', basis.GENBAS_name)
                run_opts.set('jobname' , self.molecule + "_ae-sdqmp4_" + basis.short_name) 
                run_opts.set('xcfour'  , 'xcfour')
                self.append('ae-SDQ-MP4/' + basis.proper_name, zmat_opts, run_opts)

        zmat_opts.set('frzcore', 'ON')
        for basis_set in [b_XZ_list, b_aXZ_list, b_CXZ_list, b_aCXZ_list]:
            for basis in basis_set:
                zmat_opts.set('basis', basis.GENBAS_name)
                run_opts.set('jobname' , self.molecule + "_fc-sdqmp4_" + basis.short_name) 
                run_opts.set('xcfour'  , 'xcfour')
                self.append('fc-SDQ-MP4/' + basis.proper_name, zmat_opts, run_opts)
        '''
        
        #CCSD

        #CCSD(T)

        #CCSDT

        #CCSDT(Q)_L

        #CCSDTQ(P)_L

        #SFDC

        #DBOC

#*************************************************************
# Constraints
#
# A class that gathers constraints that define a unique calculation 
#
class Constraints:
    
    def __init__(self):
        self.dict = {'type':None, #options: DBOC, SREL, NREE 
                     'calc':None, #
                     'basis':None}

    


#*************************************************************
# Recipe
#
# A recipe is just a list of jobs that we want to execute. 
#
class Recipe:

    #initialize with some list of jobs
    def __init__(self, joblist):
         self.joblist = joblist

    #add job to list
    def add(self, job):
        self.joblist.append(job)

    #read from file
    def from_file(self, file):
        with open(file, "r") as f:
            lines = f.readlines()             
        f.close()

        #process input 
        for line in lines:
            csv = line.split(",")

            #process constraints 
            for item in csv:
                continue
                


#*************************************************************
# Reicpies
#
# This is a list of (potentially) useful recipies


#*************************************************************
# Main function 

BASIS.short_names()
CALCS.short_names()

if __name__ == '__main__':
    
    #Process Docopts input
    args = docopt(__doc__, version="superHEAT 1.0")

    #if printing job ids
    if args['--joblist']:
        joblist = Job_List(None, None, None)

        joblist.print_names() 

    elif args['--show']:
        if args['--basis'   ]: 
            print("Available Basis Sets")
            BASIS.print()

        if args['--calcs'   ]: 
            print("Available Calculations")
            CALCS.print()

        if args['--ZMATopts']: 
            print("Modifiable options in ZMAT")
            zmatopts = Option_List()
            zmatopts.set_ZMAT_default()
            zmatopts.print()

        if args['--runopts']: 
            print("Modifiable options in runfile")
            runopts = Option_List()
            runopts.set_run_default()
            runopts.print()
            

    #generating job files
    else:
        #Read ZMAT
        zmat = ZMAT(args['--ZMAT'])

        #Read run.dummy
        rundummy = Runscript(args['--runfile'])

        #Generate the basic joblist
        joblist = Job_List(args['--name'], zmat, rundummy)

        #Generate the recipe
        

        #generate the jobs with a particular recipe
        joblist.generate() #testing

