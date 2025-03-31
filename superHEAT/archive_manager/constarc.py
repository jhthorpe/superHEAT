# constarc.py 
#
# Contains the Constants_Archive class, which manages the creation and retrieval of 
# historical data of universal constants and conversions
#
# NOTES:
# March 27, 2025 @ ANL : JHT created. 
# 
#

# Constants_Archive class
#
# This is a dictionary of Constants_Set classes, which are
# themselves a dictionary of Constants.
#
# The primary roll of the Constants_Archive is to set and retrieve 
# values from within the archive file structure.
# 
# Initialization requires an os.path object that directs the function to the 
# top level archive directory 
#
# The constants archive is constructed on two levels. The archive and "metadata" regarding
# the sets constained are listed in archive/constants/constarc.json", which are read in first. 
#
# Then, any given set of constants can be loaded from the file listed in this metadata, which will 
# be contained in the file:
#   archive/constants/name_of_file.json
#
# These json files are newline deliminated json objects
#
# NOTE :
#   All constants and constants sets are converted to uppercase names to support case-insensitive file systems
#
import os
import json
import sys
import copy
from superHEAT.archive_manager import constants

class Constants_Archive:
    
    # Initialize archive based on if the top path is set or not 
    def __init__(self, top_archive_path):
        self.path = os.path.join(top_archive_path, "constants")
        self.archive_file_name = os.path.join(self.path, "constarc.json")
        self.constants_sets = {}

        #Check if the top path is valid
        try: 
            if not os.path.exists(top_archive_path):
                raise RuntimeError("Top level archive path not valid, are you use you unzipped it?") 
        except RuntimeError as error:
            print("ERROR", error)
            sys.exit(1)

        #Check if the constants path exists or if this needs to be created 
        if not os.path.exists(self.archive_file_name):
            print("WARNING : No constants archive detected, generating now...")
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            with open(self.archive_file_name, 'w', encoding='utf-8') as f:
                os.utime(self.archive_file_name, None)

        #If the archive exists, we load it 
        else:
            print("Loading constants archive metadata from {path}".format(path=self.archive_file_name))
            with open(self.archive_file_name, "r", encoding="utf-8") as f:
                for line in f:
                    new_set = constants.Constants_Set.meta_from_dict(json.loads(line))
                    self.constants_sets[new_set.set_name] = new_set 

    # Aquire a copy of a Constants_Set
    def load_constants_set(self, name):
        self.constants_sets[name].json_load(os.path.join(self.path, self.constants_sets[name].set_name + ".json"))
        return copy.deepcopy(self.constants_sets[name])

    # Print a list of Constants_Sets
    def print_string(self):
        s = "Sets of constants available on the archive\n"
        for key, cset in self.constants_sets.items():
            s += "Set name : " + cset.set_name + '\n' 
            s += "Set date : " + cset.set_date + '\n'
            s += "Notes    : " + cset.set_note + '\n\n'
        return s


    #Add a new constants set to the archive
    def add_constants_set(self, new_set): 

        assert not new_set.set_name in self.constants_sets, \
                "A set called {name} already exists in the Constants Archive".format(name=new_set.set_name)
        assert not os.path.exists(os.path.join(self.path, new_set.set_name + ".json")), \
                "{name}.json already exists in the archive".format(namnew_set.set_name)

        #All checks have passed, add to the set
        self.constants_sets[new_set.set_name] = new_set

        #All checks have passed, write the .json file first (just in case) and then append to the archive metadata file
        new_set.json_dump(os.path.join(self.path, new_set.set_name + ".json"))

        #APPEND to constarc.json
        with open(self.archive_file_name, "a", encoding='utf-8') as f:
            json.dump(new_set.meta_to_dict(), f, sort_keys=True, ensure_ascii=False)
            f.write('\n')

    #Delete a set of constants from the archive
    def delete_constants_set(self, old_set_name):

        #Check that the old set actually exists 
        if old_set_name in self.constants_sets:
            #remove set from dict
            self.constants_sets.remove(old_set_name)

            #Remove the .json file for this set
            os.remove(os.path.join(self.path, old_set_name + '.json'))
 
            #update the metadata file without this set
            with open(self.archive_file_name, "w", encodint='utf-8') as f:
                for name, cset in self.constants_sets.items():
                    json.dump(cset.meta_to_dict(), f, sort_keys=True, ensure_ascii=False)
                    f.write('\n')
