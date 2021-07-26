import numpy as np
import random 
from time import process_time


#circle x polar coordinate
def x_circle(r1,r2):
    x= np.sqrt(r1)*np.cos(2*np.pi*r2)
    return x

#circle y polar coordinate
def y_circle(r1,r2):
    x= np.sqrt(r1)*np.sin(2*np.pi*r2)
    return x

#circunference definition, condition for random sampling inside the circle: x^2+y^2<=1
def circ(x,y):
    c= (x)**2+(y)**2
    return c

#square x coordinate for sampling with rejection method
def x_square(r1):
    x=-1+2*r1
    return x

#square y coordinate for sampling with rejection method
def y_square(r2):
    y=-1+2*r2
    return y
 
N=10**6             #number of sampled couples

#sampling with inversion/analytical method, computing the CPU time
x1, y1 = [],[]               #coordinates of the points inside the circle
t1_start=process_time()
while len(x1) < N:        
    r1=random.random()
    r2=random.random()
    x1.append(x_circle(r1,r2))
    y1.append(y_circle(r1,r2))
t1_stop=process_time()
print('time to sample the circle with inversion method: %g s' %(t1_stop-t1_start))


#sampling with rejection method, computing the CPU time
x2, y2 = [],[]                   #coordinates of the points inside the circle
t2_start=process_time()
while len(x2) < N:        
    r1=random.random()
    r2=random.random()
    if circ(x_square(r1),y_square(r2))<=1:
        x2.append(x_square(r1))
        y2.append(y_square(r2))
t2_stop=process_time()
print('time to sample the circle with rejection method: %g s' %(t2_stop-t2_start))
