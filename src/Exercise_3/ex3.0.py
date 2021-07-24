import numpy as np
import matplotlib.pyplot as plt
import random

#circumference x polar coordinate
def x_circle(r1,r2):
    x= np.sqrt(r1)*np.cos(2*np.pi*r2)
    return x

#circumference y polar coordinate
def y_circle(r1,r2):
    x= np.sqrt(r1)*np.sin(2*np.pi*r2)
    return x

#circunference definition, condition for random sampling: circ(x,y) <=1
def circ(x,y):
    c= (x)**2+(y)**2
    return c

cx, cy = [],[]               #random points defining x and y coordinates of the circumference of radius 1   
sx, sy = [],[]               #random points defining x and y coordinates of the square of side 2

diff= []                 #list with all the differences between real and estimated pi values

N_tot=[100,1000, 5000, 100000] # N_tot[3]: total number of extracted random points inside the square

for i in range(1, N_tot[3]+1):    #loop to extract  N_tot[3] random numbers   
    n1=random.uniform(-1,1)         # extraction of random floats between -1 and 1
    n2=random.uniform(-1,1)
    sx.append(n1)               # the random variables already satisfy the condition of being inside the square
    sy.append(n2)
    if circ(n1,n2)<=1:      #condition to for random n. to be inside the circle
        cx.append(n1)
        cy.append(n2)
    d=np.pi-4*(len(cx)/i)   #for each step i, calculate the difference between real and estimated pi
    diff.append(d)

pi= 4*(len(cx))/(N_tot[3])              #I compute the pi extimate through the area of the circle with N_tot[3] extractions
print('pi value estimated through Monte Carlo with %g extractions: %4f' %(N_tot[3],pi))

#plot of the points inside the square and circle
fig, ax1 = plt.subplots()
circle=plt.Circle((0,0), 1, color='r', fill=False)    
ax1.plot(sx, sy, ',', color='b')
plt.grid()
plt.xlim(-1.1, 1.1, 0.5)
plt.ylim(-1.1, 1.1, 0.5)
ax1.add_patch(circle)

#plot of the difference between expected and estimated pi value vs number of extractions
x=np.arange(0, N_tot[3], 1)
plt.figure()
plt.plot(x, diff, 'k', x, [0]*x, 'r', linestyle='--')
plt.xlabel('$N_{tot}$', fontsize=16)
plt.ylabel('$\pi - \pi_{MC}$', fontsize=16)
plt.title('$Expected\ vs.\ estimated\ \pi\ values$')
plt.xlim(-0.1, N_tot[3], 1)
plt.ylim(-0.2, 0.2, 0.05)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
