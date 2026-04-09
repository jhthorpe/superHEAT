import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import pandas as pd
import copy
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

##############################################################################################################
# Data genreation and some analysis
#bad_strings = ['CCH -> C + CH', 'HCCH -> H + CCH']

true = pd.read_csv('ccsd_ALL.csv')
true = true.set_index('Reaction')

conv = pd.read_csv('ccsd_conv_ALL.csv')
conv = conv.set_index('Reaction')

conv = conv[conv.index.isin(true.index)]

print("Convergence data for Helgaker")
print(conv)

# scale
# 
#   Given a list of np-friendly elements/vectors, returns the 
#   scale of a series of values (the difference between max and min)
#
def scale(elements):
    max_ = elements[0]
    min_ = elements[0]
    for i in range(1, len(elements)):
        max_ = np.maximum(max_, elements[i])
        min_ = np.minimum(min_, elements[i])

    return max_ - min_


# Returns the (signed) angle between three subsequent basis-set extrapolations.
# Note that we assume that za < zb < zc
#
# za, zb, zc : zetas of the basis sets that form the vectors
# ea, eb, ec : energies of the thermochemical propoerties at each zeta
#
# "B" is used as the origin of the vectors AB and CB. 
#
# The sign of the angle indicates if the convergence is concave up or concave down
#
def signed_angle(w, za, ea, zb, eb, zc, ec):

    #angle between AB and CB
    zab = za - zb
    zcb = zc - zb

    #scale the values
    ea_w = ea / w
    eb_w = eb / w
    ec_w = ec / w

    eab = (ea_w - eb_w)
    ecb = (ec_w - eb_w)

    mab = np.sqrt((eab * eab) + (zab * zab))
    mcb = np.sqrt((ecb * ecb) + (zcb * zcb))

    angle = np.arccos((eab * ecb + zab * zcb) / (mab * mcb))

    sign = np.sign(ec_w - (((eab)/(zab) * (zc - za)) + ea_w) )

    return sign * angle

#
# scaled slope
#
# given a scaling factor, evaluates the "slope" between two 
# different basis set extrapolations that are rescaled
#
def scaled_slope(w, za, ea, zb, eb):
    return (eb - ea)/(w * (zb - za))

conv["scale"] = scale([conv["[fc] CCSD/aC{T,Q}Z Helg"], conv["[fc] CCSD/aC{Q,5}Z Helg"], conv["[fc] CCSD/aC{5,6}Z Helg"], 
                       conv["[fc] CCSD/aC{T,Q}Z Schw"], conv["[fc] CCSD/aC{Q,5}Z Schw"], conv["[fc] CCSD/aC{5,6}Z Schw"],
                       conv["[fc] CCSD/aC{T,Q}Z"], conv["[fc] CCSD/aC{Q,5}Z"], conv["[fc] CCSD/aC{5,6}Z"]])

conv["D(Q5) Helg"] = scaled_slope(conv["scale"], 4, conv["[fc] CCSD/aC{T,Q}Z Helg"], 5, conv["[fc] CCSD/aC{Q,5}Z Helg"])
conv["D(Q5) Schw"] = scaled_slope(conv["scale"], 4, conv["[fc] CCSD/aC{T,Q}Z Schw"], 5, conv["[fc] CCSD/aC{Q,5}Z Schw"])
conv["D(Q5)"] = scaled_slope(conv["scale"], 4, conv["[fc] CCSD/aC{T,Q}Z"], 5, conv["[fc] CCSD/aC{Q,5}Z"])
conv["D(56) Helg"] = scaled_slope(conv["scale"], 5, conv["[fc] CCSD/aC{Q,5}Z Helg"], 6, conv["[fc] CCSD/aC{5,6}Z Helg"])
conv["D(56) Schw"] = scaled_slope(conv["scale"], 5, conv["[fc] CCSD/aC{Q,5}Z Schw"], 6, conv["[fc] CCSD/aC{5,6}Z Schw"])
conv["D(56)"] = scaled_slope(conv["scale"], 5, conv["[fc] CCSD/aC{Q,5}Z"], 6, conv["[fc] CCSD/aC{5,6}Z"])
conv["D(67) Helg"] = scaled_slope(conv["scale"], 6, conv["[fc] CCSD/aC{5,6}Z Helg"], 7, conv["[fc] CCSD/aC{6,7}Z Helg"])
conv["D(67) Schw"] = scaled_slope(conv["scale"], 6, conv["[fc] CCSD/aC{5,6}Z Schw"], 7, conv["[fc] CCSD/aC{6,7}Z Schw"])
conv["D(67)"] = scaled_slope(conv["scale"], 6, conv["[fc] CCSD/aC{5,6}Z"], 7, conv["[fc] CCSD/aC{6,7}Z"])

