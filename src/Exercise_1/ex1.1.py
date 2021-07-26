import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stat
from numba import jit

a=7**5      #moltiplier
m=2**31-1   #modulus
n_bins=100  #number of bins

@jit(nopython=True)     #high performance Python compiler
def MINSTD(seed):       #define MINSTD generator
    r= (a*seed) % m
    n=[np.uint32(seed), np.uint32(r)]
    while n[len(n)-1] != seed:
        h=np.uint32((a*n[len(n)-1]) % m)
        n.append(h)
    n.pop()                               #Since the loop appends also the seed after all the sequence, I delete the last item of the list
    return n

#compute normalized random numbers through MINSTD
seed=23353
x=np.array(MINSTD(seed))/(m-1)

#compute Chi2
hist, bin_edges= np.histogram(x, bins=n_bins)
chi2, p_value=stat.chisquare(hist, len(x)/n_bins)

#plot the distribution
plt.figure()
plt.hist(x, color='pink', bins=n_bins, histtype='step', density=False)
plt.xlim(0, 1)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
plt.ylim(0, 2.5*10**7)
plt.xlabel('Extracted random numbers', fontsize=10)
plt.ylabel('Counts', fontsize=10)
plt.fill_between(np.linspace(0, 1, n_bins), hist, color='pink', alpha=0.2)

print('Chi2=%.2e and p=%.2f'%(chi2,p_value))
