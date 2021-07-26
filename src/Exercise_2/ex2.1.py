import numpy as np
import matplotlib.pyplot as plt
import random 
import scipy.stats as stat
from scipy.optimize import curve_fit

def p(x,norm):                           #probability density function (PDF) for the small angle Rutherford distribution
    p = (norm*(2*x))/(1+x**2)**2
    return p

def c_inv(t):                            #inverse cumulative pdf c^-1(t)=x 
    c=np.sqrt(t/(1-t))
    return c


N=10**6                             #number of extractions


#random sampling of Rutherford distribution
x=[]
for i in range (0, N):
    n=random.random()           #extract 10^6 random numb. between 0 and 1
    x.append(c_inv(n))
x=np.array(x)                #calculate the inverse of the cumulative in the random point previosly generated
        

#fit histogram with Rutherford ditribution
a=0
b=20
n_bins=1000                         #number of bins

hist, bins=np.histogram(x, bins=n_bins , density=False, range=(a,b))
z=np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)]) #bins center
fit, cov=curve_fit(p, xdata=z, ydata=hist, p0=(10**4))
norm_fit = fit 
norm_err = np.sqrt(np.diag(cov))

#compute chi square
chi2, p_value = stat.chisquare(hist, p(z,norm_fit))
dof=n_bins-1    
chi2_red=chi2/dof   

#plot the rutherford formula histogram and its best fit curve
y=np.linspace(0,100, 10000)
plt.figure()
plt.hist(x, color='orange', bins=n_bins , histtype='step', range=(a,b))
plt.plot(y, p(y, norm_fit), 'k')
plt.xlabel('$x$', fontsize=12)
plt.ylabel('$Counts$', fontsize=12)
plt.yscale('log')
plt.xlim(0, 15, 3)
plt.ylim(1, 3*10**4)
plt.xticks(np.arange(0,16, 3), fontsize=10)
plt.yticks(fontsize=10)
props = dict(boxstyle='round', facecolor='orange', alpha=0.5)
plt.text(7, 5*10**3, '$\\chi^2$/ d.o.f = %.2f / %u = %.2f' %(chi2, dof, chi2_red), fontsize=10, bbox=props)