conv["A(Q56) Helg"] = signed_angle(conv["scale"], 4, conv["[fc] CCSD/aC{T,Q}Z Helg"], 5, conv["[fc] CCSD/aC{Q,5}Z Helg"], 6, conv["[fc] CCSD/aC{5,6}Z Helg"]) 
conv["A(Q56) Schw"] = signed_angle(conv["scale"], 4, conv["[fc] CCSD/aC{T,Q}Z Schw"], 5, conv["[fc] CCSD/aC{Q,5}Z Schw"], 6, conv["[fc] CCSD/aC{5,6}Z Schw"]) 
conv["A(Q56)"] = signed_angle(conv["scale"], 4, conv["[fc] CCSD/aC{T,Q}Z"], 5, conv["[fc] CCSD/aC{Q,5}Z"], 6, conv["[fc] CCSD/aC{5,6}Z"]) 
conv["A(567) Helg"] = signed_angle(conv["scale"], 5, conv["[fc] CCSD/aC{Q,5}Z Helg"], 6, conv["[fc] CCSD/aC{5,6}Z Helg"], 7, conv["[fc] CCSD/aC{6,7}Z Helg"]) 
conv["A(567) Schw"] = signed_angle(conv["scale"], 5, conv["[fc] CCSD/aC{Q,5}Z Schw"], 6, conv["[fc] CCSD/aC{5,6}Z Schw"], 7, conv["[fc] CCSD/aC{6,7}Z Schw"]) 
conv["A(567)"] = signed_angle(conv["scale"], 5, conv["[fc] CCSD/aC{Q,5}Z"], 6, conv["[fc] CCSD/aC{5,6}Z"], 7, conv["[fc] CCSD/aC{6,7}Z"]) 

angle_features = ["A(Q56) Helg", "A(567) Helg", "A(Q56) Schw", "A(567) Schw"] 
slope_features = ["D(Q5) Helg", "D(Q5) Schw", "D(56) Helg", "D(56) Schw", "D(67) Helg", "D(67) Schw"]
#angle_features = ["A(Q56) Helg", "A(567) Helg", "A(Q56) Schw", "A(567) Schw", "A(Q56)", "A(567)"] 
#slope_features = ["D(Q5) Helg", "D(Q5) Schw", "D(Q5)", "D(56) Helg", "D(56) Schw", "D(56)", "D(67) Helg", "D(67) Schw", "D(67)"]
all_features = angle_features + slope_features

print("\n\nAngles analysis") 
print(conv[["scale", "A(Q56) Helg", "A(567) Helg", "A(Q56)", "A(567)", "A(Q56) Schw", "A(567) Schw"]])
print("\n\nSlope analysis")
print(conv[["scale", "A(Q56) Helg", "A(567) Helg", "A(Q56)", "A(567)", "A(Q56) Schw", "A(567) Schw"]])


##############################################################################################################
# k means cluster based off the Q56 and 567 angles for the three extrapolations (6 total dimensions)
#features = ["A(Q56) Helg", "A(567) Helg", "A(Q56) Schw", "A(567) Schw", "A(Q56)", "A(567)"]
#features = ["D(Q5) Helg", "D(Q5) Schw", "D(Q5)", "D(56) Helg", "D(56) Schw", "D(56)", "D(67) Helg", "D(67) Schw", "D(67)"]

#features = all_features
features = angle_features
#features = slope_features

cost = []
sil_score = []
K = range(2, 24)
for k in K:
    kmeans = KMeans(init="k-means++", n_clusters=k, n_init=20, random_state=137)
    
    res = kmeans.fit_predict(conv[features])
    cost.append(kmeans.inertia_)
    sil_score.append(silhouette_score(conv[features], res))

