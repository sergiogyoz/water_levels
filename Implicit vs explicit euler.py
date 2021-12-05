import math
import matplotlib.pyplot as plt

def y(t): #closed form solution
    return math.exp(t);

def f(t,y):
    if t==0: #initial conditions
        return 1;
    return y;

#interval splitted
inter=[0,3];
N=[100,50,25,10,5,2];

#methods start
for n in N:    
    h=(inter[1]-inter[0])/n;
    yexp=[0]*(n+1);
    yimp=[0]*(n+1);
    t=[k/n for k in range(n+1)];
    
    yexp[0]=f(0,1);
    yimp[0]=f(0,1);
    
    for k in range(1,n+1):
        yexp[k]=(1+h)*yexp[k-1];
        yimp[k]=(1/(1-h))*yexp[k-1];
    
    plt.plot(t,yexp,label=f"Explicit n={n}");
    #plt.plot(t,yimp,label=f"Implicit n={n}");
    
plt.legend(loc="upper left");




