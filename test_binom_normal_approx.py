#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:05:11 2019

@author: Alexander Aigner
"""

import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np
from math import factorial, sqrt

N = [10, 20, 50]

clrs = ['red', 'green', 'black']
max_val = 0

fig, axs = plt.subplots(4)
for j in range(len(N)):
    n = N[j]

    k = [i for i in range(n+1)]
    x_min = -4
    x_max = n + 4
    
    # binomial distribution
    y = []
    for i in k:
        nPr = factorial(n)
        y.append( nPr / ( factorial(i) * factorial(n-i) ) )
    y_sum = sum(y)
    y = [i/y_sum for i in y]
    
    # normal distribution
    mean = n * .5
    variance = n * .5**2
    x_norm = np.linspace(x_min, x_max, 100)
    y_norm = st.norm.pdf(x_norm, mean, sqrt(variance))
    
    # print B/N distributions
    axs[j].bar(k, y, color='cornflowerblue')
    axs[j].plot(x_norm, y_norm, color=clrs[j])
    axs[j].set_ylabel('B norm. / N (k)')
    axs[j].grid()
    if j != 0:
        axs[j].set_ylim(axs[0].get_ylim())
    elif j == len(N)-1:
        axs[j].set_xlabel('k')
    else:
        max_val = round(max(y_norm)*10)/10
        axs[j].set_ylim( 0, max_val )

    x_std = [(i-mean)/sqrt(variance) for i in x_norm]
    axs[len(N)].plot(x_std, y_norm, color=clrs[j])
    
limits = axs[len(N)-1].get_xlim()
for j in range(len(N)):
    axs[j].set_xlim(limits)
axs[len(N)].set_ylabel('N (k)')
axs[len(N)].grid()
axs[len(N)].set_ylim(0)

fig.tight_layout()
plt.savefig('binomial_normal_pdf.png')
plt.show()