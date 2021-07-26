import numpy as np
import matplotlib.pyplot as plt
from time import process_time
import scipy.stats as stat
from numba import jit

@jit(nopython=True)             #high performance Python compiler
def RNG(seed,m):                #define MCG generator
    n=[np.uint32(seed), np.uint32(seed*m)]
    while n[len(n)-1] != seed:
        h=np.uint32(m*n[len(n)-1])
        n.append(h)
    n.pop()                     #Since the loop appends also the seed after all the sequence, I delete the last item of the list
    return n
    
seed=987654321          #seed
m=663608941             #multiplier
n_bins=100              #number of bins

#compute random numbers through MCG, count the CPU time of the process
t_start=process_time()
x=np.array(RNG(seed,m))
t_stop=process_time()

print("Elapsed CPU time in seconds: %u \n sequence lenght: %u"%(t_stop-t_start, len(x)))  

#compute Chi2 of the distribution with all the entries
hist, bin_edges= np.histogram(x/x.max(), bins=n_bins)
chi2, p_value=stat.chisquare(hist, len(x)/n_bins)

#plot the histogram with all the entries
plt.figure()
plt.hist(x/x.max(), color='orange', bins=n_bins, histtype='step', density=False)
plt.xlim(0, 1)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
plt.ylim(0, 1.6*10**7)
plt.xlabel('Extracted random numbers', fontsize=10)
plt.ylabel('Counts', fontsize=10)
plt.fill_between(np.linspace(0, 1, n_bins), hist, color='orange', alpha=0.2)

print('Chi2=%.2e and p=%.2f for all entries'%(chi2,p_value))

#define distributions with the first 10^3 and 10^6 elements
rng_1 = x[:10**3]
rng_2 = x[:10**6]

#compute the Chi2 of the distributions with 10^3 and 10^6 entries
hist1, bin_edges1= np.histogram(rng_1, bins=n_bins)
hist2, bin_edges2= np.histogram(rng_2, bins=n_bins)
chi2_1, p_val_1= stat.chisquare(hist1, len(rng_1)/n_bins)
chi2_2, p_val_2= stat.chisquare(hist2, len(rng_2)/n_bins)

#plot the distribution with 10^3 entries
plt.figure()
plt.hist(rng_1, color='purple', bins=n_bins, histtype='step', density=False)
plt.xlim(0, 1)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
plt.xlabel('Extracted random numbers', fontsize=10)
plt.ylabel('Counts', fontsize=10)
plt.fill_between(np.linspace(0, 1, n_bins), hist1, color='purple', alpha=0.2)


print('Chi2=%.2f and p=%.2f for 1000 entries'%(chi2_1,p_val_1))

#plot the distribution with 10^6 entries
plt.figure()
plt.hist(rng_2, color='blue', bins=n_bins, histtype='step', density=False)
plt.xlim(0, 1)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
plt.ylim(0, 1.2*10**4)
plt.xlabel('Extracted random numbers', fontsize=10)
plt.ylabel('Counts', fontsize=10)
plt.fill_between(np.linspace(0, 1, n_bins), hist2, color='blue', alpha=0.2)

print('Chi2=%.2f and p=%.2f for 1000000 entries'%(chi2_2,p_val_2))
