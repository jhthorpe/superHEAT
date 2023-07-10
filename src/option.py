#*************************************************************
#
# option.py
#	JHT, July 9, 2023, Dallas, TX
#	-- created
# 
# Contains the Option and Options class, and the ZMAT_OPTIONS
# global member variable. Option is a POD 
# type that defines a string and a value to substitute in that
# string when  
#
# Option:
#	A POD type that defines a string and a value to 
#	substitute for that string
#
# Options:
#	A collection of Option types
#
#*************************************************************

#*************************************************************
# Option class
#
# The option class is a wrapper around three things
#
# abrv          -- abbreviation for this option, used for substitution in text files
# default       -- default value for this option
# value         -- actual value for this option, what will be substituted 
#
class Option:

    def __init__(self, abrv, default, description=None):

        self.abrv        = abrv
        self.default     = default
        self.value       = self.default
        self.description = description

    def print(self):
        print(self.abrv,"->",self.value,":",self.description)

#*************************************************************
# Options 
#
# Contains a list of options.
#
class Options:

    def __init__(self):
        self.dict = {}

    #print the options
    def print(self):
        for name, option in self.dict.items():
            print(name, option.abrv, "->", option.value, ":", option.description)

    #update an option, which ADDS the option if it doesn't currently exist 
    def update(self, name, option):
        self.dict.update({name:option})

    #set an option's value
    def set(self, name, value):
        self.dict[name].value = value

    #get an option's value
    def get(self, name):
        return self.dict[name].value


#*************************************************************
# ZMAT_OPTIONS
# 
# Global that contains the list of default options

ZMAT_OPTIONS = Options()
RUN_OPTIONS = Options()

# The list of default ZMAT options tracked
ZMAT_OPTIONS.update('calc'    , Option(abrv = 'XXX', default = None      , description="Calculation"  ) )
ZMAT_OPTIONS.update('basis'   , Option(abrv = 'YYY', default = None      , description="Basis"        ) )
ZMAT_OPTIONS.update('frzcore' , Option(abrv = 'ZZZ', default = 'OFF'     , description="Frozen-Core"  ) )
ZMAT_OPTIONS.update('ccprog'  , Option(abrv = 'CCC', default = 'VCC'     , description="CC_PROG"      ) )
ZMAT_OPTIONS.update('abcd'    , Option(abrv = 'AAA', default = 'STANDARD', description="ABCD"         ) )
ZMAT_OPTIONS.update('dboc'    , Option(abrv = 'DDD', default = 'OFF'     , description="DBOC"         ) )
ZMAT_OPTIONS.update('rel'     , Option(abrv = 'RRR', default = 'OFF'     , description="Relativistic" ) )
ZMAT_OPTIONS.update('newnorm' , Option(abrv = 'NNN', default = 'ON'      , description="NEWNORM"      ) )
ZMAT_OPTIONS.update('multi'   , Option(abrv =  None, default = 1         , description="Multiplicity" ) )
ZMAT_OPTIONS.update('ref'     , Option(abrv =  None, default = 'UHF'     , description="Reference"    ) )

# The list of default runscript options tracked
RUN_OPTIONS.update('jobname'    , Option(abrv = 'JJJ'  , default = None ,     description="Jobname"      ) )
RUN_OPTIONS.update('jobid'      , Option(abrv = 'xxxxx', default = None ,     description="Job-ID"       ) )
RUN_OPTIONS.update('xcfour'     , Option(abrv = 'XC4'  , default = 'xcfour' , description="xcfour"       ) )
