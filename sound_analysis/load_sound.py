from scipy.io.wavfile import read
from librosa.core import stft
import numpy as np
from sklearn.decomposition import PCA

#class ProcessAudio:
def audio_to_array(audio):
    #self.audio = audio

    #read the audio sample
    a = read(audio)

    #convert the audio to an array
    a = np.array(a[1],dtype=float)
    #print(a)

    #short-time Fourier transform
    A = np.abs(stft(a))
    #print(A)

    #reduce number of dimensions
    pca = PCA(n_components=8)

    pca.fit_transform(A)

    #print ("A", A)
    return A

syn1, syn2, syn3, syn4, syn5, syn6, syn7, syn8, syn9 = "synth_samples/synth1.wav", "synth_samples/synth2.wav", "synth_samples/synth3.wav", "synth_samples/synth4.wav", "synth_samples/synth5.wav", "synth_samples/synth6.wav", "synth_samples/synth7.wav", "synth_samples/synth8.wav", "synth_samples/synth9.wav"
#syn1 = "synth_samples/synth1.wav"
#sample1 = audio_to_array(syn1)

samples_arrays = [audio_to_array(syn1), audio_to_array(syn2), audio_to_array(syn3), audio_to_array(syn4), audio_to_array(syn5), audio_to_array(syn6), audio_to_array(syn7), audio_to_array(syn8), audio_to_array(syn9)]

samples_values = [[127, 127, 127, 127, 127, 5999, 0, 0], [157, 127, 127, 127, 127, 5999, 0, 0], [127, 157, 127, 127, 127, 5999, 0, 0], [127, 127, 157, 127, 127, 5999, 0, 0], [127, 127, 127, 157, 127, 5999, 0, 0], [127, 127, 127, 127, 157, 5999, 0, 0], [127, 127, 127, 127, 127, 0, 0, 0], [127, 127, 127, 127, 127, 5999, 999, 0], [127, 127, 127, 127, 127, 5999, 0, 699]]

