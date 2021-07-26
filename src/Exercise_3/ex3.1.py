import numpy as np
import matplotlib.pyplot as plt
import random 
import scipy.stats as stat

N_tot=[100,1000, 5000, 100000]

#circunference definition, condition for random sampling: circ(x,y) <=1
def circ(x,y):
    c= (x)**2+(y)**2
    return c

pi_distr_N=[]
for j in range(0,3):
    pi_distr=[]                         #list that contains 3 different pi distributions, each with N_tot[3] estimates obtained with N_tot[j] extractions
    for i in range(0, N_tot[3]):        #I want to repeat N_tot[3] times the calculation of pi done with N_tot[j] extractions of random numbers.
        n=0                             #counter of random number couples that satisfy the "inside the circle" condition
        for i in range(0, N_tot[j]):        
            n1=random.uniform(-1,1)
            n2=random.uniform(-1,1)
            if circ(n1,n2)<=1:
                n+=1
        pii= 4*(n/N_tot[j])        
        pi_distr.append(pii) 
    pi_distr_N.append(pi_distr)        
pi_distr_N=np.array(pi_distr_N)

mean_j, std_j, k_j=[], [], []   #list containing mean, standard deviation and parameter k for N=( 100, 1000, 5000)
                                #where N is the number of extractions of random numbers

for j in range(0,3):                    #loop to compute  std, mean and k and fill the associated list
    std=np.std(np.pi-pi_distr_N[j])
    mean=np.mean(np.pi-pi_distr_N[j])
    k=std*(np.sqrt(N_tot[j]))
    mean_j.append(mean)
    std_j.append(std)
    k_j.append(k)
mean_j=np.array(mean_j)
std_j=np.array(std_j)
k_j=np.array(k_j)

print('k= %.3f for N_tot= %g'%(k_j[0], N_tot[0]))

#plot of the pi-distribution for N=100 and its best-fit gaussian distribution
domain=np.linspace(-1,1,100)
plt.figure()
plt.plot(domain, stat.norm.pdf(domain, mean_j[0], std_j[0]), color='r')
plt.hist(np.pi-pi_distr_N[0], color='b', bins=30, histtype='step', density=True, stacked=(True)) 
plt.ylabel('$normalized\ counts$', fontsize=14)
plt.xlabel('$\pi-\pi_{MC}$', fontsize=14)
plt.title('$N=100$', fontsize=14)
plt.xticks(np.arange(-1,1.1,0.5), fontsize=10)
plt.yticks(fontsize=10)
props = dict(boxstyle='round', facecolor='lightblue', alpha=0.5)
plt.text(0.6, 2, '$N_{tot}= 10^5 $ \n $\mu = %.5f$ \n $\sigma = %.3f$' %(mean_j[0],std_j[0]), fontsize=10, bbox=props)

#since k is constant, I want to check if I find the relation var= std^2= k^2/N , with N=100,1000,5000.
def iper(x):
    f= k_j[0]/np.sqrt(x)
    return f
  
#plot with the var computed for N=100, 1000, 5000 vs. the theoretical behaviour
t=np.arange(50, N_tot[2]+100, 100)
plt.figure()
plt.plot(N_tot[0], std_j[0], 'bo')
plt.plot(N_tot[1], std_j[1], 'bo')
plt.plot(N_tot[2], std_j[2], 'bo')
plt.plot(t, iper(t), 'k')
plt.ylabel('$Standard\ deviation\ \sigma$', fontsize=14)
plt.xlabel('$Number\ of\ extractions\ N$', fontsize=14)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.ylim(0.02, 0.18, 0.001)
plt.xlim(50, N_tot[2]+100, 100)
