# testing dictionaries in python
import datetime

class Stuff:
    def __init__(self, integ, flot):
        self.i=integ;
        self.f=flot;
    def __str__(self):
        return f"{self.i}-{self.f}";
    def __repr__(self):
        return f"{self.i}-{self.f}";
        

class ComplexStuff:
    
    def __init__(self, arrayofstuff, arrayofint):
        
        n=len(arrayofstuff);
        self.ref=dict(zip(arrayofstuff,range(n)));
        self.stuffs=arrayofstuff;
        self.ints=arrayofint;
        

#raise Exception("Halting the program");

ituf=[1,5,6,7,4,9,8,2];
ftuf=[1.1,5.5,6.6,7.7,4.4,9.9,8.8,2.2];
intis=[8,7,6,5,4,3,2,1]


x=datetime.date(1999,1,1);
y=datetime.date(1999,1,2);
delta=y-x

#x=dict(zip(ituf,ftuf));
#x[3];

#x=ComplexStuff([Stuff(ituf[i],ftuf[i]) for i in range(8)], intis);

#key=Stuff(6,6.6);
#x.stuffs[3]=100;
#x.ref[key];
