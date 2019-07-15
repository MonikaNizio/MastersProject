from scipy.io.wavfile import read
import numpy
a = read("wind_01.wav")
a = numpy.array(a[1],dtype=float)
print(a)