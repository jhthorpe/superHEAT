#*************************************************************
# recipe.py
#
#	JHT, July 9, 2023, Dallas, TX
#		- created
#
# Defines the Job, Recipe classes
#
# Job
#	- this defines a job, which is a combination of options
#
# Recipe
#	- a collection of jobs
#
#*************************************************************

import sys
from superHEAT.script_generator.job import *

#*************************************************************
# Recipe class
#
class Recipe:
    
    def __init__(self, file): 
        self.file = file
        self.jobs = []

        #read the recipe from file
        print("Reading recipe from ", self.file) 
        f = open(file, "r")
        self.all_lines = f.readlines()
        f.close() 

        #add unique jobs based on the lines in the file 
        for line in self.all_lines:

            njob = Job(line)

            found = False
            for job in self.jobs:
                if (njob == job):
                    found = True
                    break 
            if (not found): 
                self.jobs.add(njob)


    #print all jobs
    def print(self):
        print("There are ", len(self.jobs), " jobs")
        idx = 0
        for job in self.jobs:
            print("Job #", job, job.print()) 
 
