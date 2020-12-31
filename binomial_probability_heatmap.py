#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 14:28:17 2019

@author: Alexander Aigner
"""

import math
import matplotlib.pyplot as plt
import numpy as np

num_trys = 30

n = [x for x in range(num_trys+1)]
k = n

results = [[0 for x in range(num_trys+1)] for y in range(num_trys+1)]
clear = [[0 for x in range(num_trys+1)] for y in range(num_trys+1)]

for x in n:
    for y in k:
        if y > x:
            clear[y][x] = 1
        else:
            npr = math.factorial(x)/math.factorial(x-y)
            ncr = npr/math.factorial(y)
            results[y][x] = ncr * .5**x
        

levels = [10**(x) for x in [-5, -4, -3, -2]]
levels += [.05*x for x in range(1,11)]
cmap = plt.cm.get_cmap("coolwarm")
origin = 'lower'

fig, ax = plt.subplots(figsize=(7,6))
ax.pcolormesh(n, k, clear, color='k', cmap=cmap, lw=.1)
ax.contourf(n, k, results, levels, cmap=cmap, extend='min', alpha=.85)
#plt.grid()
cp = ax.contour(n, k, results, levels, colors='k', linewidths=(.5,))
ax.clabel(cp, fmt='%1.5f', colors='k', fontsize=8)
plt.plot([0,num_trys-1], [1,num_trys], color='k', lw=3)
plt.plot([0,num_trys], [0,num_trys/2], color='dimgrey', lw=2)
plt.title('Binomial distribution for probability of occurrence 0.5')
plt.xlabel('n')
plt.ylabel('k')
plt.savefig('binomial_dist.png')
plt.close()
#plt.show()