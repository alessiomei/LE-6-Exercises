import numpy as np
import matplotlib.pyplot as plt
import random 

D=list(range(1,9))          #list with the dimesions of the integral

#function to be integrated
def g(x):
    g=np.e**(-x)
    return g

#analytic result of the integral as a function of dimensionality
def I_analytic(D):
    I= (1- (1/np.e))**D
    return I

  
N=[65536, 256**2, 40**3, 16**4, 9**5, 6**6, 5**7, 4**8].  #number of extractions = number of cells


       
#Compute the integral with Monte Carlo integration (hit or miss)
I_mc=[]
for d in range(0, len(D)):
    s=1
    for j in range(0,D[d]):
        I=0
        for i in range(0,N[d]):
            x=random.random()
            h=g(x)
            I+=h
        s=s*I/N[d]
    I_mc.append(s)
I_mc=np.array(I_mc)


#number of counts in mid-point summation per each dimensionality         
def k(d):
    k=round((N[d])**(1./D[d]))
    return k        

#Compute the integral with mid-point summation:
I_mid=[]
for d in range(0, len(D)):
    n = k(d)
    h = 1/(k(d)-1)
    x = np.linspace(0., 1., n)
    I = h * sum(g((x[:n-1] + x[1:])/2))
    I_mid.append(I**D[d])
          
 
#plot of the result for Monte Carlo vs. mid-point integration
D=np.array(D)
plt.figure()
plt.plot(D, abs(I_analytic(D)-I_mc), 'ro', label='$Monte\ Carlo$')
plt.plot(D, abs(I_analytic(D)-I_mid), 'b*', label='$Mid-point$')
plt.ylabel('$|I_{analytic}-I_{numerical}|$', fontsize=14)
plt.xlabel('$Dimensionality$', fontsize=14)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.yscale('log')
plt.legend(loc='lower right')
plt.ylim(10**(-12),10**(-2) )             
