# trending_error.py 
#
# Contains the Trending_Error class. This is a special class of function
# intended to model trends in errors. This contains two parts: a 
# function, f(x), which describes the center of a set of errors, and a
# function sigma(x), which describes the width of a normal distribution
# perpendicular to, and centered upon, f(x), and which is assumed to have
# varying "noise" as a function of x.
#
#
# the f_model and s_model functions *must* take x as the first argument, and if
# more arguments are needed their values must be supplied in the f_model_args and
# s_model_args.
#
# For example, if you model was:
# 
# f(x) = -2x + 5
# s(x) = 0.5
#
# You would construct the trending error as follows:
#
#   def f(x, a, c):
#       return a*x + c
#
#   def s(x, b):
#       return b
#
#   model = trending_error(f, s, [-2, 5], [0.5]) 
#
#
# NOTES:
# June 13, 2025 @ ANL : JHT created. 
# 

import numpy as np
from scipy import optimize as opt
from scipy import stats
import math

class Trending_Error:

    def __init__(self, f_model, s_model, f_model_args, s_model_args): 
        self.f_model_ = f_model
        self.s_model_ = s_model
        self.f_model_args_ = f_model_args
        self.s_model_args_ = s_model_args

        assert(callable(self.f_model_))
        assert(callable(self.s_model_))

    def __str__(self):
        return f"f(x) = {self.f_model_} : {self.f_model_args_}\nsig(x) = {self.s_model_} : {self.s_model_args_}" 

    def f(self, x):
        return self.f_model_(x, *self.f_model_args_) 

    def sigma(self, x):
        return self.s_model_(x, *self.s_model_args_) 

    # Return a scipy normal distribution that describes the noise 
    #   perpendicular to f(x) 
    #
    # * IMPORTANT                                                          *
    # * Note that this is in the coordinate system of said distribution!!! * 
    # *                                                                    *
    # * Hence the distribution is centered at 0, and the "x" axis of the   *
    # *     distribution is, in the frame of the model, actually the       *
    # *     line perpendicular to f(x)                                     *
    #
    def normal(self, x):
        return stats.norm(loc = 0, scale = self.sigma(x)) 
