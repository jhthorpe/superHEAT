# species.py
#
# Contains the Species class

import copy

#empty_elements = {
#        'H' : 0,
#        'C' : 0,
#        'N' : 0,
#        'O' : 0,
#        'F' : 0
#}

empty_elements = {}

class Elements:
    '''Class that represents elements information within Species'''

    def __init__(self, element_dict = None):
        self.element_dict = copy.deepcopy(empty_elements)
        if element_dict is not None:
            for element, num in element_dict.items():
                self.element_dict[element] = num

    def __getitem__(self, other):
        return self.element_dict[other]

    def items(self):
        return self.element_dict.items()

    def count(self, name):
        return self.element_dict.get(name, 0)

    def __str__(self):
        s = ""
        for element, num in self.element_dict.items():
            if (num > 0):
                s += f"{element:2<}:{num:4>}\n"
        return s


class Species:
    '''Class that represents species information'''

    def __init__(self, name = None, atct_id = None, elements = None, dfh0k = None):
        self.name = name
        self.atct_id = atct_id
        self.dfh0k = dfh0k
        self.elements = Elements(elements) 

    def __str__(self):
        return f"{self.name} ({self.atct_id})\nDfH(0K):{self.dfh0k} kJ/mol\n{self.elements}"



