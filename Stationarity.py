import numpy as np
import math
import random
import time
import watlevpy.time_series as wal #base class for time series
from scipy import stats #for stats testing
import matplotlib.pyplot as plt
#--------------Kendall testing
#kdata=wal.TSReader.from_csvfile(csvfile="./data_files/KendalldataNotrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    
#kdata=wal.TSReader.from_csvfile(csvfile="./data_files/KendalldataTrend.csv",headers=True,dateformat="%m/%d/%Y %H:%M");    
#kdata=wal.TSReader.from_csvfile(csvfile="./data_files/myyeardata.csv",headers=True,dateformat="%Y-%m-%d");    

a=[1,2,3,4,5,6];
b=[10,9,8,7,6,5,4,3,2,1];
c=[1,12,13,5,3,4,6,15,16,11,21,23,-1,9,8,2,-11];
d=[2,1,4,3];
e=[1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3];
f=[1,5,9,4,3,58,1,3,5,6,1,84,6,4,4,1,1,3,2,5,1,1];
g=[random.randint(0,9) for i in range(0,10**4)];

def _merge_join(arr,l,m,r):
    s=0;#well ordered minus inversions
    ln=m-l+1; rn=r-m;
    N=ln+rn;
    join=[0]*N;
    i=0; j=0;
    
    ind=0;
    while(ind<N):
        if i>ln-1:
            join[ind]=arr[m+1+j];
            j+=1;
            ind+=1;
        elif j>rn-1:
            join[ind]=arr[l+i];
            i+=1;
            ind+=1;
        elif arr[l+i]<arr[m+1+j]:
            join[ind]=arr[l+i];
            i+=1;
            ind+=1;
            s=s+(rn-j);
        elif arr[l+i]>arr[m+1+j]:
            join[ind]=arr[m+1+j];
            j+=1;
            ind+=1;
            s=s-(ln-i);
        elif arr[l+i]==arr[m+1+j]:
            c=arr[l+i];
            lcount=0;
            rcount=0;
            while(arr[l+i]==c):
                lcount+=1;
                i+=1;
                if i>ln-1:
                    break;
            while(arr[m+1+j]==c):
                rcount+=1;
                j+=1;
                if j>rn-1:
                    break;
            add=(rn-j)*lcount; #add the number of elements above in the right per equal element on the left
            subs=(ln-i)*rcount; #substract analogous for the other side
            s=s+add-subs;
            for _ in range(lcount+rcount):
                join[ind]=c;
                ind+=1;
    return join,s;

def MergeSort(arr,l=0,r=-1, n=-1):
    if r==-1 or n==-1:
        n=len(arr);
        r=n-1;
    if l==r:
        return 0;    
    if l<r:
        m=(l+r)//2;
        ls=MergeSort(arr,l,m,m-l+1);
        rs=MergeSort(arr,m+1,r,r-m);
        
        sort_arr,s_join=_merge_join(arr,l,m,r);
        s=ls+rs+s_join;
        arr[l:r+1]=sort_arr;
        return s;     
    if l>r:
        raise ValueError;
        
def MannKendall(arr):
    """
    One sided Mann-Kendall test returns a p-value and the corresponding Z statistic. 
    Runs in O( n ln(n) ).
    """
    copy=arr[:];
    S=MergeSort(copy);
    n=len(arr);
    
    def count_ties_in_sorted_array(a):
        tp=[];
        i=0;
        while i<len(a):
            counter=0;
            c=a[i];
            while a[i]==c:
                counter+=1;
                i+=1;
                if not i<len(a):
                    break;
            if counter>1:
                tp.append(counter);
        return tp;
    tp=count_ties_in_sorted_array(copy);
    
    VarS=n*(n-1)*(2*n+5);
    for k in tp:
        VarS=VarS-k*(k-1)*(2*k+5);
    VarS=VarS/18;
    
    Z=0;
    #continuity correction
    if S>0:
        Z=(S-1)/math.sqrt(VarS);
    elif S<0:
        Z=(S+1)/math.sqrt(VarS);
    elif S==0:
        Z=0;
    p_val=stats.norm.sf(abs(Z));
    return p_val,Z;

def bruteforce(arr):
    n=len(arr);
    s=0;
    for i in range(0,n-1):
        for j in range(i+1,n):
            s=s+np.sign(arr[j]-arr[i]);
    return(s);

quo=[];
aver=[];
test_arr=[];
for i in range(5):
    quo.append([]);
    print(i);
    for j in range(100):
        g=[random.randint(0,9) for i in range(0,10**(i))];
        test_arr=g[:];
        
        t0=time.perf_counter();
        t=list(range(len(test_arr)));
        Z2, p2= stats.kendalltau(t, test_arr);
        t2=time.perf_counter()-t0;
        #--------------------
        t0=time.perf_counter();
        p1,Z1=MannKendall(test_arr);
        t1=time.perf_counter()-t0;
        
        t0=time.perf_counter();
        y=sorted(test_arr);
        t4=time.perf_counter()-t0;
        
        t0=time.perf_counter();
        MergeSort(test_arr);
        t3=time.perf_counter()-t0;
        
        print(y==test_arr);
        quo[i].append(t1/t2);
    aver.append(sum(quo[i])/10);
plt.plot(aver);