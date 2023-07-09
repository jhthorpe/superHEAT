#*************************************************************
# runscripy.py
#	
#	JHT, July 9, 2023, Dallas, TX
#	- created
#
# defined the Runscript class, which contains variables and
# functions useful for processing and generating new runscripts
# based on options passed in from the user
#
#*************************************************************

import sys

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
  

