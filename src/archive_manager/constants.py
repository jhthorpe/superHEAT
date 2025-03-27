# constants.py 
#
# Contains the class and functions related to the tracking of a set of constants 
#
# Note that there is a minimum list of constants that MUST be present
#
# NOTES:
# March 25, 2025 @ ANL : JHT created. 
# 

from datetime import datetime
from decimal import Decimal
import json

# Constant class
# Tracks the value of some constant
# name     : name for lookup
# date     : the date this value was added/modified (year_month_day)
# note     : string containing details of constant
# value    : value of the constant
# unc      : uncertainty of the constant
# rel_unc  : relative uncertainty of the constant
# unit     : units
# is_exact : bool for if a constant is exact
#
# TODO : make pretty printing...
class Constant:
    
    def __init__(self, name, date, note, value, unc, rel_unc, unit, is_exact):
        self.name     = name
        self.date     = date
        self.note     = note
        self.value    = value
        self.unc      = unc
        self.rel_unc  = rel_unc
        self.unit     = unit
        self.is_exact = is_exact

    #returns a string to print
    def print_string(self):
        if not self.is_exact:
            (sign, dig, exponent) = Decimal(self.rel_unc).as_tuple()
            numdig = len(dig) + exponent - 1
            s  = "Constant           : " + self.name + '\n'
            s += "Date               : " + self.date + '\n'
            s += "Value              : " + f"{self.value:.{-numdig}e}" + " " + self.unit + '\n'
            s += "Std. Unc.          : " + format(self.unc, 'e') + " " + self.unit + '\n'
            s += "Relative Std. Unc. : " + format(self.rel_unc, 'e') + " " + self.unit + '\n'
            s += "Note               : " + self.note + '\n'
        else:
            s  = "Constant           : " + self.name + '\n'
            s += "Date               : " + self.date + '\n'
            s += "Value              : " + "{:e}".format(self.value) + " " + self.unit + '\n'
            s += "Std. Unc.          : " + "exact\n"
            s += "Relative Std. Unc. : " + "exact\n" 
            s += "Note               : " + self.note + '\n'
        return s

    #create instance from dictionary
    @classmethod
    def from_dict(cls, dictionary):
        return cls(name = dictionary["name"], date = dictionary["date"], note = dictionary["note"], value = dictionary["value"], unc = dictionary["unc"], rel_unc = dictionary["rel_unc"], unit = dictionary["unit"], is_exact = dictionary["is_exact"])

    #returns a python dictionary
    def to_dict(self):
        return {"name" : self.name, "date" : self.date, "note" : self.note, "value" : self.value, "unc" : self.unc, "rel_unc" : self.rel_unc, "unit" : self.unit, "is_exact" : self.is_exact}


# Constants_Set
# Manages a named set of constants. Includes 
# member functions for useful conversions between units
# 
# set_name : name of this set
# set_date : date this set was generated (year_month_day)
# set_note : notes on this set
# constants : dictionary of constants in the set
#
class Constants_Set:

    #Initialize the set from metadata (name, nate, note). NOTE that this is performed
    # separately from the file load. The file name is just the set name
    def __init__(self, set_name, set_date, set_note): 
        self.set_name = set_name
        self.set_date = set_date
        self.set_note = set_note
        self.constants = {}

    #Read from a .json file, takes file name as arguement
    def json_load(self, file_name):
        with open(file_name, 'r', encoding="utf-8") as f:
            for line in f:
                const = Constant.from_dict(json.loads(line))
                self.constants[const.name] = const

    #Write to a .json file, with newline as delimination between json objects
    def json_dump(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            for key, constant in self.constants.items():
                json.dump(constant.to_dict(), f, sort_keys=True, ensure_ascii=False)
                f.write('\n')

    #update the constants set
    def update(self, constant):
        self.constants[constant.name] = constant

    #return string for printing constants
    def print_string(self):
        s  = "Constants set :" + self.set_name + '\n'
        s += "Date          :" + self.set_date + '\n'
        s += "Notes         :" + self.set_note + '\n'
        s += "Constants in set \n"

        for key, constant in self.constants.items():
            s += constant.print_string() + '\n'
        return s

    #returns a dictionary of the metadata
    def meta_to_dict(self):
        return {'set_name' : self.set_name, 'set_date' : self.set_date, 'set_note' : self.set_note} 

    #creates metadata from dictionary
    @classmethod
    def meta_from_dict(cls, d):
        return cls(set_name = d['set_name'], set_date = d['set_date'], set_note = d['set_note']) 

