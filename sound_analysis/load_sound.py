from scipy.io.wavfile import read
from librosa.core import stft
import numpy as np
from sklearn.decomposition import PCA

#class ProcessAudio:
def audio_to_vector(audio):
    #self.audio = audio
    a = read(audio)
    a = np.array(a[1],dtype=float)
    #print(a)
    A = np.abs(stft(a))
    #print(A)

    pca = PCA(n_components=8)

    pca.fit_transform(A)

    print ("A", A)
    return A

syn1, syn2, syn3, syn4, syn5, syn6, syn7, syn8, syn9 = "synth_samples/synth1.wav", "synth_samples/synth2.wav", "synth_samples/synth3.wav", "synth_samples/synth4.wav", "synth_samples/synth5.wav", "synth_samples/synth6.wav", "synth_samples/synth7.wav", "synth_samples/synth8.wav", "synth_samples/synth9.wav"
#syn1 = "synth_samples/synth1.wav"
sample1 = audio_to_vector(syn1)