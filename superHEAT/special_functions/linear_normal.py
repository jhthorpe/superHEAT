# linear_normal.py 
#
# Contains the Linear_Normal class, which is used to model error profiles where the
# trend of the error is fit via:
#
#   f(x) = a*x
#
# And a normal-distributed uncertainty which is centered on the error trend and which 
# extends perpendicular to the error-trend with a sigma which is modeled as linearly 
# dependent on the value of the error:
#
#   \sigma(x) = s0 + b * x 
#
# One can envision this as a distribution of normal distributions who are centered
# on f(x) and whose widths cover the line perpendicular to f(x) and can vary linearly
# as a function of x
#
# Note that the linear form of the normal distributions implies that there is a
# finte range in which this model can be used, as sigma must always be greater than 
# zero. You can test this range using the "valid_range" function in the class
#
# NOTES:
# June 13, 2025 @ ANL : JHT created. 
# 

import numpy as np
from scipy import optimize as opt
from scipy import stats
import math

from superHEAT.special_functions.trending_error import Trending_Error
from superHEAT.special_functions.sample_cdf import Sample_CDF

# This is the definion of our error-trend function
def ax(x, a):
    return np.multiply(a, x)

# This is the definition of our uncertainty spread function 
def s0pbx(x, s0, b):
    return np.add(s0, np.multiply(b, x))

class Linear_Normal(Trending_Error):

    def __init__(self, a=1, s0=1, b=0):  

        Trending_Error.__init__(self, ax, s0pbx, [a], [s0, b])

        self.a = a
        self.s0 = s0
        self.b = b

        assert(self.s0 > 0), f"s0 in normal model must be greater than zero"

    def __str__(self):
        return f"f(x) = {self.a}x; sig(x) = {self.s0} + {self.b} * x"

    # returns the lower and upper bounds of 
    # the current model
    def valid_range(self):
        lo = -self.s0/self.b if self.b > 0 else -math.inf
        hi = -self.s0/self.b if self.b < 0 else math.inf
        return lo, hi

    # Returns the distance of a vector of points (x, y) to the f(x) line 
    def dist(self, x, y):
        den = np.sqrt(self.a * self.a + 1)
        print(den)
        num = np.abs(np.add(np.multiply(self.a, x), np.multiply(-1, y)))
        print(num)
        return np.multiply(num, 1./den) 

    # Returns the value of the PDF at some distance d from point x 

