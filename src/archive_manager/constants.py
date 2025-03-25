# constants.py 
#
# Contains the class and functions related to the tracking of a set of constants 
#
# Note that there is a minimum list of constants that MUST be present
#
# NOTES:
# March 25, 2025 @ ANL : JHT created. 
# 

# Constant class
# Tracks the value of some constant
# name    : name for lookup
# date    : the date this value was added/modified (year_month_day)
# note    : string containing details of constant
# value   : value of the constant
# unc     : uncertainty of the constant
# rel_unc : relative uncertainty of the constant
# unit    : units
class Constant:
    
    def __init__(self, name, date, note, value, unc, rel_unc, unit):
        self.name    = name
        self.date    = date
        self.note    = note
        self.value   = value
        self.unc     = unc
        self.rel_unc = rel_unc
        self.unit    = unit

    #returns a string to print
    def print_string(self):
        s  = "Constant           : " + self.name + '\n'
        s += "Date               : " + self.date + '\n'
        s += "Value              : " + str(self.value) + " " + self.unit + '\n'
        s += "Std. Unc.          : " + str(self.unc) + " " + self.unit + '\n'
        s += "Relative Std. Unc. : " + str(self.rel_unc) + " " + self.unit + '\n'
        s += "Note               : " + self.note + '\n'
        return s


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
    def __init__(self, set_name, set_date, set_note, file): 
        self.set_name = None
        self.set_date = None
        self.set_note = None
        self.constants = {}
        self.conversions = {}

'''
    #converts from Hartrees to kJ/mol
    def Eh_to_kJmol():

    #converts from Hartrees to kcal/mol
    def Eh_to_kcalmol():

    #converts from Hartrees to wavenumbers (reciprocal centimeters)
    def Eh_to_wn():

    #converts from Hartrees to electron volts 
    def Eh_to_eV():
'''
