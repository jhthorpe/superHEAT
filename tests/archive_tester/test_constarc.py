from constants import *
from constarc import *
import json

def test_constarc():
    TEST_PATH = "test_constants_archive"
    TESTS_PASS = True
    
    #Fixed archive for testing
    seta = Constants_Set(set_name = "test_seta", set_date = "yyyy-mm-dd", set_note = "Testing set a") 
    setb = Constants_Set(set_name = "test_setb", set_date = "yyyy-mm-dd", set_note = "Testing set b") 
    
    #Fixed constants for testing
    seta_c1 = Constant(name = "a_c1", date = "yyyy-mm-dd", note = "seta const 1", value = 1, unc = 0, rel_unc = 0, unit = ".", is_exact = True)
    seta_c2 = Constant(name = "a_c2", date = "yyyy-mm-dd", note = "seta const 2", value = 2.0E-1, unc = 0.1E-1, rel_unc = 5.0E-2, unit = ".", is_exact = False)
    
    setb_c1 = Constant(name = "b_c1", date = "yyyy-mm-dd", note = "setb const 1", value = 1, unc = 0, rel_unc = 0, unit = ".", is_exact = True)
    setb_c2 = Constant(name = "b_c2", date = "yyyy-mm-dd", note = "setb const 2", value = 2.0E-1, unc = 0.1E-1, rel_unc = 5.0E-2, unit = ".", is_exact = False)
    
    seta.add_constant(seta_c1)
    seta.add_constant(seta_c2)
    
    setb.add_constant(setb_c1)
    setb.add_constant(setb_c2)
    
    #If test archive exists, delete it
    if os.path.exists(TEST_PATH):
        os.remove(TEST_PATH)
    
    
    #create archive
    constarc = Constants_Archive(TEST_PATH)
    
    #add constants
    
    #load constants
    
    #compare against tests above
    
    #delete archive
    os.path.remove(TEST_PATH)
    
    if (TESTS_PASS):
        return 0
    else:
        return 1 
