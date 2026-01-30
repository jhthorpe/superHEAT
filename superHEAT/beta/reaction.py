# reaction.py
#
# reaction dataclass 

# Reaction class
#
# Name is some string 
# stoich is a dictionary of species strings and the stoichiometry of that species in the reaction
#

from atct import (
    get_species,
    calculate_reaction_enthalpy,
    get_species_covariance_by_atctid,
    get_species_covariance_matrix,
    create_reaction_calculator,
    healthcheck,
    search_species,
    get_species_by_smiles,
    get_species_by_casrn,
    get_species_by_formula,
    get_species_by_name,
    get_species_by_inchi,
    get_species_by_inchikey,
    get_species_covariance_by_atctid,
    get_species_covariance_matrix,
    as_dataframe
)
from atct import ReactionSpecies, ReactionResult


from species import Elements, Species

#
# TODO: make it so that reaction accepts dict of Species instead of strings
#
# name   : a string representing reaction name
# stoich : a dictionary that pairs strings representing reactants/products 
#              and their stoichiometry (- for reactants, + for products). Note
#              that these are used in lookups
# value  : value of the reaction quantity
# unc    : uncertainty of the reaction
#
class Reaction():
    '''Class that represents a reaction  '''

    #construct
    def __init__(self, name=None, stoich=None, value=None, unc=None):
        self.name = name
        if stoich is None:
            self.stoich = {}
        else:
            self.stoich = stoich
        self.value = None
        self.unc = None

    # Return ATcT query for this reaction, given an external dictionary
    # of Species
    def atct_0K_query(self, species_dict = Species):
        atct_dict = {}
        for name, num in self.stoich.items():
            atct_dict[species_dict[name].atct_id] = num
        atct_query = {
            'covariance_298K': calculate_reaction_enthalpy(atct_dict,   'covariance', use_0k = False), 
            'conventional_0K': calculate_reaction_enthalpy(atct_dict, 'conventional', use_0k =  True)
        }
        return atct_query

    def rxn_str(self):
        p_plus = False
        r_plus = False
        rct_s = ""
        prd_s = ""
        for spec, num in self.stoich.items():
            if num > 0:
                if p_plus:
                    prd_s += " + "
                else:
                    p_plus = True
                if num == 1:
                    prd_s += f"{spec}"
                else:
                    prd_s += f"{num:>} {spec}"
            elif num < 0:
                if r_plus:
                    rct_s += " + "
                else:
                    r_plus = True
                if num == -1:
                    rct_s += f"{spec}"
                else:
                    rct_s += f"{-num:>} {spec}"
        return rct_s + " -> " + prd_s


    def __str__(self):
        rxn_s = self.rxn_str()
        val_s = "" 
        if (self.value is None):
            val_s += f" ( N/A"
        else:
            val_s += f" ({self.value:>8.3f}"
        if (self.unc is not None):
            val_s += f" +/- {self.unc:>5.3f} kJ/mol)"
        else:
            val_s += f" +/- N/A kJ/mol)"
        return rxn_s + val_s 

    def __eq__(self, other):
        '''
        Compare two reactions.
        '''
        if isinstance(other, Reaction):
            for a_s, a_n in self.stoich.items():
                if (abs(a_n) < 1e-14):
                    continue
                found = False
                for b_s, b_n in other.stoich.items():
                    if (a_s == b_s and abs(a_n - b_n) < 1e-14):
                        found = True
                        continue
                if not found:
                    return False
            for b_s, b_n in other.stoich.items():
                if (abs(b_n) < 1e-14):
                    continue
                found = False
                for a_s, a_n in self.stoich.items():
                    if (a_s == b_s and abs(a_n - b_n) < 1e-14):
                        found = True
                        continue
                if not found:
                    return False
            return True     
        else:
            return NotImplemented
