import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tae = pd.read_csv("superHEAT_TAE.csv")
anl = pd.read_csv("superHEAT_ANL.csv")
bde = pd.read_csv("superHEAT_BDE.csv")
all = pd.read_csv("superHEAT_ALL.csv")

tae = tae.set_index("Reaction")
anl = anl.set_index("Reaction")
bde = bde.set_index("Reaction")
all = all.set_index("Reaction")

dfs = [tae, anl, bde]
names = ["TAE", "ANL", "BDE"]

# Initialize the figure with 3 rows and 1 column
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(4, 6), sharex=True)

#####################################################################################
# 
# Correlation between superHEAT and ATcT errors
#
for i, ax in enumerate(axes):
    df = dfs[i]

    # Create the scatter plot
    ax.scatter(df["ATcT Unc"], df["|Err|"], alpha=1, edgecolors='w', color='black')

    ax.set_ylim(-1, 60)

    # Formatting each subplot
    ax.set_ylabel(r"|Err| (cm$^{-1}$)")
    ax.set_title(names[i], loc='left', fontweight='bold')
#    ax.grid(True, linestyle='--', alpha=0.5)

# Set the common X-axis label on the bottom-most plot
axes[-1].set_xlabel(r"ATcT Unc (cm$^{-1}$)")

# Optimize spacing to prevent overlap
plt.tight_layout()

plt.savefig("schemes.pdf", format="pdf", bbox_inches="tight")

plt.show()
plt.close()


#####################################################################################
#
# histograms of errors
#

# Initialize the figure with 3 rows and 1 column
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(4, 6), sharex=True)

xmin = -61
xmax = 61
bwidth = 5
nbin = round((xmax - xmin)/bwidth)

for i, ax in enumerate(axes):
    df = dfs[i]

    # Create the histogram
    # range=(0, 60) ensures the bins are consistent with your previous Y-axis scale
    ax.hist(df["Err"], bins=nbin, range=(xmin, xmax), color='black', edgecolor='white', alpha=1)

    ax.set_ylim(0, 8)

    # Formatting each subplot
    ax.set_ylabel("Count")
    ax.set_title(names[i], loc='left', fontweight='bold')
#    ax.grid(True, linestyle='--', alpha=0.4, axis='y') # Grid on the y-axis is helpful for counts

# Standardizing the x-axis range to 0-60 as per your previous style
axes[-1].set_xlim(xmin, xmax)
axes[-1].set_xlabel(r"Err (cm$^{-1}$)")

plt.savefig("histograms.pdf", format="pdf", bbox_inches="tight")

plt.show()

#####################################################################################
#
# Bond order plots
#
# Initialize the figure with 3 rows and 1 column
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(4, 6), sharex=True)

xmin = -10
xmax = 10

for i, ax in enumerate(axes):
    df = dfs[i]

    # Create the scatter plot
    ax.scatter(df["Bond order"], df["Err"], alpha=1, edgecolors='w', color='black')

    ax.set_ylim(-60, 60)

    # Formatting each subplot
    ax.set_ylabel(r"Err (cm$^{-1}$)")
    ax.set_title(names[i], loc='left', fontweight='bold')
#    ax.grid(True, linestyle='--', alpha=0.5)

# Set the common X-axis label on the bottom-most plot
axes[-1].set_xlabel(r"$\Delta$ Bond Order")

# Optimize spacing to prevent overlap
plt.tight_layout()

plt.savefig("bondorder_error.pdf", format="pdf", bbox_inches="tight")

plt.show()
plt.close()

#####################################################################################
#
# Bond order plots
#
# Initialize the figure with 3 rows and 1 column
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(4, 6), sharex=True)

xmin = -10
xmax = 10

for i, ax in enumerate(axes):
    df = dfs[i]

    # Create the scatter plot
    ax.scatter(df["Bond order"], df["Total"], alpha=1, edgecolors='w', color='black')

    # Formatting each subplot
    ax.set_ylabel(r"Total (cm$^{-1}$)")
    ax.set_title(names[i], loc='left', fontweight='bold')
#    ax.grid(True, linestyle='--', alpha=0.5)

# Set the common X-axis label on the bottom-most plot
axes[-1].set_xlabel(r"$\Delta$ Bond Order")

# Optimize spacing to prevent overlap
plt.tight_layout()

plt.savefig("bondorder_total.pdf", format="pdf", bbox_inches="tight")

plt.show()
plt.close()

#####################################################################################
#
# ANL plots with and without CH4
#

anl_no_ch4 = anl[~anl.index.str.contains("CH4")]
anl_w_ch4 = anl[anl.index.str.contains("CH4")]
# Initialize the figure with 3 rows and 1 column
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 6), sharex=True)

xmin = -61
xmax = 61
bwidth = 7.5
nbin = round((xmax - xmin)/bwidth)

#fig, axes = plt.subplots()
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(4, 6), sharex=True)

name = ["ANL without CH4", "ANL with CH4"]
dfs = [anl_no_ch4, anl_w_ch4]

for i,ax in enumerate(axes):

    df = dfs[i]

    # Create the histogram
    # range=(0, 60) ensures the bins are consistent with your previous Y-axis scale
    ax.hist(df["Err"], bins=nbin, range=(xmin, xmax), color='black', edgecolor='white', alpha=1)
    
    ax.set_ylim(0, 8)
    
    # Formatting each subplot
    ax.set_ylabel("Count")
    ax.set_title(name[i], loc='left', fontweight='bold')
    # ax.grid(True, linestyle='--', alpha=0.4, axis='y') # Grid on the y-axis is helpful for counts
        
# Standardizing the x-axis range to 0-60 as per your previous style
axes[-1].set_xlim(xmin, xmax)
axes[-1].set_xlabel(r"Err (cm$^{-1}$)")

plt.savefig("ch4_histograms.pdf", format="pdf", bbox_inches="tight")

plt.show()
plt.close()


