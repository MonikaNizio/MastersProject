from scipy.io.wavfile import read
from librosa.core import stft, load
from librosa.util import normalize
from librosa.feature import mfcc
import numpy as np
from sklearn.decomposition import PCA
import soundfile as sf

#class ProcessAudio:
def audio_to_array(audio):

    #extract audio data and sampling rate from file
    data, fs = sf.read(audio)

    #convert to wav file at correct sampling rate
    sf.write(audio, data, fs)

    #read the audio sample
    audio = read(audio)

    #[removed]
    #y, sr = load(audio, offset=30, duration=5)
    #audio_arr = mfcc(y=y, sr=sr)

    #convert the audio to an array
    audio_arr = np.array(audio[1],dtype=float)

    #normalize
    audio_arr = normalize(audio_arr, np.inf, 0)

    #short-time Fourier transform
    audio_arr = np.abs(stft(audio_arr))

    #[removed]
    #Mel - frequency cepstral coefficients(MFCCs)
    #audio_arr = np.abs(mfcc(audio_arr))
    #audio_arr = mfcc(audio_arr, sr=44100)

    #reduce number of dimensions
    pca = PCA(n_components=8)
    audio_arr = pca.fit_transform(audio_arr)
    return audio_arr
