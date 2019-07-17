from scipy.io.wavfile import read
from librosa.core import stft
import numpy as np
from sklearn.decomposition import PCA

a = read("wind_01.wav")
a = np.array(a[1],dtype=float)
print(a)
A = np.abs(stft(a))
print(A)

pca = PCA(n_components=2)
#pca.fit(A)

#print pca.explained_variance_ratio_


pca.fit_transform(A)

print ("A", A)