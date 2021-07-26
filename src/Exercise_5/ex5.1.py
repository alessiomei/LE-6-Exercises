import numpy as np
import matplotlib.pyplot as plt
import random 

N=10**5

n=list(range(1,6))       #slopes of the power law

def I_an(i):             #analytical result of the integral
    i=1/(n[i]+1)
    return i

def f(x,i):              #function to be integrated
    f=x**n[i]
    return f

I_ij=[]                 #matrix i x j where the element I(i,j) is the integral value computed for slope i and with a number of extractions j
for i in range(0, len(n)):
    I_mc=[]
    F=0
    for j in range(0, N):
        x=random.random()
        F+=f(x,i)
        I_mc.append(F/(j+1))
    I_ij.append(I_mc)
I_ij=np.array(I_ij)



y=[30, 50, 100, 300, 500, 1000, 5000, 10000,50000, 90000]       #X axis for the plots
for i in range(0, len(n)):  
    plt.figure()
    plt.plot(y, abs(I_an(i)-I_ij[i,y]), 'ro')
    plt.ylabel('$|I_{analytic}-I_{numerical}|$', fontsize=14)
    plt.xlabel('$Number\ of\ extractions\ N$', fontsize=14)
    plt.title('$f(x)= x^{%g}$'%(n[i]))
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(10**(-4),1)
    plt.xlim(10, N)

N=10**4             #number of extractions to compute the integral
k=100               #number of times I compute the integral numerically

mean_n, std_n, N_n=[], [], []     #mean value, standard deviation and number of extractions to obtain an error of 0.001 
                                  #relative to the integral, as a funct. of slope

for m in range(0,len(n)):
    int_nm=[]
    for i in range(0,k):
        F=0
        for j in range (0,N):
            x=random.random()
            F+=f(x,m)
        int_nm.append(F/N)    
    int_nm=np.array(int_nm)
    mean=np.mean(I_an(m)-int_nm)
    std=np.std(I_an(m)-int_nm)
    mean_n.append(mean)
    std_n.append(std)
    N_n.append(N*(std/0.001)**2)


#print the results as a function of the slope   
print('n \t mean \t sigma \t N(sigma < 1e-3)')
for i in range(0,len(n)):
    print('%g \t %.5f \t %.4f \t %.4f'%(n[i], mean_n[i], std_n[i], N_n[i]))
