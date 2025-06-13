# test_special_functions.py 
#
# Contains unit tests for the special_functions
#
# NOTE:
#   The list of unit tests are at the bottom

import pytest
import math

from scipy.stats import norm

from superHEAT.special_functions.trending_error import Trending_Error
from superHEAT.special_functions.linear_normal import Linear_Normal
from superHEAT.special_functions.linear_normal import ax
from superHEAT.special_functions.linear_normal import s0pbx

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
    assert(ln.f(x) == ax(x, a))
    assert(ln.sigma(x) == s0pbx(x, s0, b)) 
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

