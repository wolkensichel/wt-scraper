from scipy.integrate import quad

import matplotlib.pyplot as plt
import scipy.stats
import numpy as np


def normal_distribution_function(x,mean,std):
    value = scipy.stats.norm.pdf(x,mean,std)
    return value

x_min = -5.0
x_max = 5.0

mean = 0.0 
std = 1


ptx = np.linspace(x_min, x_max, 100)
pty = scipy.stats.norm.pdf(ptx,mean,std)

plt.plot(ptx,pty, color='gray')
plt.fill_between(ptx, pty, color='#e1b1b4', alpha='1.0')
plt.grid()

plt.title('How to integrate a function that takes parameteres in python ?', fontsize=10)
plt.xlabel('x', fontsize=8)
plt.ylabel('Probability Density Function', fontsize=8)

res, err = quad(normal_distribution_function, -1.96, 1.96, args=(mean,std,))
print(res)

plt.savefig("integrate_function_takes_parameters.png")
plt.show()
