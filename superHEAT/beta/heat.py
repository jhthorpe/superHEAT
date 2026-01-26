import pandas as pd
from HEAT_species import *

##############################################################################
# 
# This contains functions used to generate and manipulate pandas 
# dataframes of the HEAT data. Note that this will eventually be replaced 
# by custom classes that then use pandas internally


kJ2cm = 83.59347229110210
au2cm = 219474.6313631

##############################################################################
# UTILITY FUNCTIONS
#
# Extapolate with <X^-3 and (X+1/2)^-4>
#
def extrap_coef(x,y):
    return 0.5*( x**3/(y**3 - x**3) + (x+0.5)**4/((y+0.5)**4 - (x+0.5)**4) )

##############################################################################
#
# Load HEAT raw data and generate the various columns we need 
#
def load_heat():
    '''
    Loads heat data from "raw.csv" and generates columns.  
    '''


    data = pd.read_csv("raw.csv")
    
    # All but the first column are numerics
    #numeric_cols = data.columns.drop('Calculation')
    
    # Grab the columns we're going to need 
    recipe_ingredients = ["SCF/aCQZ", "CCSD/aCTZ", "CCSD/aCQZ", "[fc] CCSD/aTZ", "[fc] CCSD/aQZ", "[fc] (T) / aTZ", "[fc] (T) / aQZ", "PETER Anharmonic"]
    
    heat = data[recipe_ingredients].apply(pd.to_numeric, errors="coerce")
    heat['Species'] = data['Species'] 
    
    # Find rows that have NaN and warn they're going to be dropped 
    nan_rows = heat[heat.isna().any(axis=1)]
    print("Rows that will be removed with this recipe")
    print(nan_rows)
    
    # Modify ZPE since it's in cm-1 at the moment
    heat["PETER Anharmonic"] = heat["PETER Anharmonic"] / 219474.6313631
    
    #Drop t
    heat = heat.dropna(axis=0)
    
    # Start forming recipe
    heat['D/aC{T,Q}Z'] = heat['CCSD/aCQZ'] + (heat['CCSD/aCQZ'] - heat['CCSD/aCTZ']) * extrap_coef(3,4) 
    
    # (T) CBS estimate
    heat['(T) - D/aTZ'] = heat['[fc] (T) / aTZ'] - heat['[fc] CCSD/aTZ']
    heat['(T) - D/aQZ'] = heat['[fc] (T) / aQZ'] - heat['[fc] CCSD/aQZ']
    heat['(T)-D/a{T,Q}Z'] =  heat['(T) - D/aQZ'] + (heat['(T) - D/aQZ'] - heat['(T) - D/aTZ']) * extrap_coef(3,4)

    return heat


##############################################################################
#
# Generate reaction dataset using the "reaction" class
#
# TODO: look into if this can be done better by generating a transposed list, 
# and then adding columns.
#
def reaction_data(heat, reaction_list, column_list):
    '''
    Computes the data for a given set of reactions provided a heat dataframe

    Note: the species strings between reaction_list and heat 'Species' *must*
    be identical. In the future, we can instead use an internal indexing 
    scheme. 

    Input:
    heat          : original heat dataframe 
    reaction_list : list of Reaction class objects 
    column_list   : list of columns from dataframe we wish to create
    '''

    df = heat.set_index('Species')
    rxns = []

    for rxn in reaction_list:
        row = {'Reaction': rxn.name}

        for col in column_list:
            if col in df.columns:
                val = sum(
                    coef * df.loc[spec, col]
                    for spec, coef in rxn.stoich.items()
                )
            else:
                row[col] = None
        rxns.append(row)

    return pd.DataFrame(rxns)



##############################################################################
# 
# Call to generate all purely HEAT data
#
if __name__ == "__main__":
    heat = load_heat()

    print("Loaded HEAT set\n", heat)

    scf_conv_cols = ['SCF/aCTZ', 'SCF/aCQZ', 'SCF/aC5Z', 'SCF/aC6Z']
    scf_conv = reaction_data(heat, heat_tae, scf_conv_cols)

    print(scf_conv)

    
