##############################################
# unit_tester.py
#
# March 28, 2025 @ ANL : JHT added
#
# Unit testing 
##############################################

##############################################
#DOCOPT STRING
#
"""unit_test

Usage:
    unit_test.py [-j <ntask>]

Options:
    -j  Number of concurrent tests to run [default: 1]

"""

##############################################
from docopt import docopt
import concurrent.futures
import sys

import time

#from constarc import *
#from archive_tester import * 

TEST_PASS = 0
TEST_FAIL = 1

def call_member_func(obj, func):
    func = getattr(obj, func)
    return func()

def success():
    return TEST_PASS 

def fail():
    return TEST_FAIL

class unit_test:
    def __init__(self, func, name, note):
        self.func = func
        self.name = name
        self.note = note
        self.future = None
        self.result = None

    def execute(self):
        self.result = self.func()


##############################################
# MAIN
#
if __name__ == "__main__":

    args = docopt(__doc__, version="Unit Tester 1.0")
    ntask = args['-j'] 
    if ntask > 100 :
        ntask = 1
    if ntask < 1 :
        ntask = 1

    test_list = []

    #Add tests here
    test_list.append(unit_test(func = success, name = "Default Pass", note= 'None'))
    test_list.append(unit_test(func = fail, name = "Default Fail", note= 'None'))

    with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
        futures = [executor.submit(call_member_func, test, "execute") for test in test_list] 

    #print the results
    print('{name: <30} {note: <50} {result: <10}'.format(name='Name', note='Note', result='Result'))
    for test in test_list:
        rstring = ""
        if (test.result == TEST_PASS):
            rstring = "SUCCESS"
        else:
            rstring = "FAIL"
        print('{name: <30} {note: <50} {result: <10}'.format(name=test.name, note=test.note, result=rstring))


