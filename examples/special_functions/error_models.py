from superHEAT.special_functions.linear_normal import Linear_Normal
from superHEAT.special_functions.trending_error import Trending_Error

def f(x, a):
    return x*a

def s(x, b, c):
    return b + c*x

ll = Trending_Error(f, s, [-1], [1.5, 1])

print(ll.f(0))
print(ll.f(1))
print(ll.sigma(0))
print(ll.sigma(1))
print(ll.normal(0).stats())
print(ll.normal(1).stats())

ln = Linear_Normal(-1, 1.5, 1)
print(ln.f(0))
print(ln.f(1))
print(ln.sigma(0))
print(ln.sigma(1))
print(ln.normal(0).stats())
print(ln.normal(1).stats())
