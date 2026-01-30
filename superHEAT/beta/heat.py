import pandas as pd
import numpy as np
from HEAT_species import *
from recipe import Ingredient, Transformation, Recipe
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
#
# Ingredient, coef based transformation functions
#
def extrapolate(df, ingr, coefs):
    '''
    Extrapolate function for use in Transformation

    df      : dataframe to operate on
    ingr    : ingredient dictionary 
    coefs   : coefficients dictionary
    '''
    return df[ingr['Y'].name] + (df[ingr['Y'].name] - df[ingr['X'].name]) * coefs['C']

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

    # drop the "zeta" row
    if 'Zeta 1' in heat.columns:
        heat = heat.drop('Zeta 1', axis=0) 
    
    return heat

##############################################################################
# 
# Generate two-point extrapolation data. 
#
def extrapolate_2p(df_other, extrapolations):
    """
    Generates new extrapolation columns of a given heat dataframe. 
    
    Takes as input a dictionary of columns and zetas, along with a
    coefficient function. The function must be of the Schwenke form:

    extrapolated_value = y_val + (y_val - x_val) * coef 

    And the dictionary must be constructed with the following style

    {
       'new_col_name' : {
            'X'  : X column name,
            'Y'  : Y column name,
            'C'  : coefficient 
        }
    }
    """

    df = df_other 

    for col_name, extrap in extrapolations.items():
        df[col_name] = df[extrap['Y']] + (df[extrap['Y']] - df[extrap['X']]) * extrap['C'] 

    return df
        
##############################################################################
#
# Generate core-valence data
#
def minus(df_other, calcs):
    '''
    Contstructs returns the difference between columns 'A' and 'B':
    A - B

    Dictionary must be of style:

    'new column name' :
    {
        'A' : 'all electron column'
        'B' : 'frozen-core column'
    }
    '''

    df = df_other
    for result, cv in calcs.items():
        df[result] = df[cv['A']] - df[cv['B']]

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
        row = {'Reaction': rxn_name}

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
def add_atct(reaction_df, reactions, conversion = 1.):
    '''
    Adds ATcT values to a dataframe of reactions. 
    '''

    df = reaction_df.set_index('Reaction')

    filled_reactions = asyncio.run(fill_reactions(reactions))

    values = {key:reactions[key].value for key in reactions}
    uncs = {key:reactions[key].unc for key in reactions}

    df['ATcT Values'] = pd.Series(values) * conversion
    df['ATcT Unc'] = pd.Series(uncs) * conversion

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

