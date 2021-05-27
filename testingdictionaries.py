# testing dictionaries in python

class Stuff:
    def __init__(self, integ, flot):
        self.i=integ;
        self.f=flot;

class ComplexStuff:
    
    def __init__(self, arrayofstuff, arrayofint):
        
        n=len(arrayofstuff);
        self.ref=dict(zip(arrayofstuff,range(n)));
        self.stuffs=arrayofstuff;
        self.ints=arrayofint;
        

ituf=[1,5,6,7,4,9,8,2];
ftuf=[1.1,5.5,6.6,7.7,4.4,9.9,8.8,2.2];

Mystuff=[Stuff(ituf[i],ftuf[i]) for i in range(8)]