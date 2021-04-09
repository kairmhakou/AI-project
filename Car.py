# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:26:45 2021

@author: dehan
"""
from State import State
class Car:
    id = 0 
    carIDtoStr = {}
    carStrtoID = {}
    zoneIDtoStr = {}
    zoneStrtoID = {}
    zoneIDtoADJ = []
    def __init__(self,inc = 1):
        self.id = Car.id
        self.res = [] #list of reservations assigned to this car
        self.zone = 0
        
        Car.id += inc
    def clone(self):
        cloneCar = Car(0)
        cloneCar.id = self.id
        cloneCar.res = [x for x in self.res]
        cloneCar.zone = self.zone
        return cloneCar
    def inZone(self,r):
        if(self.zone == r.zone):
            return 1 # car is in the ideal zone for r
        elif(self.zone in Car.zoneIDtoADJ[r.zone]):
            return 2 # car is in adjecent zone for r
        else:
            return 0 # r cannot be assigned to c unless c.zone is changed
    def overlap(self,start,end):
        for rID in self.res:
            print(rID,len(State.rlist))
            r = State.rlist[rID]
            if(r.overlap(start,end)):
                return True
        return False

    def addR(self,nres):
        if(not(nres.zone == self.zone or nres.zone in Car.zoneIDtoADJ[self.zone])):
            print("cannot add to car in this zone")
            return 0
        i = 0
        while(i<len(self.res)):
            r = State.rlist[self.res[i]]
            #remove all res that overlap with nres
            if(nres.overlap(r.start,r.end)):
                temprID = self.res.pop(i)
                tempr = State.rlist[temprID]
                #print("removed:",tempr.id)
                tempr.setCar(-1)#None
                tempr.notAssigned = True
                tempr.adjZone =False
                i-=1
            i+=1
        nres.setCar(self.id)#self
        nres.notAssigned = False
        nres.adjZone = nres.zone!=self.zone
        self.res.append(nres.id)
        nres.assignCount+=1
        return 1
    """def setZone_old(self,zone):
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
                r.setCar(-1)#None
                self.res.pop(i)
                i-=1
            i+=1"""
    def setZone(self,zone):
        self.zone= zone
        i = 0
        while(i<len(self.res)):
            r = State.rlist[self.res[i]]
            if(r.zone == zone):
                r.adjZone = False
            elif(r.zone in Car.zoneIDtoADJ[zone]):
                r.adjZone = True
            else:
                #DIT GAAT MOGELIJKS FOUT
                r.adjZone = False
                r.notAssigned = True
                r.setCar(-1)#None
                self.res.pop(i)
                i-=1
            i+=1        
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
