from scipy.io.wavfile import read
from librosa.core import stft
import numpy as np
from sklearn.decomposition import PCA

class AudioArray:
    def __init__(self, audio):
        self.audio = audio

    def audio_to_vector:
        #read the audio sample
        a = read("wind_01.wav")

        #convert the audio to an array
        a = np.array(a[1],dtype=float)
        print(a)

        #short-time Fourier transform
        A = np.abs(stft(a))
        print(A)

        #reduce number of dimensions
        pca = PCA(n_components=8)
        #pca.fit(A)
        #print pca.explained_variance_ratio_

        pca.fit_transform(A)
        print ("A", A)