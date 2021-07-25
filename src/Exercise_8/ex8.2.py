import numpy as np
import matplotlib.pyplot as plt
import random 

U=88.01                             #K shell binding energy [keV]             

L_energies =[15.86, 15.20, 13.04]   #L shell energies [keV]    
L_occupancy = [2, 2, 4]             #L shell electron occupancies

N=10**5         #number of extractions
n_bins=100      #number of bins

#sample uniformly cos(theta) and phi, sample photons energies according to occupancies
cos_theta, phi = [], []
E1, E2 = [] , []
for i in range(0,N):
    n=random.uniform(-1,1)
    m=random.uniform(0, 2*np.pi)
    cos_theta.append(n)
    phi.append(m)
    E_gamma1=random.choices(L_energies, weights=L_occupancy)
    E_gamma2= U-E_gamma1[0]
    E1.append(E_gamma1)
    E2.append(E_gamma2)
cos_theta, phi = np.array(cos_theta), np.array(phi)
E1, E2 = np.array(E1), np.array(E2)   
    

#plot energy histograms
plt.figure()
plt.hist(E1, color='orange', bins=n_bins, histtype='step', density=False)
plt.hist(E2, color='brown', bins=n_bins, histtype='step', density=False)
plt.xlim(0, 90)
plt.ticklabel_format(axis="y", style="sci", scilimits=(4,4), useMathText=True)
plt.ylim(10**4, 6*10**4)
plt.xlabel('Energy [keV]', fontsize=10)
plt.ylabel('Counts', fontsize=10)



#define photons spherical coordinates after sampling
sin_theta= np.sqrt(1-cos_theta**2)
cos_phi=np.cos(phi)
sin_phi=np.sin(phi)

coordinates=[sin_theta*cos_phi, sin_theta*sin_phi, cos_theta]
coordinates=np.array(coordinates)


#3D plot of photons emission directions
fig=plt.figure()
ax= plt.axes(projection='3d')
ax.scatter(coordinates[0,:], coordinates[1,:] , coordinates[2,:],color='orange', s=0.01)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
