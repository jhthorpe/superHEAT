import pandas as pd
from heat import l2d

import scipy.stats as stats

pd.set_option("display.max_rows", None)

reactions = [
    "CH3 -> 3 H + C",
    "CH3 + 0.5 H2 -> CH4",
    "CH3 -> CH2 + H",
    "CH4 -> CH3 + H",
    "CH2 -> 2 H + C",
    "CH2 + H2 -> CH4",
    "CH2 -> CH + H",
    "CH3 -> CH2 + H",
    "CH -> H + C",
    "C + 2.0 H2 -> CH4",
    "CH + 1.5 H2 -> CH4"
]

reactions = list(dict.fromkeys(reactions))


all = pd.read_csv("superHEAT_ALL.csv")
all = all.set_index("Reaction")

anl = pd.read_csv("superHEAT_ANL.csv")
anl = anl.set_index("Reaction")

chn = all.loc[reactions]

print(chn)


anl_w_ch4 = anl[anl.index.str.contains("CH4")]
anl_no_ch4 = anl[~anl.index.str.contains("CH4")]

print("ANL with CH4 Reaction")
print(  f"Bias : {anl_w_ch4["Err"].mean()}")
print(  f"MAE : {anl_w_ch4["|Err|"].mean()}")
print(  f"95 CI : {l2d(anl_w_ch4["|Err|"].mean()}")
