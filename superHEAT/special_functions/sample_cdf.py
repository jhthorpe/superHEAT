# sample_cdf.py
#
# Generate a CDF from a sample

import numpy as np

def Sample_CDF(x):
    x = np.sort(x)

    y = np.zeros((len(x)))

    for i in range(0,len(x)):
        y[i] = i+1

    re = y[-1]

    y = np.multiply(y, 1./re)

    return x, y


