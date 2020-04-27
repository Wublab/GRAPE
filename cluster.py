import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import sys

df = pd.read_csv(sys.argv[1])

labels = np.array(df["Mutation"])
data = np.array(df[["dTm","Interaction cluster","Region","Distance","Hbonds","Hydrophobic interactions",
                   "Entropy change","Binding region"]])

#import numpy as np

#data = np.array(data_list)
#labels = np.array(labels_list)

N_CLUSTERS = 3

kmeans = KMeans(init='k-means++', n_clusters=N_CLUSTERS,n_init=9)
kmeans.fit(data)
pred_classes = kmeans.predict(data)

for cluster in range(N_CLUSTERS):
    print('cluster: ', cluster)
    print(labels[np.where(pred_classes == cluster)])
