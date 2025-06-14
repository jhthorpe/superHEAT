# test_special_functions.py 
#
# Contains unit tests for the special_functions
#
# NOTE:
#   The list of unit tests are at the bottom

import pytest
import math

from scipy.stats import norm
import numpy as np

from superHEAT.special_functions.trending_error import Trending_Error
from superHEAT.special_functions.linear_normal import Linear_Normal
from superHEAT.special_functions.linear_normal import ax
from superHEAT.special_functions.linear_normal import s0pbx
from superHEAT.special_functions.sample_cdf import Sample_CDF

##
# These are the same
@pytest.mark.parametrize("x, a, s0, b", [
    (0, -1, 0.5, 1),
    (1, -1, 0.5, 1),
    (1,  2, 0.5, 0.5)
    ])
def test_linear_normal_is_linear(x, a, s0, b):
    ln = Linear_Normal(a, s0, b)
    gen = Trending_Error(ax, s0pbx, [a], [s0, b])
    assert(ln.f(x) == gen.f(x))
    assert(ln.sigma(x) == gen.sigma(x))
    assert(ln.normal(x).stats() == gen.normal(x).stats())

##
# Correctness check 
@pytest.mark.parametrize("x, a, s0, b", [
    (0, -1, 1, 1),
    (1, -1, 10, 1),
    (-5, 2, 0.1, -0.5)
    ])
def test_linear_normal_correctness(x, a, s0, b):
    ln = Linear_Normal(a, s0, b)
    assert(ln.f(x) == a*x)
    assert(ln.sigma(x) == s0 + b * x) 
    assert(ln.normal(x).stats() == norm(loc=0, scale=s0pbx(x, s0, b)).stats())

##
# check that linear normal throws and error if s0 is negative
def test_linear_nonegsig():
    with pytest.raises(AssertionError): 
        ln = Linear_Normal(0, -1, 0)

##
# check that we get a valid range with linear normal
@pytest.mark.parametrize("a, s0, b, lo, hi", [
    (0, 1, 0, -math.inf, math.inf),
    (1, 1.5, 2, -0.75, math.inf),
    (-1, 1.5, -2, -math.inf, 0.75)
    ])
def test_linear_range(a, s0, b, lo, hi):
    ln = Linear_Normal(a, s0, b)
    lo0, hi0 = ln.valid_range()
    assert(lo0 == lo)
    assert(hi0 == hi)
##
# check generation of a CDF from a sample
@pytest.mark.parametrize("x, xsort, y", [
    ([10,9,8,7],
     [7,8,9,10],
     [0.25, 0.5, 0.75, 1.])
    ])
def test_sample_cdf(x, xsort, y):
    v, c = Sample_CDF(x)
    assert((v == xsort).all())
    assert((y == c).all())

##
# check distance of points to the f(x) line
@pytest.mark.parametrize("a, x, y, d", [
    (-2, 1, 0.5, 1.118033988749895),
    (2, 10, 0.5, 8.72066511224918),
    (2, np.array([1, 2]), np.array([2, 1]), np.array([0., 1.3416407864998738]))
    ])
def test_linear_normal_distance(a, x, y, d):
    ln = Linear_Normal(a, 1, 1)
    assert((ln.dist(x, y) == d).all())
