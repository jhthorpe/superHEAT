from superHEAT.special_functions.linear_normal import Linear_Normal

import scipy.optimize as opt
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import erf
import numpy as np
import math

import threading

def mcdf(x, mu, sig):
    return 0.5*(1 + erf( (x - mu) / (sig * math.sqrt(2)) ) )

def dcdf_dsig(x, mu, sig):
    z = np.add(x, -mu)
    z = np.multiply(z, 1. / (sig * math.sqrt(2)))
    zz = np.multiply(-z, z)
    zz = np.exp(zz)
    z = np.multiply(z, zz)
    return np.multiply(z, -1 / (math.sqrt(math.pi) * sig ))

def dcdf_dmu(x, mu, sig):
    z = np.add(x, -mu)
    z = np.multiply(z, 1. / (sig * math.sqrt(2)))
    zz = np.multiply(-z, z)
    zz = np.exp(zz)
    return np.multiply(zz, -1 / (math.sqrt(math.pi * 2) * sig ))

#from a distribution, generate the cdf
def ncdf(x):

    #sort x
    x = np.sort(x)

    y = np.zeros((len(x)))

    for i in range(1,len(x)):
        y[i] = i

    re = y[-1]

    y = y/re

    return x, y


mu = 0.25
sigma = 1.5

nd = norm(loc = mu, scale = sigma)

#generate a distribution like this
n = 100000
dist = np.random.normal(loc = mu, scale = sigma, size= n)

print(dist)

#def cdf
dist, cdf = ncdf(dist)

x = 0.5
m = mu
s = sigma
print("true cdf at {x}", nd.cdf(x))
print("my cdf at {x}", mcdf(x, m, s))
print("numerical test for cdf derivative")
print(f"x = {x}, m = {m}, s = {s}", mcdf(x, m, s)) 
print(f"x = {x}, m = {m}, s = {s+0.1}", mcdf(x, m, s+0.1)) 
print("sigma derivs")
print("derivative : 0.1", (mcdf(x, m, s+0.1) - mcdf(x, m, s))/0.1)
print("derivative : 0.01", (mcdf(x, m, s+0.01) - mcdf(x, m, s))/0.01)
print("derivative : 0.001", (mcdf(x, m, s+0.001) - mcdf(x, m, s))/0.001)
print("derivative : 0.0001", (mcdf(x, m, s+0.0001) - mcdf(x, m, s))/0.0001)
print("analytical :", dcdf_dsig(x, m, s))
print("mu derivs")
print("derivative : 0.1", (mcdf(x, m+0.1, s) - mcdf(x, m, s))/0.1)
print("derivative : 0.01", (mcdf(x, m+0.01, s) - mcdf(x, m, s))/0.01)
print("derivative : 0.001", (mcdf(x, m+0.001, s) - mcdf(x, m, s))/0.001)
print("derivative : 0.0001", (mcdf(x, m+0.0001, s) - mcdf(x, m, s))/0.0001)
print("analytical :", dcdf_dmu(x, m, s))

print("vectorize test", dcdf_dsig(np.array([-0.5, 0, 0.5]), 0., 1.))

#Now we can try to fit the numerical CDF to the model 
def mjac(x, mu, sig):
    z = np.add(x, -mu)
    z = np.multiply(z, 1. / (sig * math.sqrt(2)))
    zz = np.multiply(-z, z)
    zz = np.exp(zz)
    z = np.multiply(z, zz)
    return np.transpose([np.multiply(zz, -1 / (math.sqrt(math.pi * 2) * sig )), 
                        np.multiply(z, -1 / (math.sqrt(math.pi) * sig ))])

#def mmjac(x, arg):
#    mu = arg[0]
#    sig = arg[1]
#    return [dcdf_dmu(x, mu, sig), dcdf_dsig(x, mu, sig)]

popt, pconv = opt.curve_fit(mcdf, dist, cdf, [0.000001, 1], jac = mjac) 
print(popt)
