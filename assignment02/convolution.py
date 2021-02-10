import numpy as np
from scipy.io import wavfile
import scipy.io as sp
import matplotlib.pyplot as plt
from numpy import random

# x= np.array([1.,2.,3.,4.,5.])
# h = np.array([99.,99.,99.])
x = np.ones(200)
h = np.concatenate((np.arange(0,25)/25, np.arange(25,0,-1)/25 ))
h = np.append(h,0)


#If the length of 'x' is 200 and the length of 'h' is 100, length of 'y' = 299
def myTimeConv(x,h):
    h = np.flip(h) 

    lenX = len(x)
    lenH = len(h)
    newX = np.concatenate((np.zeros(lenH),x))
    newH = np.concatenate((h,np.zeros(lenX)))

    tau = np.arange(0,len(x)+len(h)) #define a list of counting how many values will be calculated
    sumArr = np.empty([len(x) + len(h), len(x) + len(h)]) #define an empty array to hold intermediate values

    for t in tau:
        row = newX*newH
        newH = np.insert(newH,0,0) #inserts a 0 at the beginning of h 
        newH = newH[:-1] #remove the last value of h so that the arrays stay the same size
        sumArr[t,:] = row #place the row of index-multiplied values into a new row in the summing 2d array

    y = np.sum(sumArr,axis=1) #we have a 2d array, now sum the columns (like doing the integral)
    y = y[1:] #remove first value which is 0

    return y




print(myTimeConv(x,h).astype(int))

#next to do for future me:
#In your main script define 'x' as a DC signal of length 200 (constant amplitude of 1) and 'h' as a symmetric triangular signal of length 51 (0 at the first and last sample and 1 in the middle). Add a function call to myTimeConv() in your script to compute 'y_time' as the time-domain convolution of 'x' and 'h' as defined above. Plot the result (label the axes appropriately) and save in the results folder [10]


