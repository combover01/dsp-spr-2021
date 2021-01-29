import numpy as np
from scipy.io import wavfile
import scipy.io as sp
import matplotlib.pyplot as plt


def loadSoundFile(filename):
    sr, multiChannel = wavfile.read(filename)
    singleChannel = multiChannel[0:,0] #takes all rows, first column of data to give just the left channel of samples.

    floatArray = singleChannel.astype(np.float) #convert from int to float
    return floatArray


def crossCorr(x,y):
    z = np.correlate(x,y,mode='same')
    return z



def findSnarePosition(snareFileName, drumLoopFileName):
    x = loadSoundFile(snareFileName)
    y = loadSoundFile(drumLoopFileName)
    z = crossCorr(x,y)

    globalMax = np.amax(z) # if the sample is 90% or higher of the global maximum correlation, it is a snare hit and is added to "txtContent"

    txtContent = []
    maxz = len(z)
    for i in range(maxz):
        cur = z[i]
        if cur >= 0.9 * globalMax:
            txtContent.append(i)

    return txtContent

def main():
    x = loadSoundFile('assignment01\snare.wav')
    y = loadSoundFile('assignment01\drum_loop.wav')
    z = crossCorr(x,y)

    plt.figure(figsize=(16,8))
    plt.plot(z)
    plt.title("Cross Correlation of Drum Loop and Snare")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")
    plt.savefig('assignment01/results/01-correlation.png')
    plt.show()

    txtContent = findSnarePosition('assignment01\snare.wav','assignment01\drum_loop.wav')
    txtFile = open("assignment01/results/02-snareLocation.txt","w")
    txtFile.writelines(["%s\n" % samp for samp in txtContent])
    txtFile.close()
main()

