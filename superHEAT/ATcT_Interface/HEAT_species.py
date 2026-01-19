# HEAT_species
#
# Contains information about the species in the HEAT database

from species import Elements, Species

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
