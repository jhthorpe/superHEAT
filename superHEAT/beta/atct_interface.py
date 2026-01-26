# atct_interface.py
# 
#   JHT, September 18, 2025 @ ANL. Created
#
# Tests how to get reactions and/or atomization energies for species in the HEAT suite 
"""Testing how to use the ATcT pythonic API to gather reaction data used in comp. thermo"""

import asyncio
import os
import time
import copy
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
from HEAT_species import heat_species, heat_bde
from reaction import Reaction

# Converts kJ/mol to wavenumbers (inverse centimeters)
kJ2cm = 83.59347229110210

async def main():

    # 1. Health check
    print("1. Health Check:")
    if await healthcheck():
        print("   ✅ API is healthy")
    else:
        print("   ❌ API is not responding")
        return
    print()

    ###################################################################################
    #
    # Generate general recovery tasks
    #
    print("Generating Species Recovery Tasks")

    species_tasks = {}
    for spec, data in heat_species.items():
        species_tasks[spec] = {'atct_data' : get_species(data.atct_id, expand_xyz=True)}

    print("Waiting on ATcT recovery data")
    species_atct = {}
    for spec, res in species_tasks.items():

        species_atct[spec] = await asyncio.gather(*res.values(), return_exceptions=True)

        #David trick to map species name to results data 
        species_atct[spec] = dict(zip(res.keys(), species_atct[spec]))

        #Now rip the DfH (0 K) from data
        heat_species[spec].dfh0k = species_atct[spec]['atct_data'].delta_h_0k

    print("ATcT Species Info")
    for spec, data in heat_species.items():
        print(f"{spec} : {data.dfh0k} kJ/mol")

    ###################################################################################
    # 
    # Generate TAE tasks
    #

    tae_refs = {'H' :'H', 'C':'C', 'N':'N', 'O':'O', 'F':'F'}
    tae_species = {key:None for key in heat_species} 
    for atom,ref in tae_refs.items():
        tae_species.pop(ref)

    print("Generating TAE tasks")
    tae_tasks = {}
    tae_rxns = {}
    for spec in tae_species:

        species = heat_species[spec]
        rxn = Reaction(name = spec)

        rxn.stoich[spec] = -1
        for atom,num in species.elements.items():
            rxn.stoich[atom] = num

        tae_rxns[spec] = rxn
        tae_tasks[spec] = rxn.atct_0K_query(heat_species)

    print("Processing TAE tasks")
    tae_res = {}
    for spec, task in tae_tasks.items():
        tae_res[spec] = await asyncio.gather(task['covariance_298K'], task['conventional_0K'], return_exceptions=True)
        tae_rxns[spec].value = tae_res[spec][1].delta_h
        tae_rxns[spec].unc = tae_res[spec][0].uncertainty

    for name, rxn in tae_rxns.items():
        print(f"TAE of {name:4} : {rxn.value * kJ2cm:>12.3f} +- {rxn.unc * kJ2cm:>.6f}")


    ###################################################################################
    # 
    # Generate ANL tasks
    #

    anl_ref = {'H' : 'H2', 'C' : 'CH4', 'N' : 'NH3', 'O': 'H2O', 'F' : 'HF'}
    anl_species = {key:None for key in heat_species}
    for atom,ref in anl_ref.items():
        anl_species.pop(ref)

    print("Generating ANL Tasks")
    anl_tasks = {}
    anl_rxns = {}
    for spec in anl_species:
       
        species = heat_species[spec]

        rxn = Reaction(name = spec, stoich = {spec : -1})
        numh = species.elements.count('H') 

        for atom, num in species.elements.items():
            ref = heat_species[anl_ref[atom]]
            rxn.stoich[anl_ref[atom]] = num * ref.elements.count(atom)
            numh += num * ref.elements.count('H')
        if (abs(numh) > 1e-14):
            rxn.stoich['H2'] = rxn.stoich['H2'] - numh * 0.5

        rxn.value = None
        rxn.unc = None

        anl_rxns[spec] = rxn
        anl_tasks[spec] = rxn.atct_0K_query(heat_species)

    print("Processing ANL tasks")
    anl_res = {}
    for spec, task in anl_tasks.items():
        anl_res[spec] = await asyncio.gather(task['covariance_298K'], task['conventional_0K'], return_exceptions=True)
        anl_rxns[spec].value = anl_res[spec][1].delta_h
        anl_rxns[spec].unc = anl_res[spec][0].uncertainty

    for name, rxn in anl_rxns.items():
        print(f"ANL Rxn of {name:4} : {rxn.value * kJ2cm:>12.3f} +- {rxn.unc * kJ2cm:>.6f}")

    
    ###################################################################################
    #
    # Stepwise BDE Tasks 
    #
    print("Generating BDE Tasks")
    bde_tasks = {}
    for name, rxn in heat_bde.items():
        bde_tasks[name] = rxn.atct_0K_query(heat_species)        

    print("Processing BDE Tasks")
    rxn_atct = {}
    for name, task in bde_tasks.items():
        rxn_atct[name] = await asyncio.gather(task['covariance_298K'], task['conventional_0K'], return_exceptions=True)

    for name, task in bde_tasks.items():
        heat_bde[name].value = rxn_atct[name][1].delta_h
        heat_bde[name].unc = rxn_atct[name][0].uncertainty

    for name,rxn in heat_bde.items():
        print(f"{name:18} : {rxn.value * kJ2cm:>12.3f} +- {rxn.unc * kJ2cm:>.6f}")

########################################################################################
#
# fill provided reactions from a Reactions Dictionary
#
async def fill_reactions(reactions):

    rxns = reactions
    
    # 1. Health check
    print("1. Health Check:")
    if await healthcheck():
        print("   ✅ API is healthy")
    else:
        print("   ❌ API is not responding")
        return
    print()

    rxn_tasks = {}
    for name, rxn in reactions.items():
        rxn_tasks[name] = rxn.atct_0K_query(heat_species)        

    print("Processing ATcT Reaction Tasks")
    rxn_atct = {}
    for name, task in rxn_tasks.items():
        rxn_atct[name] = await asyncio.gather(task['covariance_298K'], task['conventional_0K'], return_exceptions=True)

    for name, task in rxn_tasks.items():
        rxns[name].value = rxn_atct[name][1].delta_h
        rxns[name].unc = rxn_atct[name][0].uncertainty

    #option print at end, probably remove
    #for name, rxn in rxns.items():
    #    print(f"{name:18} : {rxn.value * kJ2cm:>12.3f} +- {rxn.unc * kJ2cm:>.6f}")

    return rxns

########################################################################################
# 
# MAIN
if __name__== "__main__":
    asyncio.run(main())

