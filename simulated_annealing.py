# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:46:11 2021

@author: dehan
"""
import random
import copy
from Cost import Cost
import time
import math

from Car import Car
#global variables
START_TEMPRATURE = 10000
END_TEMPRATURE= 10
NUM_ITERATIONS= 1000
COOLING_RATE = 0.95

class Simulated_Annealing:
    def __init__(self,solver,Code, Car):
        self.solver = solver
    
    def freeData(self):
        for r in self.solver.rlist:
            r.car = None
            r.notAssigned=True
            r.adjZone=False
        for c in self.solver.cars:
            c.res=[]
    def steepest_descent(self):
        bestc = None
        bestz = None
        bestr = None
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in self.solver.rlist:
            for c in r.options:
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        best = cost
                        bestc = c
                        bestr = r
            
      
        return bestc,bestz,bestr
    
    def hill_climbing(self):
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in self.solver.rlist:
            for c in r.options:
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        return c,None,r
        
        
        return None,None,None

    def localSearch(self,steepest_descent = 0):

        count = 0
        while(1):
            count += 1
            #pick one of the local search methods
            if(steepest_descent):
                bestc,bestz,bestr = self.steepest_descent()
            else:
                bestc,bestz,bestr = self.hill_climbing()
           
            
            if(bestz is not None):
                bestc.setZone(bestz)
            elif(bestr is not None):
                if(bestr.car):#if currently assigned to a car, remove from list
                    bestr.car.res.remove(bestr)
                #assign to new car
                bestc.addR(bestr)
            else:
                #reached peak
                return count
    def start(self,most_strict):
        if(most_strict):
            l = self.solver.sorted_rlist
        else:
            l = self.solver.rlist
        for r in l:
            if(r.notAssigned):
                for c in r.options:
                        if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
                            c.addR(r)
                            break            
            
    def simulatedAnnealing(self):
        
        currReservationList = copy.deepcopy(self.solver.rlist)
        currCarList= copy.deepcopy(self.solver.cars) 
        currCost = Cost.getCost(self.solver.rlist)
        
        #select random  zone and assign it to random car 
        t = START_TEMPRATURE
        start = time.perf_counter()
        while t > END_TEMPRATURE:
            if((time.perf_counter()-start) > self.solver.maxtime):
                print('~~timeisup~~')
                break   #return because the time is up
            
            i =0 
            while(i < NUM_ITERATIONS):
                if((time.perf_counter()-start) > self.solver.maxtime):
                    print('~~timeisup~~')
                    break   #return because the time is up
                randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                randomCarIndex = random.randint(0, len(self.solver.cars)-1)
                randomZoneIndex2 = random.randint(0, len(Car.zoneIDtoADJ)-1)
                randomCarIndex2 = random.randint(0, len(self.solver.cars)-1)
                randomZoneIndex3 = random.randint(0, len(Car.zoneIDtoADJ)-1)
                randomCarIndex3 = random.randint(0, len(self.solver.cars)-1)
                    
                c1 = self.solver.cars[randomCarIndex]
                c1.setZone(randomZoneIndex)
                c2 =  self.solver.cars[randomCarIndex2]
                c2.setZone(randomZoneIndex2)
                c3 =  self.solver.cars[randomCarIndex3]
                c3.setZone(randomZoneIndex3)
                
                self.localSearch(0)
                newCost= Cost.getCost(self.solver.rlist)
                # print(newCost, " ",currCost, randomZoneIndex, randomCarIndex)
                diff = newCost - currCost
                if diff < 0:
                    #print("diff < 0" , newCost , diff, self.solver.getBest())
                    currReservationList = copy.deepcopy(self.solver.rlist)
                    currCarList= copy.deepcopy(self.solver.cars) 
                    currCost = Cost.getCost(self.solver.rlist)
                    if(currCost<self.solver.getBest()):
                        self.solver.setBest()
                else:
                    probability= math.exp(-abs(diff/t))
                    if(random.uniform(0,1) < probability):
                        # print("probability" , probability)
                        currReservationList = copy.deepcopy(self.solver.rlist)
                        currCarList= copy.deepcopy(self.solver.cars) 
                        currCost = Cost.getCost(self.solver.rlist)
                
                    else:
                        self.rlist =copy.deepcopy(currReservationList) 
                        self.cars =copy.deepcopy(currCarList)
                i += 1
            t = t * COOLING_RATE
            print("t" , t ," cost " ,Cost.getCost(self.solver.rlist) , self.solver.getBest())
        return 1 