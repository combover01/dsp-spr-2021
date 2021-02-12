import numpy as np
from scipy.io import wavfile
import scipy.io as sp
import scipy.signal as spsig
import matplotlib.pyplot as plt
import time


x = np.ones(200)
h = np.concatenate((np.arange(0,25)/25, np.arange(25,0,-1)/25 ))
h = np.append(h,0)


#If the length of 'x' is 200 and the length of 'h' is 100, length of 'y' = 299
def myTimeConv(x,h):
    y = np.zeros(len(x) + len(h) - 1)
    h = np.flip(h) 

    lenX = len(x)
    lenH = len(h)
    shortest = min(lenX,lenH)
    longest = max(lenX,lenH)    
    

    for t in range(len(y)):
        if t<longest:
            curRange = min(t+1,shortest)
        else:
            curRange = shortest-(t+1-longest)

        xStart = max(0,t-lenH+1)
        xEnd = xStart + curRange
        hStart = max(lenH-1-t,0)
        hEnd = hStart+curRange

        y[t] = np.sum(x[xStart:xEnd]*h[hStart:hEnd])
    return y




yy = myTimeConv(x,h)
plt.plot(yy)
plt.title("Triangle Convolved with Ones")
plt.xlabel("tau")
plt.ylabel("Amplitude")
plt.savefig('assignment02/results/01-convolution.png')
plt.show()


#(m, mabs, stdev, time) = 
def compareConv(x, h):
    t1 = time.perf_counter()
    myOutput = myTimeConv(x,h)
    t2 = time.perf_counter()
    spOutput = spsig.convolve(x,h)
    t3 = time.perf_counter()
    m = np.sum(myOutput-spOutput) / len(myOutput)
    mabs = np.sum(np.abs(myOutput-spOutput)) / len(myOutput)
    stdev = np.sqrt((np.sum((np.abs(myOutput-spOutput)**2)))/len(myOutput))
    times = np.array([t2-t1,t3-t2]) #index 0 is my convolution, index 1 is scipy's convolution

    return m,mabs,stdev,times


sr, impulseResponse = wavfile.read('assignment02/impulse-response.wav')
sr, piano = wavfile.read('assignment02/piano.wav')

m,mabs,stdev,times = compareConv(impulseResponse,piano)
print(m)
print(mabs)
print(stdev)
print(times)

txtFile = open("assignment02/results/comparison","w")
txtFile.writelines(f'Mean: {m}\nMean Absolute Difference: {mabs} \nStandard Deviation: {stdev} \nTime of my function: {times[0]} \nTime of SciPy convolve: {times[1]}')
txtFile.close()

