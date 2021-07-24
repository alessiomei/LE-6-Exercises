import numpy as np

N=[10**4, 10**5, 10**6]             #number of sum iterations
Xf_N, Xd_N=[], []                   #list with sum values for each N for float and double

#compute the sum for each N
for n in range(0, 3):
    x=np.full(N[n], np.float32(1/N[n]))     #float variable case
    Xf_N.append(sum(np.float32(x)))
    
    y=np.full(N[n], np.float64(1/N[n]))     #double variable case
    Xd_N.append(sum(np.float64(y)))
    
print('N \t float|1-X| \t double|1-X|')
for i in range(0, len(N)):
    print('%g \t %.1e \t %.1e'%(N[i], abs(1.-Xf_N[i]),abs(1-Xd_N[i])))
