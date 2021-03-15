# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:26:45 2021

@author: dehan
"""

class Car:
    id = 0 
    carIDtoStr = {}
    carStrtoID = {}
    zoneIDtoStr = {}
    zoneStrtoID = {}
    zoneIDtoADJ = []
    def __init__(self):
        self.id = Car.id
        Car.id += 1
    
        self.res = [] #list of reservations assigned to this car
        self.zone = 0
        
    def overlap(self,start,end):
        for r in self.res:
            if(r.overlap(start,end)):
                return True
        return False
    
    def swap(self,c2,r):
        #https://stackoverflow.com/questions/1835756/using-try-vs-if-in-python#:~:text=As%20far%20as%20the%20performance,than%20using%20if%20statement%20everytime.&text=As%20a%20general%20rule%20of,handling%20stuff%20to%20control%20flow.
        #As far as the performance is concerned, using try block for code that normally doesn’t raise exceptions is faster than using if statement everytime.
        try:
            self.res.remove(r)
            c2.res.append(r)
            if(c2.zone==r.zone):
                r.adjZone=0
            else:
                r.adjZone=1
        except:
            print("Error: swap failed")


    def costToAddr(self,nres):
        cost = nres.cost()-(self.zone!=nres.zone)*nres.P2
 
        #print("add:",nres.id,'to car',self.id,cost,end =",")
        for r in self.res:
            #print(nres.id,r.id)
            #print(nres.start,nres.end,r.start,r.end)
            if(nres.overlap(r.start,r.end)):
                #overlap => r zou moeten worden verwijderd
                cost -= (r.P1-r.cost())
        #print("->",cost)
        return cost
    def addr(self,nres):
        i = 0
        while(i<len(self.res)):
            r = self.res[i]
            if(nres.overlap(r.start,r.end)):
                tempr = self.res.pop(i)
                #print("removed:",tempr.id)
                tempr.car = None
                tempr.notAssigned = True
                tempr.adjZone =False
                i-=1
            i+=1
        nres.car = self
        nres.notAssigned = False
        nres.adjZone = nres.zone!=self.zone
        self.res.append(nres)
    
    def costToSetZ(self,zone):
        cost = 0
        for r in self.res:
            cost += r.costNewZone(zone)
        return cost
    def setZone(self,zone):
        self.zone= zone
        i = 0
        while(i<len(self.res)):
            r = self.res[i]
            if(r.zone == zone):
                r.adjZone = False
            elif(r.zone in Car.zoneIDtoADJ[zone]):
                r.adjZone = True
            else:
                #DIT GAAT MOGELIJKS FOUT
                r.adjZone = False
                r.notAssigned = True
                r.car = None
                self.res.pop(i)
                i-=1
            i+=1
            
    def changeCode(self,bestr,code):  
        zone = bestr.zone
        code[0][bestr.id] = self.id
        code[1][self.id] = zone
        i = 0
        while(i<len(self.res)):
            r = self.res[i]

            if(r.zone == zone):
                pass #was adj is now ==zone => no code change
            elif(r.zone in Car.zoneIDtoADJ[zone]):
                pass #was ==zone now adj => no code change
            else:
                code[0][r.id] = 'x' #r now no longer assigned
            i+=1
        
        nres = bestr
        i = 0
        while(i<len(self.res)):
            r = self.res[i]
            if(r.id == bestr.id):
                i+=1
                continue
            if(nres.overlap(r.start,r.end)):
                code[0][r.id] = 'x'
            i+=1
        return code
    
    def code(self):
        return self.zone
    def __str__(self):
        s = str(self.id)+" "
        s +=  Car.carIDtoStr[self.id]
        s += " in zone: "+str(Car.zoneIDtoStr[self.zone])
        s += " / reservations: ["
        for r in self.res:
            s+=str(r.id)+','
        s+=']'
        return s