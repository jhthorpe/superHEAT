#*************************************************************
#
# zmat.py
#	JHT, July 9, 2023, Dallas, TX:
#	- created
#
# Defines the Zmat class, which contains information and routines used
# to process and create new ZMATs depending on the options used. 
#
#*************************************************************

import sys

#*************************************************************
# ZMAT class
# 
# This contains all the lines of the user-supplied ZMAT
#
class Zmat:
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
                    ref = csv.split("=")[1]
        return ref