#    bad_species = ["CCH", "NH", "CH", "HO2", "OF", "CN" ]
    bad_species = ["CCH"]

    # go through and remove reactions with bad species
    for set_name, data in {'TAE' : heat_tae, 'ANL' : heat_anl, 'BDE' : heat_bde}.items():
        bad_list = []

        for name, rxn in data.items():
            for bad in bad_species:
                for spec in rxn.stoich: 
                    if (bad == spec):
                        bad_list.append(name)

        #remove duplicates
        bad_list = list(dict.fromkeys(bad_list)) 

        print(f"Following reactions were removed from {set_name}")
        print(bad_list)

        for bad in bad_list:
            data.pop(bad)
    
    # create the "all" dataset
    duplicates = []
    heat_all = heat_tae | heat_anl | heat_bde
    for name, rxn in heat_all.items():
        for name2, rxn2 in heat_all.items():
            if name2 != name and rxn == rxn2:
                    duplicates.append(name2)

    print("The following were identified as duplicates")
    print(duplicates)

    for dup in duplicates:
        heat_all.pop(dup)

    # screen all for formally identical reactions

    # This is how we'd eventually like to do things, but I'm out of time now
    # Generate the recipes we want to look at 
    # superHEAT = Recipe(name = "superHEAT")

    # SCF
    # superHEAT.add_ingredient(Ingredient(name = "SCF/aC6Z"))

    # CCSD
    # CHECK that result from transform defaults to true, here
    # superHEAT.add_transformation(Transformation(
    #    name = "[fc] CCSD/aCV{5,6}Z",
    #    func = extrapolate,
    #    result = Ingredient(name = "[fc] CCSD/aCV{5,6}Z"),
    #    ingredients = {'X' : Ingredient(name = "[fc] CCSD/aC5Z"),
    #                   'Y' : Ingredient(name = "[fc] CCSD/aC6Z")},
    #    coefs = { 'C' : avg_schwenke(5, 6) }
    #))

    # Add raw data
    # BE CAREFUL NOT TO ADD DUPLICATES
    recipe_ingredients = [
        "SCF/aC6Z",
        "[fc] CCSD/aC6Z", "[fc] CCSD/aC7Z",
        "CCSD/aC5Z", "CCSD/aC6Z", "[fc] CCSD/aC5Z",
        "[fc] (T)/aC5Z", "[fc] (T)/aC6Z",
        "(T)/aC5Z", "(T)/aC6Z",
        "[fc] (T) / 5Z", "[fc] (T) / 6Z",
        "[fc] T / 5Z", "[fc] T / 6Z",
        "[fc] (T)/aCTZ", "[fc] (T)/aCQZ",
        "(T)/aCTZ", "(T)/aCQZ",
        "[fc] T / aCTZ", "[fc] T / aCQZ",
        "T / aCTZ", "T / aCQZ",
        "[fc] T / QZ", 
        "[fc] (Q)_L / QZ", "[fc] (Q)_L / 5Z", 
        "[fc] (Q)_L / aCTZ", "(Q)_L / aCTZ",
        "[fc] (Q)_L / TZ",
        "[fc] Q / TZ",
        "[fc] Q / DZ",
        "[fc] (P)_L / DZ",
        "SF SCF / uaCQZ", "NR SCF / uaCQZ",
        "NR D / uaCTZ", "NR D / uaCQZ", "SF D / uaCTZ", "SF D / uaCQZ",
        "NR (T) / uaCTZ", "NR (T) / uaCQZ", "SF (T) / uaCTZ", "SF (T) / uaCQZ",
        "DBOC SCF / aCTZ", "DBOC D / aCTZ", "[fc] DBOC D / TZ", "[fc] DBOC T / TZ", "[fc] DBOC T / DZ", "[fc] DBOC Q / DZ",
        'SO (Hill Van Vleck/Hougen)',
        "PETER Anharmonic" 
    ]

    #remove accidental duplicates
    recipe_ingredients = list(dict.fromkeys(recipe_ingredients))

    # NOTE: this will eventually be replaced by internal functions that query a dataset
    heat = load_heat(recipe_ingredients)

    print("Loaded HEAT set\n", heat)

    # Add extrapolated data
    # Extrapolated data
    heat = extrapolate_2p(heat, {
        '[fc] CCSD/aC{6,7}Z'    : { 'X' : '[fc] CCSD/aC6Z',     'Y' : '[fc] CCSD/aC7Z',     'C' : avg_schwenke(6,7) },
        '[ae] CCSD/aC{5,6}Z'    : { 'X' : 'CCSD/aC5Z',          'Y' : 'CCSD/aC6Z',          'C' : avg_schwenke(5,6) },
        '[fc] CCSD/aC{5,6}Z'    : { 'X' : '[fc] CCSD/aC5Z',     'Y' : '[fc] CCSD/aC6Z',     'C' : avg_schwenke(5,6) },
        '[fc] CCSD(T)/aC{5,6}Z' : { 'X' : '[fc] (T)/aC5Z',      'Y' : '[fc] (T)/aC6Z',      'C' : avg_schwenke(5,6) },
        '[ae] CCSD(T)/aC{5,6}Z' : { 'X' : '(T)/aC5Z',           'Y' : '(T)/aC6Z',           'C' : avg_schwenke(5,6) },
        '[fc] CCSD(T)/{5,6}Z'   : { 'X' : '[fc] (T) / 5Z',      'Y' : '[fc] (T) / 6Z',      'C' : avg_schwenke(5,6) },
        '[fc] CCSDT/{5,6}Z'     : { 'X' : '[fc] T / 5Z',        'Y' : '[fc] T / 6Z',        'C' : avg_schwenke(5,6) },
        '[fc] CCSD(T)/aC{T,Q}Z' : { 'X' : '[fc] (T)/aCTZ',      'Y' : '[fc] (T)/aCQZ',      'C' : avg_schwenke(3,4) },
        '[ae] CCSD(T)/aC{T,Q}Z' : { 'X' : '(T)/aCTZ',           'Y' : '(T)/aCQZ',           'C' : avg_schwenke(3,4) },
        '[fc] CCSDT/aC{T,Q}Z'   : { 'X' : '[fc] T / aCTZ',      'Y' : '[fc] T / aCQZ',      'C' : avg_schwenke(3,4) },
        '[ae] CCSDT/aC{T,Q}Z'   : { 'X' : 'T / aCTZ',           'Y' : 'T / aCQZ',           'C' : avg_schwenke(3,4) },
        '[fc] CCSDT/{Q,5}Z'     : { 'X' : '[fc] T / QZ',        'Y' : '[fc] T / 5Z',        'C' : avg_schwenke(4,5) },
        '[fc] CCSDT(Q)L/{Q,5}Z' : { 'X' : '[fc] (Q)_L / QZ',    'Y' : '[fc] (Q)_L / 5Z',    'C' : avg_schwenke(4,5) },
        'NR CCSD/uaC{T,Q}Z'     : { 'X' : 'NR D / uaCTZ',       'Y' : 'NR D / uaCQZ',       'C' : avg_schwenke(3,4) },
        'SF CCSD/uaC{T,Q}Z'     : { 'X' : 'SF D / uaCTZ',       'Y' : 'SF D / uaCQZ',       'C' : avg_schwenke(3,4) },
        'NR CCSD(T)/uaC{T,Q}Z'  : { 'X' : 'NR (T) / uaCTZ',     'Y' : 'NR (T) / uaCQZ',     'C' : avg_schwenke(3,4) },
        'SF CCSD(T)/uaC{T,Q}Z'  : { 'X' : 'SF (T) / uaCTZ',     'Y' : 'SF (T) / uaCQZ',     'C' : avg_schwenke(3,4) }
    })

    # Add core-valence data
    # Core-Valence data
    heat = minus(heat, {
        '[cv] CCSD/aC{5,6}Z'    : { 'A' : '[ae] CCSD/aC{5,6}Z',     'B' : '[fc] CCSD/aC{5,6}Z' },
        '[cv] CCSD(T)/aC{5,6}Z' : { 'A' : '[ae] CCSD(T)/aC{5,6}Z',  'B' : '[fc] CCSD(T)/aC{5,6}Z' },
        '[cv] CCSD(T)/aC{T,Q}Z' : { 'A' : '[ae] CCSD(T)/aC{T,Q}Z',  'B' : '[fc] CCSD(T)/aC{T,Q}Z' },
        '[cv] CCSDT/aC{T,Q}Z'   : { 'A' : '[ae] CCSDT/aC{T,Q}Z',    'B' : '[fc] CCSDT/aC{T,Q}Z' },
        '[cv] CCSDT/aCTZ'       : { 'A' : 'T / aCTZ',               'B' : '[fc] T / aCTZ' },
        '[cv] CCSDT(Q)L/aCTZ'   : { 'A' : '(Q)_L / aCTZ',           'B' : '[fc] (Q)_L / aCTZ' }
    })

    # Scalar Relativistic correction data
    heat = minus(heat, {
        'SREL SCF/uaCQZ'        : {'A' : 'SF SCF / uaCQZ',          'B' : 'NR SCF / uaCQZ'},
        'SREL CCSD/uaC{T,Q}Z'   : {'A' : 'SF CCSD/uaC{T,Q}Z',       'B' : 'NR CCSD/uaC{T,Q}Z'}, 
        'SREL CCSD(T)/uaC{T,Q}Z'   : {'A' : 'SF CCSD(T)/uaC{T,Q}Z', 'B' : 'NR CCSD(T)/uaC{T,Q}Z'} 
    })

    # DBOC correction data
    heat = minus(heat, {
        'DBOC [ae] CCSD-SCF/aCTZ'   : { 'A' : 'DBOC D / aCTZ',      'B' : 'DBOC SCF / aCTZ'},
        'DBOC [fc] T-D/TZ'          : { 'A' : '[fc] DBOC T / TZ',   'B' : '[fc] DBOC D / TZ'},
        'DBOC [fc] Q-T/DZ'          : { 'A' : '[fc] DBOC Q / DZ',   'B' : '[fc] DBOC T / DZ'}
    })

    # Correlation correction data
    heat = minus(heat, {
        '[fc] (T)-D/aC{5,6}Z'   : { 'A' : '[fc] CCSD(T)/aC{5,6}Z',  'B' : '[fc] CCSD/aC{5,6}Z' }, 
        '[cv] (T)-D/aC{5,6}Z'   : { 'A' : '[cv] CCSD(T)/aC{5,6}Z',  'B' : '[cv] CCSD/aC{5,6}Z' }, 
        '[fc] T-(T)/{5,6}Z'     : { 'A' : '[fc] CCSDT/{5,6}Z',      'B' : '[fc] CCSD(T)/{5,6}Z' }, 
        '[cv] T-(T)/aC{T,Q}Z'   : { 'A' : '[cv] CCSDT/aC{T,Q}Z',    'B' : '[cv] CCSD(T)/aC{T,Q}Z' },
        '[fc] (Q)L-T/{Q,5}Z'    : { 'A' : '[fc] CCSDT(Q)L/{Q,5}Z',  'B' : '[fc] CCSDT/{Q,5}Z'},
        '[cv] (Q)L-T/aCTZ'      : { 'A' : '[cv] CCSDT(Q)L/aCTZ',    'B' : '[cv] CCSDT/aCTZ'},
        '[fc] Q-(Q)L/TZ'        : { 'A' : '[fc] Q / TZ',            'B' : '[fc] (Q)_L / TZ'},
        '[fc] (P)L-Q/DZ'        : { 'A' : '[fc] (P)_L / DZ',        'B' : '[fc] Q / DZ'},
        'SREL (T)-D/uaC{T,Q}Z'  : { 'A' : 'SREL CCSD(T)/uaC{T,Q}Z', 'B' : 'SREL CCSD/uaC{T,Q}Z'}
    })


    # Form total energies and recipe list
    recipe_list = [
        'SCF/aC6Z',
        '[fc] CCSD/aC{6,7}Z', '[cv] CCSD/aC{5,6}Z',
        '[fc] (T)-D/aC{5,6}Z', '[cv] (T)-D/aC{5,6}Z',
        '[fc] T-(T)/{5,6}Z', '[cv] T-(T)/aC{T,Q}Z', 
        '[fc] (Q)L-T/{Q,5}Z', '[cv] (Q)L-T/aCTZ',
        '[fc] Q-(Q)L/TZ',
        '[fc] (P)L-Q/DZ',
        'SREL SCF/uaCQZ', 'SREL CCSD/uaC{T,Q}Z', 'SREL (T)-D/uaC{T,Q}Z',
        'DBOC SCF / aCTZ', 'DBOC [ae] CCSD-SCF/aCTZ', 'DBOC [fc] T-D/TZ', 'DBOC [fc] Q-T/DZ',
        'SO (Hill Van Vleck/Hougen)',
        "PETER Anharmonic" 
    ]

    heat['Total'] = sum(heat[item] for item in recipe_list)

    #Write to superHEAT csv
    heat.to_csv('superHEAT_raw.csv')

    # append total to the recipe list for the reaction analysis 
    recipe_list.append('Total')

    tae_data = reaction_data(heat, heat_tae, recipe_list, conversion = au2cm)
    anl_data = reaction_data(heat, heat_anl, recipe_list, conversion = au2cm)
    bde_data = reaction_data(heat, heat_bde, recipe_list, conversion = au2cm)
    all_data = reaction_data(heat, heat_all, recipe_list, conversion = au2cm)

    # Last step, add ATcT values for reactions
    tae_data = add_atct(tae_data, heat_tae, conversion = kJ2cm)
    anl_data = add_atct(anl_data, heat_anl, conversion = kJ2cm)
    bde_data = add_atct(bde_data, heat_bde, conversion = kJ2cm)
    all_data = add_atct(all_data, heat_all, conversion = kJ2cm)

    # Now we can do statistical analysis
    tae_data["Err"] = tae_data["Total"] - tae_data["ATcT Values"]
    anl_data["Err"] = anl_data["Total"] - anl_data["ATcT Values"]
    bde_data["Err"] = bde_data["Total"] - bde_data["ATcT Values"]
    all_data["Err"] = all_data["Total"] - all_data["ATcT Values"]

    # Absoulte value of error
    tae_data["|Err|"] = np.abs(tae_data["Err"])
    anl_data["|Err|"] = np.abs(anl_data["Err"])
    bde_data["|Err|"] = np.abs(bde_data["Err"])
    all_data["|Err|"] = np.abs(all_data["Err"])

    #write to csv files
    tae_data.to_csv('superHEAT_TAE.csv')
    anl_data.to_csv('superHEAT_ANL.csv')
    bde_data.to_csv('superHEAT_BDE.csv')
    all_data.to_csv('superHEAT_ALL.csv')

    print("TAE data\n", tae_data)
    print(f"TAE Mean error : {tae_data["Err"].mean()}")
    print(f"TAE Std.Dev. error : {tae_data["Err"].std(ddof=1)}")
    print(f"TAE MAE :, {tae_data["|Err|"].mean()}")
    print(f"TAE 2*sigma : {2*l2d(tae_data["Err"])}")
    print("")
    print("ANL data\n", anl_data)
    print(f"ANL Mean error : {anl_data["Err"].mean()}")
    print(f"ANL Std.Dev. : {anl_data["Err"].std(ddof=1)}")
    print(f"ANL MAE :, {anl_data["|Err|"].mean()}")
    print(f"ANL 2*sigma : {2*l2d(anl_data["Err"])}")
    print("")
    print("BDE data\n", bde_data)
    print(f"BDE Mean error : {bde_data["Err"].mean()}")
    print(f"BDE Std.Dev.: {bde_data["Err"].std(ddof=1)}")
    print(f"BDE MAE :, {bde_data["|Err|"].mean()}")
    print(f"BDE 2*sigma : {2*l2d(bde_data["Err"])}")
    print("")
    print("ALL data\n", all_data)
    print(f"ALL Mean error : {all_data["Err"].mean()}")
    print(f"ALL Std.Dev. : {all_data["Err"].std(ddof=1)}")
    print(f"ALL MAE :, {all_data["|Err|"].mean()}")
    print(f"ALL 2*sigma : {2*l2d(all_data["Err"])}")


