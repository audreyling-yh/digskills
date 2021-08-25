import ast
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

df=pd.read_csv('data/tsc_bert.csv')
skill=df['tsc_title']
df['bert']=df['bert_embeddings'].apply(lambda x:ast.literal_eval(x))
embeddings=np.array(df['bert'].tolist())

numclusters=range(10,110,10)
distortion,inertia=[],[]
for i in numclusters:
    print(i)
    kmeans = KMeans(n_clusters=i)
    kmeans.fit_predict(embeddings)
    distortion.append(sum(np.min(cdist(embeddings,kmeans.cluster_centers_,'euclidean'),axis=1))/embeddings.shape[0])
    inertia.append(kmeans.inertia_)

img_folder='img/{}.png'

values=[inertia,distortion]
ylables=['Inertia','Distortion']
img_names=['inertia_elbow','distortion_elbow']
for i in range(0,len(values)):
    plt.plot(numclusters,values[i])
    plt.title('KMeans Elbow Plot')
    plt.xlabel('Number of clusters')
    plt.ylabel(ylables[i])
    plt.savefig(img_folder.format(img_names[i]))
    plt.close()