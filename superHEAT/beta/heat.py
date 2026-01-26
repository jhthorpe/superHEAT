import pandas as pd
import numpy as np
from HEAT_species import *
from atct_interface import fill_reactions
import asyncio

##############################################################################
# 
# This contains functions used to generate and manipulate pandas 
# dataframes of the HEAT data. Note that this will eventually be replaced 
# by custom classes that then use pandas internally


kJ2cm = 83.59347229110210
au2cm = 219474.6313631
au2kJ = au2cm / kJ2cm

##############################################################################
# UTILITY FUNCTIONS
#
# Extapolate with <X^-3 and (X+1/2)^-4>
#
def avg_schwenke(x,y):
    return 0.5*( x**3/(y**3 - x**3) + (x+0.5)**4/((y+0.5)**4 - (x+0.5)**4) )

##############################################################################
#
# Load HEAT raw data and generate the various columns we need 
#
def load_heat(col_keep):
    '''
    Loads heat data from "raw.csv", keeping only the data specificed by col_keep 
    '''

    data = pd.read_csv("raw.csv")
    
    # Grab the columns we're going to need 
    heat = data[col_keep].apply(pd.to_numeric, errors="coerce")
    heat['Species'] = data['Species'] 
    heat.index = heat['Species']

    # Find rows that have NaN and warn they're going to be dropped, and warn 
    nan_rows = heat[heat.isna().any(axis=1)]
    if (len(nan_rows) !=- 0):
        print(f"WARNING: Rows that will be removed with this recipe : {len(nan_rows)}")
        print(nan_rows)

    # Modify ZPE since it's in cm-1 at the moment
    zpe_names = ["PETER Anharmonic", "ZPE HEAT"]
    for name in zpe_names:
        if name in heat.columns:
            heat[name] = heat[name] / au2cm
    
    #Drop the Species with  
    heat = heat.dropna(axis=0)
    
    # Start forming recipe
#    heat['D/aC{T,Q}Z'] = heat['CCSD/aCQZ'] + (heat['CCSD/aCQZ'] - heat['CCSD/aCTZ']) * extrap_coef(3,4) 
    
    # (T) CBS estimate
#    heat['(T) - D/aTZ'] = heat['[fc] (T) / aTZ'] - heat['[fc] CCSD/aTZ']
#    heat['(T) - D/aQZ'] = heat['[fc] (T) / aQZ'] - heat['[fc] CCSD/aQZ']
#    heat['(T)-D/a{T,Q}Z'] =  heat['(T) - D/aQZ'] + (heat['(T) - D/aQZ'] - heat['(T) - D/aTZ']) * extrap_coef(3,4)

    return heat

##############################################################################
# 
# Generate two-point extrapolation data. 
#
#
def extrapolate_2p(df_other, func, extrapolations):
    """
    Generates new extrapolation columns of a given heat dataframe. 
    
    Takes as input a dictionary of columns and zetas, along with a
    coefficient function. The function must be of the Schwenke form:

    extrapolated_value = y_val + (y_val - x_val) * func(x_zeta, y_zeta)

    And the dictionary must be constructed with the following style

    {
       'new_col_name' : {
           'X_name' : 'X_col_name',
           'X_zeta' : X_col_zeta
           'Y_name' : 'Y_col_name',
           'Y_zeta' : Y_zeta
        }
    }
    """

    df = df_other 

    for col_name, extrap in extrapolations.items():
        df[col_name] = df[extrap["Y_name"]] + (df[extrap["Y_name"]] - df[extrap["X_name"]]) * func(extrap["X_zeta"], extrap["Y_zeta"])

    return df
        



##############################################################################
#
# Generate reaction dataset using the "reaction" class
#
# TODO: look into if this can be done better by generating a transposed list, 
# and then adding columns.
#
def reaction_data(heat, reaction_list, column_list, conversion = None):
    '''
    Computes the data for a given set of reactions provided a heat dataframe

    Note: the species strings between reaction_list and heat 'Species' *must*
    be identical. In the future, we can instead use an internal indexing 
    scheme. 

    TODO: Look into doing this with transpose dataframe instead, for better vectorization
          on large datasets. This is fine for now, though

    Input:
    heat          : original heat dataframe 
    reaction_list : list of Reaction class objects 
    column_list   : list of columns from dataframe we wish to create
    conversion    : optional input scalar to multiply values by
    '''

    df = heat.set_index('Species')
    rxns = []

    cc = 1. if conversion == None else conversion

    for rxn_name, rxn in reaction_list.items():
        row = {'Reaction': rxn.name}

        for col in column_list:
            if col in df.columns:
                val = sum(
                    coef * df.loc[spec, col]
                    for spec, coef in rxn.stoich.items()
                )
                row[col] = val * cc
            else:
                row[col] = None
        rxns.append(row)

    return pd.DataFrame(rxns)


##############################################################################
# 
# Add reaction data from ATcT to a dataframe indexed by species name
#
def add_atct(reaction_df, reactions):
    '''
    Adds ATcT values to a dataframe of reactions. 
    '''

    df = reaction_df.set_index('Reaction')

    filled_reactions = asyncio.run(fill_reactions(reactions))

    values = {key:reactions[key].value for key in reactions}
    uncs = {key:reactions[key].unc for key in reactions}

    print("Values are \n", values)
    print("unc are \n", uncs)

    df['ATcT Values'] = pd.Series(values)
    df['ATcT Unc'] = pd.Series(uncs)

    return df

##############################################################################
#
# Returns the l2deviation of some data, assuming no NaNs
#
def l2d(data):
    n = len(data)
    val = None if n <= 1 else np.sqrt(np.sum(np.square(data))/(n-1)) 
    return val



##############################################################################
# 
# Call to generate all purely HEAT data
#
# Eventually this will all be replaced with a "recipe" class, where you generate a desired recipe beforehand, 
# and use it to (semi) automate all this analysis
if __name__ == "__main__":

    #CCH is problematic at the moment, remove it from tests
    heat_tae.pop('CCH')

    #unapproximated superHEAT recipe
    # eventually name generation will be automated within this framework
    recipe_ingredients = ["SCF/aC6Z", "(T)/aC5Z", "(T)/aC6Z", "PETER Anharmonic"]
    heat = load_heat(recipe_ingredients)
    print("Loaded HEAT set\n", heat)

    # Extrapolated data
    heat = extrapolate_2p(heat, avg_schwenke, {
        '(T)/aC{5,6}Z' : {'X_name' : '(T)/aC5Z', 'X_zeta' : 5, 'Y_name' : '(T)/aC6Z', 'Y_zeta' : 6}
    })
    print("Extrapolated heat : \n", heat)

    # Now, form a test 
    example_list = ['SCF/aC6Z', '(T)/aC{5,6}Z', 'PETER Anharmonic']
    example_data = reaction_data(heat, heat_tae, example_list, conversion = au2kJ)
    example_data["Total"] = example_data['SCF/aC6Z'] + example_data['(T)/aC{5,6}Z'] + example_data['PETER Anharmonic']


    # Last step, add ATcT values for reactions
    example_data = add_atct(example_data, heat_tae)

    # Now we can do statistical analysis
    example_data["Err"] = example_data["ATcT Values"] - example_data["Total"]

    print("Example data\n", example_data)

    print(f"Mean error : {example_data["Err"].mean()}")
    print(f"Std.Dev. error : {example_data["Err"].std(ddof=1)}")
    print(f"CI : {l2d(example_data["Err"])}")


    
