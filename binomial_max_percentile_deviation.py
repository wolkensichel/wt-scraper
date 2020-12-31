#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:31:50 2019

@author: wolkensichel
"""

from math import factorial
import numpy as np
from matplotlib import pyplot as plt

dev_max = []
dev_min = []
dev_min2 = []
devs = []
N = np.arange(1001)
for n in N:
    if n % 2 == 0:
        limit = int(n/2)
    else:
        limit = int(1 + (n-1)/2)
        
    nPr = factorial(n)
    
    num_res = 0
    mid_res = 0
    for k in range(limit):
        k_res = nPr / ( factorial(k)*factorial(n-k) )
        num_res += k_res
        if n % 2 == 1 and k == limit-1:
            mid_res = k_res
            
    num_res *= 2
    if n % 2 == 0:
        k_res = nPr / ( factorial(int(n/2)) )**2
        num_res += k_res
        mid_res = k_res
    
    dev_max.append(.5*mid_res/num_res)
    dev_min.append(.5*1/num_res)
    if n != 0:
        dev_min2.append(.5*n/num_res)
    else:
        dev_min2.append(.5)
        
    if n in [1, 5, 10, 25, 50, 100, 200, 400, 1000]:
        devs.append((n,.5*mid_res/num_res))
    
plt.figure()
plt.plot(N[::2], dev_max[::2], lw=1.5)
plt.plot(N[::2], dev_min[::2], lw=1.5, alpha=.75)
plt.plot(N[::2], dev_min2[::2], lw=1.5, alpha=.75)
plt.grid()
plt.title('Max. deviation of percentiles given n observations')
plt.xlabel('n')
plt.ylabel('deviation')
plt.legend(['center column of distribution', 'outermost column of distribution', 'second outermost column of distribution'])
plt.xlim([0,N[-1]])
plt.ylim([0,0.5])
plt.yticks(.025*np.arange(21))
#plt.savefig('binomial_max_percentile_dev.png')
#plt.close()
plt.show()

[print(dev[0], '\t',dev[1]) for dev in devs]