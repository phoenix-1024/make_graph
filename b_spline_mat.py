import numpy as np
from scipy import interpolate

import matplotlib.pyplot as plt


ctr =np.array( [(0,0),(1,0),(1,1),(2,1)])

def make_spine(x, y, k=2, s=0):
    ''' 
    The function make_spine takes a set of control points and returns a set of points that define a B-spline curve.
    
    '''
    x=ctr[:,0]
    y=ctr[:,1]

    # uncomment both lines for a closed curve
    #x=np.append(x,[x[0]])  
    #y=np.append(y,[y[0]])

    l=len(x)  

    t=np.linspace(0,1,l-2,endpoint=True)
    t=np.append([0,0,0],t)
    t=np.append(t,[1,1,1])

    tck=[t,[x,y],3]
    u3=np.linspace(0,1,(max(l*2,70)),endpoint=True)
    out = interpolate.splev(u3,tck)
    return out

x=ctr[:,0]
y=ctr[:,1]
out = make_spine(x, y)
plt.plot(x,y,'k--',label='Control polygon',marker='o',markerfacecolor='red')
#plt.plot(x,y,'ro',label='Control points only')
plt.plot(out[0],out[1],'b',linewidth=2.0,label='B-spline curve')
plt.legend(loc='best')
plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
plt.title('Cubic B-spline curve evaluation')
plt.show()


 