#Plot the convergence of the clustering wrt k

fig, ax1 = plt.subplots()
ax1.set_xlabel("#clusters")
ax1.set_ylabel("Inertia Score")
ax1.plot(K, cost, 'bx-', label="Inertia Score")

ax2 = ax1.twinx()
ax2.set_ylabel("Silhouette Score")
ax2.plot(K, sil_score, '--', label="Sil Score")
plt.show()

#Get user input to determine the number of clusters to use
k_selected = input("Enter k: ")
k_selected = int(k_selected)

kmeans = KMeans(init="k-means++", n_clusters=k_selected, n_init=20, random_state=137)
conv['cluster'] = kmeans.fit_predict(conv[features])

print("Clustered curvature analysis")
features.append('cluster')
print(conv[features].sort_values(by="cluster"))

count_per_cluster = []
for k in range(k_selected):
    count_per_cluster.append((conv['cluster'] == k).sum())

print("Counts per cluster: ", count_per_cluster)

# PCA Analysis
pca = PCA(n_components=3)
X_pca = pca.fit_transform(conv[features])

fig,axes = plt.subplots(nrows=1, ncols=3, figsize=(8,4))
axes[-1].set_title("PCA")

axes[0].scatter(X_pca[:,0], X_pca[:,1], c=conv['cluster'], cmap='viridis')
axes[0].set_xlabel("PCA Comp 1")
axes[0].set_ylabel("PCA Comp 2")

axes[1].scatter(X_pca[:,0], X_pca[:,2], c=conv['cluster'], cmap='viridis')
axes[1].set_xlabel("PCA Comp 1")
axes[1].set_ylabel("PCA Comp 3")

axes[2].scatter(X_pca[:,1], X_pca[:,2], c=conv['cluster'], cmap='viridis')
axes[2].set_xlabel("PCA Comp 2")
axes[2].set_ylabel("PCA Comp 3")

plt.show()

#tsne analysis

tsne = TSNE(n_components=3, random_state=42)
X_tsne = tsne.fit_transform(conv[features])

fig,axes = plt.subplots(nrows=1, ncols=3, figsize=(8,4))
axes[-1].set_title("TSNE")

axes[0].scatter(X_tsne[:,0], X_tsne[:,1], c=conv['cluster'], cmap='viridis')
axes[0].set_xlabel("TSNE Comp 1")
axes[0].set_ylabel("TSNE Comp 2")

axes[1].scatter(X_tsne[:,0], X_tsne[:,2], c=conv['cluster'], cmap='viridis')
axes[1].set_xlabel("TSNE Comp 1")
axes[1].set_ylabel("TSNE Comp 3")

axes[2].scatter(X_tsne[:,1], X_tsne[:,2], c=conv['cluster'], cmap='viridis')
axes[2].set_xlabel("TSNE Comp 2")
axes[2].set_ylabel("TSNE Comp 3")

plt.show()


##############################################################################################################
# Make data function that selects things we want in our subplots
def make_data(name, idx, true_df, conv_df):

    x = [4, 5, 6, 7]

    avg = conv_df.loc[idx, ["[fc] CCSD/aC{T,Q}Z", "[fc] CCSD/aC{Q,5}Z", "[fc] CCSD/aC{5,6}Z", "[fc] CCSD/aC{6,7}Z"]]
    helg = conv_df.loc[idx, ["[fc] CCSD/aC{T,Q}Z Helg", "[fc] CCSD/aC{Q,5}Z Helg", "[fc] CCSD/aC{5,6}Z Helg", "[fc] CCSD/aC{6,7}Z Helg"]]
    schw = conv_df.loc[idx, ["[fc] CCSD/aC{T,Q}Z Schw", "[fc] CCSD/aC{Q,5}Z Schw", "[fc] CCSD/aC{5,6}Z Schw", "[fc] CCSD/aC{6,7}Z Schw"]]
    scale = conv_df.loc[idx, ['scale']]

    truev = true_df.loc[idx, 'Semiempirical [fc] CCSD']
    truev_unc = true_df.loc[idx, 'Semiempirical [fc] CCSD unc.']

    data = {
        'x' : x, 
        'Helg' : helg.to_numpy(), 
        'Schw' : schw.to_numpy(), 
        'Avg'  : avg.to_numpy(), 
        'True' : truev,
        'True unc' : truev_unc,
        'scale' : scale.to_numpy()
        }

    return data

