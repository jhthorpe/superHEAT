# constants.py 
#
# Contains the class and functions related to the tracking of a set of constants 
#
# Note that there is a minimum list of constants that MUST be present
#
# NOTES:
# March 25, 2025 @ ANL : JHT created. 
# 

from decimal import Decimal

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
# conversions : dictionary of conversions in the set
#
class Constants_Set:

    #Initialize the set from metadata (name, nate, note) and a file object that is positioned to be read
    def __init__(self, set_name, set_date, set_note, file=None): 
        self.set_name = None
        self.set_date = None
        self.set_note = None
        self.constants = {}
        self.conversions = {}

'''
    #write constants and conversions to a text file 
    def save_txt(self, file):
        return 
    #converts from Hartrees to kJ/mol
    def Eh_to_kJmol():

    #converts from Hartrees to kcal/mol
    def Eh_to_kcalmol():

    #converts from Hartrees to wavenumbers (reciprocal centimeters)
    def Eh_to_wn():

    #converts from Hartrees to electron volts 
    def Eh_to_eV():
'''


#TESTING
