import species
from HEAT_species import HEAT_Species

CH4 = species.Species(name = 'CH4', atctid = '111', elements=species.Elements({'H':4, 'C':1}), dfh0k = 100)

for key,val in HEAT_Species.items():
    print(f"Species : {key}\n{val}")


