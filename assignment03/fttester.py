import numpy as np
from numpy import fft
from scipy.io import wavfile
import scipy.io as sp
import scipy.signal as spsig
import matplotlib.pyplot as plt

fs = 44100
time = np.arange(0,3,1/fs)
carrier = np.sin(2*np.pi*20*time)
modulator = np.linspace(0,19980,len(time))
sweep = np.sin(2*np.pi*(modulator+carrier)*time)
plt.plot(sweep)
plt.xlim(0,44100)
plt.show()