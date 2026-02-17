'''
    unc.py
    Generates data needed for uncertainty estimations for the superHEAT testsets. This also 
    generates the following datasets:

        NREE    : semi-empirical non-relativistic electronic-energy components
        CCSD    : semi-empirical valence-only CCSD basis-set limits
        ZPE     : semi-empirical zero-point energies 

'''

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":

    # Read in tests
    tests = {"TAE" : pd.read_csv("superHEAT_TAE.csv"),
             "ANL" : pd.read_csv("superHEAT_ANL.csv"),
             "BDE" : pd.read_csv("superHEAT_BDE.csv")
    }

    uncs = {}

    for name, test in tests.items():
        tests[name] = test.set_index("Reaction")
        uncs[name] = tests[name][["ATcT Values", "ATcT Unc", 'Total', 'Err', '|Err|']].copy(deep=True)

    #####################################################################
    #
    # add varieties for uncertainty estimation 
    #
    for name in tests:
        test = tests[name]
        unc = uncs[name]

        # SCF BSIE
        test['SCF/CBS'] = test["SCF/aC6Z"]
        test['SCF/CBS-1'] = test["SCF/aC5Z"]

        # CCSD BSIE
        test['CCSD/CBS'] = test["[fc] CCSD/aC{6,7}Z"] + test["[cv] CCSD/aC{5,6}Z"]
        test['CCSD/CBS-1'] = test["[fc] CCSD/aC{5,6}Z"] + test["[cv] CCSD/aC{Q,5}Z"]
        test['CCSD/CBS alt'] = test["[fc] CCSD/aC{6,7}Z : Helgaker"] + test["[cv] CCSD/aC{5,6}Z : Helgaker"]

        # (T) - D BSIE
        test['(T)-D/CBS'] = test["[fc] (T)-D/aC{5,6}Z"] + test["[cv] (T)-D/aC{5,6}Z"]
        test['(T)-D/CBS-1'] = test["[fc] (T)-D/aC{Q,5}Z"] + test["[cv] (T)-D/aC{Q,5}Z"]
        test['(T)-D/CBS alt'] = test["[fc] (T)-D/aC{5,6}Z : Helgaker"] + test["[cv] (T)-D/aC{5,6}Z : Helgaker"]

        # (Q)L - (T) BSIE
        test['(Q)L-(T)/CBS'] = test['[fc] (Q)L-(T)/CBS'] + test['[cv] (Q)L-(T)/CBS'] 
        test['(Q)L-(T)/CBS-1'] = test['[fc] T-(T)/{Q,5}Z'] + test['[fc] (Q)L-T/{Q,5}Z'] + test['[cv] T-(T)/aCQZ'] 

        # (P)L - (Q)L BSIE
        test['(P)L-(Q)L/CBS'] = test['[fc] (P)L-Q/DZ'] + test['[fc] Q-(Q)L/TZ'] 
        test['(P)L-(Q)L/CBS-1'] = test['[fc] (P)L-Q/DZ'] + test['[fc] Q-(Q)L/DZ'] 

        # SREL BSIE 
        test['SREL SCF/CBS'] = test['SREL SCF/uaCQZ'] 
        test['SREL SCF/CBS-1'] = test['SREL SCF/uaCTZ'] 

        test['SREL CCSD/CBS'] = test['SREL CCSD/uaC{T,Q}Z']
        test['SREL CCSD/CBS-1'] = test['SREL CCSD/uaCQZ'] 
        test['SREL CCSD/CBS alt'] = test['SREL CCSD/uaC{T,Q}Z : Helgaker']

        test['SREL (T)-D/CBS'] = test['SREL (T)-D/uaC{T,Q}Z']
        test['SREL (T)-D/CBS-1'] = test['SREL (T)-D/uaCQZ']
        test['SREL (T)-D/CBS alt'] = test['SREL (T)-D/uaC{T,Q}Z : Helgaker']

        test['SREL CBS'] = test['SREL SCF/CBS'] + test['SREL CCSD/CBS'] + test['SREL (T)-D/CBS']

        # DBOC
        test['DBOC CBS'] = test['DBOC SCF / aCTZ'] + test['DBOC [ae] CCSD-SCF/aCTZ'] + test['DBOC [fc] T-D/TZ'] + test['DBOC [fc] Q-T/DZ'] 

        # Spin Orbit
        test['SO'] = test['SO (Hill Van Vleck/Hougen)']

    #####################################################################
    #
    # Generate uncertainties
    #
    for name, test in tests.items():
        unc = uncs[name]

        # SCF
        unc['SCF BSIE'] = np.abs(test["SCF/CBS"] - test["SCF/CBS-1"])

        # CCSD
        unc['CCSD zeta'] = np.abs(test['CCSD/CBS'] - test['CCSD/CBS-1'])
        unc['CCSD extrap'] = np.abs(test['CCSD/CBS'] - test['CCSD/CBS alt'])
        unc['CCSD BSIE'] = np.maximum(np.abs(test['CCSD/CBS'] - test['CCSD/CBS alt']), 
                                      np.abs(test['CCSD/CBS'] - test['CCSD/CBS-1']))
        # (T) - D 
        unc['(T)-D zeta'] = np.abs(test['(T)-D/CBS'] - test['(T)-D/CBS-1'])
        unc['(T)-D extrap'] = np.abs(test['(T)-D/CBS'] - test['(T)-D/CBS alt'])
        unc['(T)-D BSIE'] = np.maximum(np.abs(test['(T)-D/CBS'] - test['(T)-D/CBS alt']), 
                                      np.abs(test['(T)-D/CBS'] - test['(T)-D/CBS-1']))

        # (Q)L - (T) : note that difference between extrapolation is effectively zero, here
        unc['(Q)L-(T) BSIE'] = np.abs(test['(Q)L-(T)/CBS'] - test['(Q)L-(T)/CBS-1'])

        # (P)L - (Q)L
        unc['(P)L-(Q)L BSIE'] = np.abs(test['(P)L-(Q)L/CBS'] - test['(P)L-(Q)L/CBS-1'])

        # HLC this is just a best estimate, we can't really do much here
        unc['Post-(P)L HLC'] = 0.1 * np.abs(test['(P)L-(Q)L/CBS'])

        # SREL BSIE
        unc['SREL SCF BSIE'] = np.abs(test['SREL SCF/CBS'] - test['SREL SCF/CBS-1'] )

        unc['SREL CCSD zeta'] = np.abs(test['SREL CCSD/CBS'] - test['SREL CCSD/CBS-1'])
        unc['SREL CCSD extrap'] = np.abs(test['SREL CCSD/CBS'] - test['SREL CCSD/CBS alt'])
        unc['SREL CCSD BSIE'] = np.maximum(np.abs(test['SREL CCSD/CBS'] - test['SREL CCSD/CBS-1']),
                                           np.abs(test['SREL CCSD/CBS'] - test['SREL CCSD/CBS alt']))

        unc['SREL (T)-D zeta'] = np.abs(test['SREL (T)-D/CBS'] - test['SREL (T)-D/CBS-1'])
        unc['SREL (T)-D extrap'] = np.abs(test['SREL (T)-D/CBS'] - test['SREL (T)-D/CBS alt'])
        unc['SREL (T)-D BSIE'] = np.maximum(np.abs(test['SREL (T)-D/CBS'] - test['SREL (T)-D/CBS-1']),
                                           np.abs(test['SREL (T)-D/CBS'] - test['SREL (T)-D/CBS alt']))

        #HLC est. Again, rough estimate, not much more we can do here
        unc['SREL HLC est'] = 0.25 * np.abs(test['SREL (T)-D/CBS'])
        
        # DBOC this seems like it has very very nearly zero error
        unc['DBOC unc est'] = 1.

        # Spin Orbit. Again, rough estimate, nothing we can do 
        unc['2nd Order SO est'] = 0.1 * np.abs(test['SO (Hill Van Vleck/Hougen)'])

        # Peter Uncertainty
        unc['ZPE Harmonic'] = np.abs(test['ZPE Harmonic Best'] - test['ZPE Harmonic Second best'])
        unc['ZPE Anarmonic'] = np.abs(test['ZPE Anharm Best'] - test['ZPE Anharm Second Best'])

    #####################################################################
    #
    # Total uncertainty estimates 
    #
    # These are not great, this is very rough
    #
    for name in uncs:
        unc = uncs[name]
        test = tests[name]

        # Total uncertainty
        unc['Total Unc'] = np.sqrt(unc['SCF BSIE']**2 + unc['CCSD BSIE']**2 + unc['(T)-D BSIE']**2 + unc['(Q)L-(T) BSIE']**2 + unc['(P)L-(Q)L BSIE']**2 + unc['Post-(P)L HLC']**2 + unc['SREL SCF BSIE']**2 + unc['SREL CCSD BSIE']**2 + unc['SREL (T)-D BSIE']**2 + unc['SREL HLC est']**2 + unc['DBOC unc est']**2 + unc['2nd Order SO est']**2 + unc['ZPE Harmonic']**2 + unc['ZPE Anarmonic']**2)

