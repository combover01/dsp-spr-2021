import numpy as np
from numpy import fft
from scipy.io import wavfile
import scipy.io as sp
import scipy.signal as spsig
import matplotlib.pyplot as plt

# Q1: Generating sinusoids
def generateSinusoidal(amplitude,sampling_rate_Hz,frequency_Hz,length_secs,phase_radians):
    t = np.linspace(0,length_secs,int(sampling_rate_Hz*length_secs))
    x = amplitude*np.sin(t*frequency_Hz*2*np.pi + phase_radians)
    return t,x

(t,sinWave) = generateSinusoidal(1,44100,400,0.5,np.pi/2)
plt.plot(t,sinWave)
plt.xlim(0,0.005) #show 5 ms
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("5 ms of a 400 Hz sine wave with phase pi/2")
plt.savefig('assignment03/results/sine.png')
plt.show()

#Q2: Combining sinusoids to generate waveforms with complex spectra
def generateSquare(amplitude,sampling_rate_Hz,frequency_Hz,length_secs,phase_radians):
    x = np.zeros(int(length_secs*sampling_rate_Hz))
    for i in range(10):
        num = 2*i+1 #find the harmonic number (should all be odd)
        multiplier=1/num #find the multiplier of each harmonic
        (t,harmonic) = generateSinusoidal(amplitude,sampling_rate_Hz,frequency_Hz*num,length_secs,phase_radians)
        harmonic = harmonic*multiplier
        x = x+harmonic
    return t,x

(t,squareWave) = generateSquare(1,44100,400,0.5,0)
plt.plot(t,squareWave)
plt.xlim(0,0.005) #show 5 ms
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("5 ms of a 400 Hz square wave with phase 0")
plt.savefig('assignment03/results/square.png')
plt.show()


#Q3: Fourier Transform
def computeSpectrum(x,sample_rate_Hz):
    fftOfX = np.fft.fft(x)
    XAbs = np.abs(fftOfX)
    XPhase = np.angle(fftOfX)
    XRe = fftOfX.real
    XIm = fftOfX.imag
    f = np.zeros(int(len(fftOfX)/2))
    usefulFreqs = int(len(fftOfX)/2)
    for i in range(usefulFreqs):
        curF = i*sample_rate_Hz/len(fftOfX)
        f[i] = curF
    return f,XAbs,XPhase,XRe,XIm

# spectrum of sine wave
fSin,XAbsSin,XPhaseSin,XReSin,XImSin = computeSpectrum(sinWave,44100)
plt.subplot(2,1,1, title="Magnitude Spectrum of Sinusoid",xlabel="Frequency (Hz)",ylabel="Magnitude")
plt.plot(fSin,XAbsSin[0:len(fSin)])
plt.subplot(2,1,2, title="Phase Spectrum of Sinusoid",xlabel="Frequency (Hz)",ylabel="Angle (Rads)")
plt.plot(fSin,XPhaseSin[0:len(fSin)])
plt.tight_layout()
plt.savefig('assignment03/results/sinspectrum.png')
plt.show()

# spectrum of square wave
fSq,XAbsSq,XPhaseSq,XReSq,XImSq = computeSpectrum(squareWave,44100)
plt.subplot(2,1,1, title="Magnitude Spectrum of Square Wave",xlabel="Frequency (Hz)",ylabel="Magnitude")
plt.plot(fSq,XAbsSq[0:len(fSq)])
plt.subplot(2,1,2,title="Phase Spectrum of Square Wave",xlabel="Frequency (Hz)",ylabel="Angle (Rads)")
plt.plot(fSq,XPhaseSq[0:len(fSq)])
plt.tight_layout()
plt.savefig('assignment03/results/squarespectrum.png')
plt.show()

# Q4: Windowed FFT
def computeSpectrumWindowed(x,sample_rate_Hz,window_type):
    if window_type=="rect":
        fftOfX = np.fft.fft(x) 
    elif window_type=="hann":
        hannX = np.hanning(len(x))*x
        fftOfX = np.fft.fft(hannX)
    else:
        print ("The valid arguments for 'window_type' are 'rect' and 'hann'.")
        return
    XAbs = np.abs(fftOfX)
    XPhase = np.angle(fftOfX)
    XRe = fftOfX.real
    XIm = fftOfX.imag
    f = np.zeros(int(len(fftOfX)/2))
    usefulFreqs = int(len(fftOfX)/2)
    for i in range(usefulFreqs):
        curF = i*sample_rate_Hz/len(fftOfX)
        f[i] = curF
    return f,XAbs,XPhase,XRe,XIm

# make rectangular windowed spectrum
fw1,XAbsw1,XPhasew1,XRew1,XImw1 = computeSpectrumWindowed(squareWave,44100,'rect')
# make hann windowed spectrum
fw2,XAbsw2,XPhasew2,XRew2,XImw2 = computeSpectrumWindowed(squareWave,44100,'hann')

# plot them on the same plot for easy visual comparison
plt.plot(fw1,XAbsw1[0:len(fw1)],c='b', label='Rectangular Windowed')
plt.plot(fw2,XAbsw2[0:len(fw2)],c='r', label='Hann Windowed')
plt.title("Magnitude Spectrums of Windowed Square Wave")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.legend(loc='best')
plt.savefig('assignment03/results/windowed.png')
plt.show()

# Q5: Sine Sweep
# we can do this with the formula for a chirp, when we want frequency = a+bt.
# chirp = sin(2pi(at+0.5bt^2))
time = np.arange(0,5,1/44100)
origFreq = 20
freqSlope = 3996 # if we want to go up to 20000 Hz in 5 seconds, we need a slope of 3996
chirpout = np.sin(2*np.pi*(origFreq*time + 0.5*freqSlope*time*time))

# proof of concept: the FT of this chirp
fsweep,XAbssweep,XPhasesweep,XResweep,XImsweep = computeSpectrum(chirpout,44100)
plt.plot(fsweep,XAbssweep[0:len(fsweep)])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Magnitude Spectrum of Chirp from 20-20000 Hz")
plt.savefig('assignment03/results/chirpFT.png')
plt.show()