ntotal = len(true)
if (len(conv) != ntotal):
    print(f"Lengths of convergence data and benchmark data not equivilant : {len(conv)} vs {len(true)}")
    exit(1)

#New style, with clustering
nrow = k_selected
ncol = np.max(count_per_cluster)

# Old style, without clustering. Set 5 for general viewability
#nrow = 5
#ncol = (ntotal + nrow - 1) // nrow 
npad = ncol * nrow - ntotal

# Generate indexed lookups for the data in the dataframe. This gets a bit more complicated for clustering 

# What works if you don't care about clustering
#idxs = copy.deepcopy(conv.index)
#idxs = np.pad(idxs, (0, npad), mode='constant', constant_values = None)
#idxs = idxs.reshape((nrow, ncol))

#What we need to do for clustering...
idxs = np.full((nrow, ncol), None, dtype=np.dtypes.StringDType)

counter = np.full((k_selected), 0, dtype=np.integer)
for idx, cluster in conv['cluster'].items():
    idxs[cluster, counter[cluster]] = idx
    counter[cluster] += 1


fit, axes = plt.subplots(nrows = nrow, ncols = ncol, figsize=(20,10))
fsize = 5
tsize = 3
msize = 1
lwidth = 1

# Row loops over clusters
# col loops over examples per cluster
#for i in range(nrow):
#    for j in range(ncol):
for i in range(nrow):
    for j in range(ncol):
        if idxs[i, j] is None or idxs[i, j] == 'None':
            continue

        ax = axes[i,j] 
        name = idxs[i, j]
        idx = idxs[i, j] 

        data = make_data(name, idx, true, conv) 

        x = data['x']
        scale = data['scale'][0]
        Helg = data['Helg']/scale
        Schw = data['Schw']/scale
        Avg = data['Avg']/scale
        truev = data['True'] / scale
        truev_unc = data['True unc'] / scale 

        ax.plot(x, Helg, color='black', marker='s', markersize=msize, linestyle='-', linewidth=lwidth)
        ax.plot(x, Schw, color='black', marker='s', markersize=msize, linestyle='--', linewidth=lwidth)
        ax.plot(x, Avg, color='black', marker='s', markersize=msize, linestyle='-.', linewidth=lwidth)

        lo = truev - truev_unc 
        hi = truev + truev_unc 

        ax.axhline(y=lo, color='blue', linestyle='-', linewidth=1)
        ax.axhline(y=hi, color='blue', linestyle='-', linewidth=1)
        ax.axhspan(lo, hi, color='blue', alpha=0.15)

        ax.set_xlim(4,7)

        #ylabel = r'[fc] $\Delta E^\infty_{\text{CCSD}}$ for '
        #ylabel += f'{figlab[i][j]} ' 
        #ylabel += r'(cm$^{-1}$)'
        ylabel = f'{name}'
        ax.set_ylabel(ylabel, fontsize=fsize, labelpad=5, fontname='Helvetica')
        #ax.set_xlabel(r'aug-cc-pCV{$n-1$,$n$}Z', fontsize=fsize, fontname='Helvetica', labelpad=10)
        ax.set_xlabel(r'Zeta', fontsize=fsize, fontname='Helvetica', labelpad=5)

        ax.tick_params(
            axis='both',
            which='minor',
            direction='in',
        )
        ax.tick_params(
            axis='both',
            which='major',
            direction='in'
        )
        
        ax.set_xticks(np.arange(4, 8, 1))
        
        for tick in ax.get_xticklabels():
            tick.set_fontname('Helvetica')
            tick.set_fontsize(tsize)
        for tick in ax.get_yticklabels():
            tick.set_fontname('Helvetica')
            tick.set_fontsize(tsize)
        
        y_min, y_max = ax.get_ylim()
#        ax.set_yticks(np.arange(np.floor(y_min / 10) * 10, np.ceil(y_max / 10) * 10 + 10, 10), minor=True)
        ax.tick_params(axis='y', which='minor', length=2, color='black')


plt.tight_layout()

plt.savefig("ccsd_all.png",dpi=300)

plt.show()