#      Checking totals have been calcualted correctly (they have)
#        unc['Test total'] = test['SCF/CBS'] + test['CCSD/CBS'] + test['(T)-D/CBS'] + test['(Q)L-(T)/CBS'] + test['(P)L-(Q)L/CBS'] + test['SREL SCF/CBS'] + test['SREL CCSD/CBS'] + test['SREL (T)-D/CBS'] + test['DBOC CBS'] + test['ZPE Best'] + test['SO'] 
#        unc['Test total err'] = unc['Total'] - unc['Test total']

    #####################################################################
    #
    # NREE estimates
    #
    for name in uncs:
        unc = uncs[name]
        test = tests[name]

        test['Semiempirical NREE'] = test['ATcT Values'] - test['SO'] - test['ZPE Best'] - test['DBOC CBS'] - test['SREL CBS']
        test['Semiempirical NREE unc'] = np.sqrt(unc['ATcT Unc']**2 + unc['2nd Order SO est']**2 + unc['DBOC unc est']**2 +  unc['SREL SCF BSIE']**2 + unc['SREL CCSD BSIE']**2 + unc['SREL (T)-D BSIE']**2 + unc['ZPE Harmonic']**2 + unc['ZPE Anarmonic']**2)
        test['Semiempirical NREE unc (no SO unc)'] = np.sqrt(unc['ATcT Unc']**2 + unc['DBOC unc est']**2 +  unc['SREL SCF BSIE']**2 + unc['SREL CCSD BSIE']**2 + unc['SREL (T)-D BSIE']**2 + unc['ZPE Harmonic']**2 + unc['ZPE Anarmonic']**2)

        test[['Semiempirical NREE', 'Semiempirical NREE unc', 'Semiempirical NREE unc (no SO unc)']].to_csv(f"nree_{name}.csv")

    #####################################################################
    #
    # Valence CCSD estimates
    #
    for name in uncs:
        unc = uncs[name]
        test = tests[name]

        test['Semiempirical [fc] CCSD'] = test['ATcT Values'] - test['SO'] - test['ZPE Best'] - test['DBOC CBS'] - test['SREL CBS'] - test['SCF/CBS'] - test['(T)-D/CBS'] - test['(Q)L-(T)/CBS'] - test['(P)L-(Q)L/CBS'] - test['[cv] CCSD/aC{5,6}Z']

        unc['[cv] CCSD/CBS'] = np.maximum(np.abs(test["[cv] CCSD/aC{5,6}Z"] - test["[cv] CCSD/aC{Q,5}Z"]), 
                                          np.abs(test["[cv] CCSD/aC{5,6}Z"] - test["[cv] CCSD/aC{5,6}Z : Helgaker"]))
        test['Semiempirical [fc] CCSD unc.'] = np.sqrt(unc['SCF BSIE']**2 + unc['[cv] CCSD/CBS']**2 +  unc['(T)-D BSIE']**2 + unc['(Q)L-(T) BSIE']**2 + unc['(P)L-(Q)L BSIE']**2 + unc['Post-(P)L HLC']**2 + unc['SREL SCF BSIE']**2 + unc['SREL CCSD BSIE']**2 + unc['SREL (T)-D BSIE']**2 + unc['SREL HLC est']**2 + unc['DBOC unc est']**2 + unc['2nd Order SO est']**2 + unc['ZPE Harmonic']**2 + unc['ZPE Anarmonic']**2)

        test['Semiempirical [fc] CCSD unc. (no SO unc)'] = np.sqrt(unc['SCF BSIE']**2 + unc['[cv] CCSD/CBS']**2 + unc['(T)-D BSIE']**2 + unc['(Q)L-(T) BSIE']**2 + unc['(P)L-(Q)L BSIE']**2 + unc['Post-(P)L HLC']**2 + unc['SREL SCF BSIE']**2 + unc['SREL CCSD BSIE']**2 + unc['SREL (T)-D BSIE']**2 + unc['SREL HLC est']**2 + unc['DBOC unc est']**2 + unc['ZPE Harmonic']**2 + unc['ZPE Anarmonic']**2)
         
        test[['Semiempirical [fc] CCSD', 'Semiempirical [fc] CCSD unc.', 'Semiempirical [fc] CCSD unc. (no SO unc)']].to_csv(f'ccsd_{name}.csv')

    #####################################################################
    #
    # ZPE estimates
    #
    for name in uncs:
        unc = uncs[name]
        test = tests[name]

        test['Semiempirical ZPE'] = test['ATcT Values'] - test['SO'] - test['DBOC CBS'] - test['SREL CBS'] - test['SCF/CBS'] - test['CCSD/CBS'] - test['(T)-D/CBS'] - test['(Q)L-(T)/CBS'] - test['(P)L-(Q)L/CBS'] 


        test['Semiempirical ZPE Unc'] = np.sqrt(unc['SCF BSIE']**2 + unc['CCSD BSIE']**2 + unc['(T)-D BSIE']**2 + unc['(Q)L-(T) BSIE']**2 + unc['(P)L-(Q)L BSIE']**2 + unc['Post-(P)L HLC']**2 + unc['SREL SCF BSIE']**2 + unc['SREL CCSD BSIE']**2 + unc['SREL (T)-D BSIE']**2 + unc['SREL HLC est']**2 + unc['DBOC unc est']**2 + unc['2nd Order SO est']**2)
        test['Semiempirical ZPE Unc (no SO unc)'] = np.sqrt(unc['SCF BSIE']**2 + unc['CCSD BSIE']**2 + unc['(T)-D BSIE']**2 + unc['(Q)L-(T) BSIE']**2 + unc['(P)L-(Q)L BSIE']**2 + unc['Post-(P)L HLC']**2 + unc['SREL SCF BSIE']**2 + unc['SREL CCSD BSIE']**2 + unc['SREL (T)-D BSIE']**2 + unc['SREL HLC est']**2 + unc['DBOC unc est']**2)

        test[['Semiempirical ZPE', 'Semiempirical ZPE Unc', 'Semiempirical ZPE Unc (no SO unc)']].to_csv(f"zpe_{name}.csv")


    #Save to files
    for name, test in tests.items():
        test.to_csv(f"unc_{name}.csv")

