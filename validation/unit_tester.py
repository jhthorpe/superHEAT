# unit_tester.py
#
# March 28, 2025 @ ANL : JHT added
#
# Unit testing 

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


def main():
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


if __name__ == "__main__":
    main()
