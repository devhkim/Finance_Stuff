"""
Created on Thu Oct 26 20:50:14 2017

@author: Devin
"""

""" Simulate interest rate paths by the CIR model """

# import packages
import math
import numpy as np
import pandas as pd
from datetime import datetime

# time measure start
startTime = datetime.now()

# define CIR function for a single path
def cir(r0, K, theta, sigma, T, N):
    dt = T/float(N)
    rates = [r0]
    for i in range(N):
        if rates[-1] >= 0:
            dr = K*(theta-rates[-1])*dt + \
                   sigma*math.sqrt(rates[-1])*np.random.normal()
            rates.append(rates[-1] + dr)
        else:
            dr = K*(theta-rates[-1])*dt + \
                   sigma*math.sqrt(abs(rates[-1]))*np.random.normal()
            rates.append(rates[-1] + dr)
    return range(N+1), rates

# set the variable values
r0 = 0.0313 # current interest rate
K = 0.86 # speed of adjustment
theta = 0.0303 # mean
sigma = 0.012 # standard deviation
T = 1.
N = 360
pathnum = 2000

# range and rates are assigned to x and y (plot axes)
x, y = cir(r0, K, theta, sigma, T, N)

# import plot package
import matplotlib.pyplot as plt

# draw plot for a single path
plt.plot(x,y)
plt.show()

# define loop for multiple paths
listy = list(cir(r0, K, theta, sigma, T, N))

def repeat(times):
    df = pd.DataFrame(listy)
    for i in range(times-1):
        df = df.append(pd.DataFrame(list(cir(r0, K, theta, sigma, T, N))))
    df = pd.DataFrame(df.iloc[1::2])
    return df

# polish the dataframe encompassing all paths
dff = pd.DataFrame(repeat(pathnum))
dff.index = range(pathnum) # change row names into regular index
dff = dff.transpose()

# show a specific number of paths
numberofpath = 10
dff.iloc[:,0:numberofpath].plot(legend = False)
plt.show()

# get the mean value of the paths
dff2 = dff.iloc[[-1]]
dff2['Mean'] = dff2.mean(axis=1)

print("\n","The expected interest rate is","\n", dff2['Mean'])

# end time measure
print("\n", "It took this long: ", datetime.now() - startTime, "\n")
