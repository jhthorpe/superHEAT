import numpy as np
import pandas as pd
from recipe import Ingredient, Transformation

def axpby(df, names, coefs):
    return coefs['a'] * df[names['x'].name] + coefs['b'] * df[names['y'].name] 

df = pd.DataFrame({"A" : [1, 2, 3], "B" : [2,3,4], "C" : [-1,-1,-1] })

apb = Transformation(name = "A+C", func = axpby, 
                result = Ingredient(name = 'A+C', from_transform = True),
                ingredients = { 'x' : Ingredient(name = 'A'), 'y' : Ingredient(name = 'C')},
                coefs = { 'a' : 1, 'b' : 2  })

print(f"Transformation will be {apb}")

df[apb.result.name] = apb.apply(df)


print(df)


