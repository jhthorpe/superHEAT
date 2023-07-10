#*************************************************************
# job.py
#
#	JHT, July 9, 2023, Dallas, TX
#		- created
#
# Defines the Job and Joblist classes
#
# Job:
#	A single job to be generated 
#
# Joblist:
#	A list of jobs to be generated
#*************************************************************
import sys
import copy
from zmat import *
from runscript import *
from option import *

#*************************************************************
# Job class
#
# This class contains information about a particular job (calculation)
# that the script should generate. Note that the initialization does 
# specifically deepcopy only, in order to prevent any unfortunate 
# accidents overwritting the orginal data
#
# Member variables:
#       num             : unique identifier for the job
#       name            : string name for the job
#       zmat            : ZMAT class object
#       run             : Run  class object 
#       options         : Options list for this job
#       zmat_name       : file to save zmat to
#       run_name        : file to save runscript to
#
class Job:

    def __init__(self, num, name, zmat, zmat_options, run, run_options):
        self.num            = copy.deepcopy(num)
        self.name           = copy.deepcopy(name)
        self.zmat           = copy.deepcopy(zmat) 
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

    #generate the run.xxx and zmat.xxx files
    def generate(self):
        self.run_options.set('jobid', str(self.num).zfill(4))
        self.zmat.set_options(self.zmat_options)
        self.zmat.to_file(self.zmat_name)
        self.run.set_options(self.run_options)
        self.run.to_file(self.run_name)

#*************************************************************
# Joblist
#
# This class is "just" a dictionary of Job class objects. The 
# user requests specific instances of jobs from within this list
#
class Joblist:

    def __init__(self, molecule, zmat, run, zmat_options=ZMAT_OPTIONS, run_options=RUN_OPTIONS):
        self.jobs         = []
        self.molecule     = copy.deepcopy(molecule)
        self.zmat         = copy.deepcopy(zmat)
        self.run          = copy.deepcopy(run)
        self.zmat_options = zmat_options 
        self.run_options  = run_options 


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
        self.jobs.append(Job( len(self.jobs)+1,
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

    #generate the jobs
    def generate(self):
        f = open('joblist.txt', 'w')
        idx = 1
        for job in self.jobs:
            job.generate()
            f.write(str(idx).zfill(4) +  "  " +  job.name)
            idx = idx + 1
        f.close() 

