# stats.py
#
# Program for analysis of data 

import pandas as pd
import numpy as np
import scipy.stats as stats

tae = pd.read_csv("superHEAT_TAE.csv")
anl = pd.read_csv("superHEAT_ANL.csv")
bde = pd.read_csv("superHEAT_BDE.csv")
tot = pd.read_csv("superHEAT_ALL.csv")

tae = tae.set_index("Reaction")
anl = anl.set_index("Reaction")
bde = bde.set_index("Reaction")
tot = tot.set_index("Reaction")

sets = {"TAE" : tae, "ANL" : anl, "BDE" : bde, "Total" : tot}

def l2d(x, axis = 0):
    n = x.shape[axis]
    return np.sqrt(np.sum(np.square(x), axis=axis)/(n-1))


for dname, df in sets.items(): 

#   Uncomment to select all rows below a certain uncertainty
#    df = df[df["ATcT Unc"] < 10.]

    print(f"\nStatistics for {dname}")


    #Bootstrap the mean
    bs_mean = stats.bootstrap((df['Err'],), np.mean, n_resamples = 99999, method='BCa', vectorized=True, confidence_level=0.95)
    print(f"    Center of Bias : {df['Err'].mean()}") 
    print(f"    95% confidence: ", bs_mean.confidence_interval.low , bs_mean.confidence_interval.high )
    print("")

    #Bootstrap the mae
    bs_mae = stats.bootstrap((df['|Err|'],), np.mean, n_resamples = 99999, method='BCa', vectorized=True, confidence_level=0.95)
    print(f"    Center of MAE : {df["|Err|"].mean()}")
    print(f"    95% confidence: ", bs_mae.confidence_interval.low , bs_mae.confidence_interval.high )
    print("")

    #bootstrap the CI
    bs_l2d = stats.bootstrap((df['Err'],), l2d, n_resamples = 99999, method='BCa', vectorized=True, confidence_level=0.95)
    st = stats.t.ppf(0.975, len(df) - 1)
    print(f"    Center of 95% Conf : {st*l2d(df["Err"])}")
    print(f"    95% confidence: ", bs_l2d.confidence_interval.low * st, bs_l2d.confidence_interval.high * st)
    print("")


