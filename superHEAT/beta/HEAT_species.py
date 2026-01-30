# HEAT_species
#
# Contains information about the species and reactions 
# in the HEAT database

from species import Elements, Species
from reaction import Reaction

##########################################################################################
#
# HEAT species
#
heat_species = {
    'H' : Species(
		name = 'H',
        atct_id =  '12385-13-6*0',
        elements = Elements({
            'H' : 1,
            'C' : 0,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'C' : Species(
		name = 'C',
        atct_id =  '7440-44-0*0',
        elements = Elements({
            'H' : 0,
            'C' : 1,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'N' : Species(
		name = 'N',
        atct_id =  '17778-88-0*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 1,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'O' : Species(
		name = 'O',
        atct_id =  '17778-80-2*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 0,
            'O' : 1,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'F' : Species(
		name = 'F',
        atct_id =  '14762-94-8*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 0,
            'O' : 0,
            'F' : 1
        }),
        dfh0k =  None
    ),

    'N2' : Species(
		name = 'N2',
        atct_id =  '7727-37-9*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 2,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'H2' : Species(
		name = 'H2',
        atct_id =  '1333-74-0*0',
        elements = Elements({
            'H' : 2,
            'C' : 0,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'F2' : Species(
		name = 'F2',
        atct_id =  '7782-41-4*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 0,
            'O' : 0,
            'F' : 2
        }),
        dfh0k =  None
    ),

    'O2' : Species(
		name = 'O2',
        atct_id =  '7782-44-7*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 0,
            'O' : 2,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CO' : Species(
		name = 'CO',
        atct_id =  '630-08-0*0',
        elements = Elements({
            'H' : 0,
            'C' : 1,
            'N' : 0,
            'O' : 1,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'HCCH' : Species(
		name = 'HCCH',
        atct_id =  '74-86-2*0',
        elements = Elements({
            'H' : 2,
            'C' : 2,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CCH' : Species(
		name = 'CCH',
        atct_id =  '2122-48-7*0',
        elements = Elements({
            'H' : 1,
            'C' : 2,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CH2' : Species(
		name = 'CH2',
        atct_id =  '2465-56-7*1',
        elements = Elements({
            'H' : 2,
            'C' : 1,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CH' : Species(
		name = 'CH',
        atct_id =  '3315-37-5*0',
        elements = Elements({
            'H' : 1,
            'C' : 1,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CH3' : Species(
		name = 'CH3',
        atct_id =  '2229-07-4*0',
        elements = Elements({
            'H' : 3,
            'C' : 1,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CO2' : Species(
		name = 'CO2',
        atct_id =  '124-38-9*0',
        elements = Elements({
            'H' : 0,
            'C' : 1,
            'N' : 0,
            'O' : 2,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'HOOH' : Species(
		name = 'HOOH',
        atct_id =  '7722-84-1*0',
        elements = Elements({
            'H' : 2,
            'C' : 0,
            'N' : 0,
            'O' : 2,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'H2O' : Species(
		name = 'H2O',
        atct_id =  '7732-18-5*0',
        elements = Elements({
            'H' : 2,
            'C' : 0,
            'N' : 0,
            'O' : 1,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'HCO' : Species(
		name = 'HCO',
        atct_id =  '2597-44-6*0',
        elements = Elements({
            'H' : 1,
            'C' : 1,
            'N' : 0,
            'O' : 1,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'HF' : Species(
		name = 'HF',
        atct_id =  '7664-39-3*0',
        elements = Elements({
            'H' : 1,
            'C' : 0,
            'N' : 0,
            'O' : 0,
            'F' : 1
        }),
        dfh0k =  None
    ),

    'HO2' : Species(
		name = 'HO2',
        atct_id =  '3170-83-0*0',
        elements = Elements({
            'H' : 1,
            'C' : 0,
            'N' : 0,
            'O' : 2,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'NO' : Species(
		name = 'NO',
        atct_id =  '10102-43-9*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 1,
            'O' : 1,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'OH' : Species(
		name = 'OH',
        atct_id =  '3352-57-6*0',
        elements = Elements({
            'H' : 1,
            'C' : 0,
            'N' : 0,
            'O' : 1,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'HNO' : Species(
		name = 'HNO',
        atct_id =  '14332-28-6*0',
        elements = Elements({
            'H' : 1,
            'C' : 0,
            'N' : 1,
            'O' : 1,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CN' : Species(
		name = 'CN',
        atct_id =  '2074-87-5*0',
        elements = Elements({
            'H' : 0,
            'C' : 1,
            'N' : 1,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'HCN' : Species(
		name = 'HCN',
        atct_id =  '74-90-8*0',
        elements = Elements({
            'H' : 1,
            'C' : 1,
            'N' : 1,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'CF' : Species(
		name = 'CF',
        atct_id =  '3889-75-6*0',
        elements = Elements({
            'H' : 0,
            'C' : 1,
            'N' : 0,
            'O' : 0,
            'F' : 1
        }),
        dfh0k =  None
    ),

    'NH2' : Species(
		name = 'NH2',
        atct_id =  '13770-40-6*0',
        elements = Elements({
            'H' : 2,
            'C' : 0,
            'N' : 1,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'NH3' : Species(
		name = 'NH3',
        atct_id =  '7664-41-7*0',
        elements = Elements({
            'H' : 3,
            'C' : 0,
            'N' : 1,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'NH' : Species(
		name = 'NH',
        atct_id =  '13774-92-0*0',
        elements = Elements({
            'H' : 1,
            'C' : 0,
            'N' : 1,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    ),

    'OF' : Species(
		name = 'OF',
        atct_id =  '12061-70-0*0',
        elements = Elements({
            'H' : 0,
            'C' : 0,
            'N' : 0,
            'O' : 1,
            'F' : 1
        }),
        dfh0k =  None
    ),

    'CH4' : Species(
		name = 'CH4',
        atct_id =  '74-82-8*0',
        elements = Elements({
            'H' : 4,
            'C' : 1,
            'N' : 0,
            'O' : 0,
            'F' : 0
        }),
        dfh0k =  None
    )
}

##########################################################################################
# 
# HEAT TAE reactions
#
tae_refs = {'H' :'H', 'C':'C', 'N':'N', 'O':'O', 'F':'F'}

tae_species = {key:None for key in heat_species}

for atom, ref in tae_refs.items():
    tae_species.pop(ref)

heat_tae = {}
for spec in tae_species:
    species = heat_species[spec]

    rxn = Reaction(name = f"{species.name}")
    rxn.stoich[spec] = -1

    for atom, num in species.elements.items():
        rxn.stoich[atom] = num

    heat_tae[rxn.rxn_str()] = rxn 
#    heat_tae[rxn.name] = rxn 

##########################################################################################
# 
# HEAT ANL reactions
#
anl_ref = {'H' : 'H2', 'C' : 'CH4', 'N' : 'NH3', 'O': 'H2O', 'F' : 'HF'}
anl_species = {key:None for key in heat_species}
for atom, ref in anl_ref.items():
    anl_species.pop(ref)

heat_anl = {}
for spec in anl_species:
    species = heat_species[spec]

    rxn = Reaction(name = species.name, stoich = {spec : -1})
    numh = species.elements.count('H')

    for atom, num in species.elements.items():
        ref = heat_species[anl_ref[atom]]
        rxn.stoich[anl_ref[atom]] = num * ref.elements.count(atom)
        numh += num * ref.elements.count('H')

    if (abs(numh) > 1e-14):
	    rxn.stoich['H2'] = rxn.stoich['H2'] - numh * 0.5

    rxn.value = None
    rxn.unc = None

    heat_anl[rxn.rxn_str()] = rxn



##########################################################################################
#
# HEAT sequential bond dissociation energies
#
heat_bde = {
        'H2 -> 2 H'         : Reaction(stoich = {'H2'   : -1,  'H'   : 2           }),
        'CH -> H + C'       : Reaction(stoich = {'CH'   : -1,  'C'   : 1,  'H' : 1 }),
        'CH2 -> CH + H'     : Reaction(stoich = {'CH2'  : -1,  'CH'  : 1,  'H' : 1 }),
        'CH3 -> CH2 + H'    : Reaction(stoich = {'CH3'  : -1,  'CH2' : 1,  'H' : 1 }),
        'CH4 -> CH3 + H'    : Reaction(stoich = {'CH4'  : -1,  'CH3' : 1,  'H' : 1 }),
        'HCCH -> 2 CH'      : Reaction(stoich = {'HCCH' : -1,  'CH'  : 2           }),
        'HCCH -> CCH + H'   : Reaction(stoich = {'HCCH' : -1,  'CCH' : 1,  'H' : 1 }),
        'CCH -> CH + C'     : Reaction(stoich = {'CCH'  : -1,  'CH'  : 1,  'C' : 1 }),
        'CF -> C + F'       : Reaction(stoich = {'CF'   : -1,  'C'   : 1,  'F' : 1 }),
        'F2 -> 2 F'         : Reaction(stoich = {'F2'   : -1,  'F'   : 2           }),
        'HF -> H + F'       : Reaction(stoich = {'HF'   : -1,  'H'   : 1,  'F' : 1 }),
        'CO2 -> CO + O'     : Reaction(stoich = {'CO2'  : -1,  'CO'  : 1,  'O' : 1 }),
        'CO -> C + O'       : Reaction(stoich = {'CO'   : -1,  'C'   : 1,  'O' : 1 }),
        'HCO -> CO + H'     : Reaction(stoich = {'HCO'  : -1,  'CO'  : 1,  'H' : 1 }),
        'HCO -> CH + O'     : Reaction(stoich = {'HCO'  : -1,  'CH'  : 1,  'O' : 1 }),
        'OF -> O + F'       : Reaction(stoich = {'OF'   : -1,  'O'   : 1,  'F' : 1 }),
        'O2 -> 2 O'         : Reaction(stoich = {'O2'   : -1,  'O'   : 2           }),
        'HO2 -> O2 + H'     : Reaction(stoich = {'HO2'  : -1,  'O2'  : 1,  'H' : 1 }),
        'HO2 -> OH + O'     : Reaction(stoich = {'HO2'  : -1,  'OH'  : 1,  'O' : 1 }),
        'HOOH -> HO2 + H'   : Reaction(stoich = {'HOOH' : -1,  'HO2' : 1,  'H' : 1 }),
        'HOOH -> HO2 + H'   : Reaction(stoich = {'HOOH' : -1,  'HO2' : 1,  'H' : 1 }),
        'HOOH -> 2 OH'      : Reaction(stoich = {'HOOH' : -1,  'OH'  : 2           }),
        'H2O -> OH + H'     : Reaction(stoich = {'H2O'  : -1,  'OH'  : 1,  'H' : 1 }),
        'OH -> O + H'       : Reaction(stoich = {'OH'   : -1,  'O'   : 1,  'H' : 1 }),
        'HNO -> NO + H'     : Reaction(stoich = {'HNO'  : -1,  'NO'  : 1,  'H' : 1 }),
        'NO -> N + O'       : Reaction(stoich = {'NO'   : -1,  'N'   : 1,  'O' : 1 }),
        'HNO -> NH + O'     : Reaction(stoich = {'HNO'  : -1,  'NH'  : 1,  'O' : 1 }),
        'NH -> H + N'       : Reaction(stoich = {'NH'   : -1,  'N'   : 1,  'H' : 1 }),
        'NH3 -> NH2 + H'    : Reaction(stoich = {'NH3'  : -1,  'NH2' : 1,  'H' : 1 }),
        'NH2 -> NH + H'     : Reaction(stoich = {'NH2'  : -1,  'NH'  : 1,  'H' : 1 }),
        'N2 -> 2 N'         : Reaction(stoich = {'N2'   : -1,  'N'   : 2           }),
        'HCN -> CH + N'     : Reaction(stoich = {'HCN'  : -1,  'CH'  : 1,  'N' : 1 }),
        'HCN -> CN + H'     : Reaction(stoich = {'HCN'  : -1,  'NH'  : 1,  'C' : 1 }),
        'CN -> C + N'       : Reaction(stoich = {'CN'   : -1,  'C'   : 1,  'N' : 1 })
}
