import numpy as np
import matplotlib.pyplot as plt
import random 
from scipy.optimize import curve_fit

#pdf for particle tracking 
def p(x,mu,norm):
    f=norm*mu*np.exp(-mu*x)
    return f

#inverse cumulative pdf
def c_inv(x,mu):
    c=-(np.log(x))/(mu)
    return c

N=10**6             #number of entries for Monte Carlo
n_bins=5*10**2           #number of bins

# compute the individual step lengths for process 1 and 2, keep the minimum, count how many times  s1 is the minimum
#Geant4-like sampling
s=[]
counter=0
for i in range(0,N):
    x=random.random()
    y=random.random()
    s_1=c_inv(x,1)
    s_2=c_inv(y,2)
    if s_1 < s_2:
        s.append(s_1)
        counter+=1
    else:
        s.append(s_2)
s=np.array(s) 
   
#fit the histogram with the exponential function used by Penelope for sampling
hist, bin_edges=np.histogram(s, bins=n_bins, density=False)
x=np.linspace(s.min(),s.max(),n_bins)
fit, cov =curve_fit(p, xdata=x, ydata=hist, p0=(3,10000))
mu_fit, norm_fit = fit
mu_err, norm_err =  np.sqrt(np.diag(cov)[0]) , np.sqrt(np.diag(cov)[1])

#plot the results
plt.figure()
plt.hist(s, color='orange', bins=n_bins, histtype='step')
plt.plot(x, p(x,mu_fit, norm_fit), 'k')
plt.xlabel('min($s_1, s_2$)', fontsize=14)
plt.ylabel('$Counts$', fontsize=14)
plt.yscale('log')
plt.xlim(0, 3, 0.5)
plt.xticks(np.arange(0,3.5, 0.5), fontsize=10)
plt.yticks(fontsize=10)
props = dict(boxstyle='round', facecolor='orange', alpha=0.5)
plt.text(2, 10000, '$\mu = %.3f \pm %.3f $' %(mu_fit, mu_err), fontsize=10, bbox=props)

print('probability that s_1 is the minimum: %.2f \n probability that s_2 is the minimum: %.2f' %(counter/N, (N-counter)/N))
