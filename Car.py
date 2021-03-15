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
        
    def inZone(self,r):
        if(self.zone == r.zone):
            return 1
        elif(self.zone in Car.zoneIDtoADJ[r.zone]):
            return 2
        else:
            return 0
    def overlap(self,start,end):
        for r in self.res:
            if(r.overlap(start,end)):
                return True
        return False
    

    def addR(self,nres):
        i = 0
        while(i<len(self.res)):
            r = self.res[i]
            #remove all res that overlap with nres
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
            
    """
    Nergens anders gebruiken
    """
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