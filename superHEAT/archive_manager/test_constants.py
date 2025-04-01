from constants import *
from constarc import *
import json

#create archive

constarc = Constants_Archive("/Users/l00332323/superHEAT/archive")

print(constarc.print_string())

if "CFOUR_OLD" in constarc.constants_sets.keys():
    CFOUR_OLD = constarc.load_constants_set("CFOUR_OLD")

    print(CFOUR_OLD.print_string())

else:

    #Example of adding constants
    CFOUR_OLD = Constants_Set(set_name = "CFOUR_OLD", set_date = "2025_3_27", set_note = "testing stuff")
    
    a0 = Constant(name="a0", date="2025_3_25", note = "CFOUR_OLD", value = 0.5291772083E-10, unc = 0.0000000019E-10, rel_unc =  3.7E-9, unit = "m", is_exact=False) 
    hbar = Constant(name="hbar", date="2025_3_25", note = "CFOUR_OLD", value = 1, unc = 0., rel_unc =  0., unit = "atomic", is_exact=True) 
    
    CFOUR_OLD.update(a0)
    CFOUR_OLD.update(hbar)
    
    constarc.add_constants_set(CFOUR_OLD)



'''
CFOUR_OLD = Constants_Set(set_name = "CFOUR_OLD", set_date = "2025_3_27", set_note = "testing stuff")


#name, date, note, value, unc, rel_unc, unit
a0 = Constant(name="a0", date="2025_3_25", note = "CFOUR_OLD", value = 0.5291772083E-10, unc = 0.0000000019E-10, rel_unc =  3.7E-9, unit = "m", is_exact=False) 
hbar = Constant(name="hbar", date="2025_3_25", note = "CFOUR_OLD", value = 1, unc = 0., rel_unc =  0., unit = "atomic", is_exact=True) 

CFOUR_OLD.update(a0)
CFOUR_OLD.update(hbar)

print(CFOUR_OLD.print_string())


CFOUR_OLD.json_dump("CFOUR_OLD.json")

#try writing to file
with open("test.json", "w", encoding="utf-8") as f:
    json.dump(a0.to_dict(), f, sort_keys=True, ensure_ascii=False)
    f.write('\n')
    json.dump(hbar.to_dict(), f, sort_keys=True, ensure_ascii=False)
    f.write('\n')


NEW_SET = Constants_Set(set_name = "FOO", set_date = "2025-3-27", set_note = "another test")
with open("test.json", "r", encoding="utf-8") as f:
    for line in f:
        NEW_SET.update(Constant.from_dict(json.loads(line)))

print(NEW_SET.print_string())


#TRY THE CONSTANTS ARCHIVE
constarc = Constants_Archive("/Users/l00332323/superHEAT/archive")
'''
