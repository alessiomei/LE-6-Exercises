import numpy as np
import matplotlib.pyplot as plt
import random 
import scipy.stats as stat
from scipy.optimize import curve_fit
import scipy

U=88.01 #Pb K-shell binding energy [keV]
E_g=1.*10**3 #gamma-ray energy before photo-electric effect [keV]
E_e= (E_g-U)*1.609*(10**(-16)) #photo-electron energy after photo-electric effect [J=kg*m^2/s^2]
c = 3*10**8 #speed of light [m/s]
m_e=9.109*10**(-31)   # electron mass [kg]
beta= (np.sqrt(E_e*(E_e+2*m_e*c**2)))/(E_e+m_e*c**2) # ~0.93
gamma= 1+ E_e/(m_e*c**2)                             # ~2.79

#differential cross section from Sauter's formula
def sigma(x, gamma, beta, norm):                              #x=cos(theta)
    s= norm*((1-x**2)/(1-beta*x)**4)*(1+gamma*(gamma-1)*(gamma-2)*(1-beta*x)/2)
    return s


N=10**6                                     #number of Monte Carlo entries
n_bins=5000                                 #number of bins
x=np.linspace(-1,1, n_bins)

sigma_max=sigma(x, gamma, beta, 1).max()    #diff. cross section max
rect_max=900                                #y-axis of the rectangle

#compute the efficiecy of rejection sampling
rectangle_area=2*rect_max
sigma_int_value, sigma_int_error=scipy.integrate.quad(sigma, -1, 1, args=(gamma, beta, 1))
efficiency= sigma_int_value*100/rectangle_area

#plot the function and the uniform distribution for rejection method
plt.figure()
plt.plot(x,np.zeros(n_bins)+(rect_max), 'b')
plt.plot(x, sigma(x, gamma, beta, 1), 'r')
plt.axvline(x=1, ymax= rect_max/1000, color='b')
plt.ylim(0, 10**3)
plt.xlim(-1, 1.05)
plt.xlabel('$\\cos{\\theta}$', fontsize=10)
plt.ylabel('$\\frac{d \\sigma}{d \\Omega}$', fontsize=14)
plt.fill_between(x,np.zeros(n_bins)+(rect_max), sigma(x, gamma, beta, 1), color='lightblue', alpha=0.2)
plt.fill_between(x, sigma(x, gamma, beta, 1), color='orange', alpha=0.2)
props = dict(boxstyle='square', facecolor='lightblue', alpha=0.5)
plt.text(-0.3,500, 'Efficiency $\simeq$ %.2f %%'%(efficiency),fontsize=10, bbox=props)

#sample cos(theta) with acceptance criterion and phi from Sauter's formula
cos_theta, phi =[], []

for i in range(0,N):
    n=random.uniform(-1,1)   
    m=random.uniform(0,900)
    j=random.uniform(0, 2*np.pi)
    if m <= sigma(n, gamma, beta, 1):  
        cos_theta.append(n)
    phi.append(j)
cos_theta=np.array(cos_theta)
phi=np.array(phi)

#create cos(theta) histogram 
hist, bin_edges=np.histogram(cos_theta, bins=n_bins, density=False)

#fit cos(theta) histogram with Sauter's formula
fit, cov=curve_fit(sigma, xdata=x, ydata=hist,p0=(gamma, beta, 1))
gamma_fit, beta_fit, norm_fit = fit 
gamma_err, beta_err, norm_err = np.sqrt(np.diag(cov)[0]), np.sqrt(np.diag(cov)[1]), np.sqrt(np.diag(cov)[2])

#plot cos(theta) histogram and best fit curve
plt.figure()      
plt.hist(cos_theta,color='orange', bins=n_bins, histtype='step', density=False)
plt.plot(x, sigma(x, gamma_fit, beta_fit, norm_fit), 'k')
plt.xlim(-1, 1.05)
plt.xlabel('$\\cos{\\theta}$', fontsize=10)
plt.ylabel('$Counts$', fontsize=10)
props = dict(boxstyle='round', facecolor='orange', alpha=0.5)
plt.text(-0.75, 150, '$N_{entries}= %u$ \n$ N_{bins}= %g$ \n $\gamma= %.3f \pm %.3f$\n $\\beta$ = %.3f $\pm$ %.3f\n $Normalization = %.3f \pm %.3f$' %(N, n_bins, gamma_fit, gamma_err, beta_fit, beta_err, norm_fit, norm_err), fontsize=10, bbox=props)


#plot phi histogram
plt.figure()
plt.hist(phi, color='green', bins=200, histtype='step', density=False)
plt.xlim(0, 2*np.pi)
plt.ylim(0, 6000)
plt.xlabel('$\\phi$', fontsize=10)
plt.ylabel('Counts', fontsize=10)
d1,d2=np.histogram(phi, bins=200, density=False)
plt.fill_between(np.linspace(0, 2*np.pi, 200), d1, color='g', alpha=0.2)


#coordinates for photon travelling along (0,0,1) (z-axis)
phi=np.random.uniform(0,2*np.pi, len(cos_theta))    #I have to re-define phi since the ones I sampled before are too many
sin_theta= np.sqrt(1-cos_theta**2)
cos_phi=np.cos(phi)
sin_phi=np.sin(phi)

coordinates_1=[sin_theta*cos_phi, sin_theta*sin_phi, cos_theta]   #spherical coordinates
coordinates_1=np.array(coordinates_1)


#3D plot with density colormap for photon along z-axis
fig=plt.figure()
ax= plt.axes(projection='3d')
xyz_1 = np.vstack([coordinates_1[0,:], coordinates_1[1,:] , coordinates_1[2,:]])
density = stat.gaussian_kde(xyz_1)(xyz_1)
ax.scatter(coordinates_1[0,:], coordinates_1[1,:] , coordinates_1[2,:], c=density, cmap='magma', s=10)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#define rotation matrix
def R(theta, phi):
     r=np.matrix([[np.cos(theta)*np.cos(phi), -np.sin(theta), np.sin(theta)*np.cos(phi)],
                 [np.sin(phi)*np.cos(theta), np.cos(phi), np.sin(theta)*np.sin(phi)],
                 [-np.sin(theta), 0 , np.cos(theta)]])
     r=r.reshape((3,3))
     return r


#apply the rotation matrix to the old coordinates, now photon traverls along (0,1,0) (y-axis)
#Since in this code the z-axis versor is a row vector, I have to use the transpose rotation matrix
coordinates_2=np.zeros((3,len(phi)))
for j in range(0, len(phi)):
  coordinates_2[:,j]= coordinates_2[:,j]+np.array(coordinates_1[:,j]*np.matrix.transpose(R(np.pi/2, np.pi/2)))

#3D plot with density colormap for photon along y-axis
fig=plt.figure()
ax= plt.axes(projection='3d')
xyz = np.vstack([coordinates_2[0,:], coordinates_2[1,:] , coordinates_2[2,:]])
density = stat.gaussian_kde(xyz)(xyz)
ax.scatter(coordinates_2[0,:], coordinates_2[1,:] ,  coordinates_2[2,:], c= density, cmap='magma', s=10)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
