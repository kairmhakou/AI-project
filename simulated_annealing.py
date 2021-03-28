# -*- coding: utf-8 -*-

"""
Created on Tue Mar 23 22:46:11 2021

@author: dehan
# """
# #%%
# from main import Solver
import random
import copy

import  matplotlib.pyplot as plt
from Cost import Cost
import time
import math
from Car import Car
#global variables
START_TEMPRATURE = 100000
END_TEMPRATURE= 10
NUM_ITERATIONS= 10000
COOLING_RATE = 0.99

class Simulated_Annealing:
    def __init__(self,solver,Code, Car):
        self.solver = solver
    
    
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
            
        for c in self.solver.cars:
            for r in c.res:
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    best = cost
                    bestc = c
                    bestz = r.zone
        return bestc,bestz,bestr, best
    
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
                bestc,bestz,bestr,bestCost = self.steepest_descent()
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
        
        #list for the plot
        tempratureList =[]
        probabilityList = []
        diffTempList =[] #for diff/t values
        tempratureList.append(t)
        probabilityList.append(1)
        minProbability =99999999
        
        start = time.perf_counter()
        while t > END_TEMPRATURE:
            # if((time.perf_counter()-start) > self.solver.maxtime):
            #     print('~~timeisup~~')
            #     break   #return because the time is up
            checkBest = self.solver.getBest()
            i =0 
            while(i < NUM_ITERATIONS):
                # if((time.perf_counter()-start) > self.solver.maxtime):
                #     print('~~timeisup~~')
                #     break   #return because the time is up
                
                for j in range(1):
                    randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                    randomCarIndex = random.randint(0, len(self.solver.cars)-1)
                        
                    c1 = self.solver.cars[randomCarIndex]
                    c1.setZone(randomZoneIndex)
                
                self.localSearch(1)
                newCost= Cost.getCost(self.solver.rlist)
                # print(newCost, " ",currCost, randomZoneIndex, randomCarIndex)
                diff = newCost - currCost
                
                if diff < 0:
                    #print("diff < 0" , newCost , diff, self.solver.getBest())
                    currReservationList = copy.deepcopy(self.solver.rlist)
                    currCarList= copy.deepcopy(self.solver.cars) 
                    currCost = Cost.getCost(self.solver.rlist)
                    
                    
                    if(currCost<self.solver.getBest()):
                        bestR = copy.deepcopy(currReservationList)
                        bestC = copy.deepcopy(currCarList)
                        bestCost = currCost
                        self.solver.setBest() #print the setNewBest
                
                else:
                    
                    probability= math.exp(-(diff/t))
                    
                    
                    
                    if(random.uniform(0,1) < probability):
                        # print("probability" , probability)
                        if(probability<minProbability):
                            minProbability =probability
                        currReservationList = copy.deepcopy(self.solver.rlist)
                        currCarList= copy.deepcopy(self.solver.cars) 
                        currCost = Cost.getCost(self.solver.rlist)
                
                    else:
                        self.rlist =copy.deepcopy(currReservationList) 
                        self.cars =copy.deepcopy(currCarList)
                
                if(i == NUM_ITERATIONS/2 and checkBest == bestCost):
                    print("enough")
                    break
                i += 1
                checkBest = self.solver.getBest()
            t = t * COOLING_RATE
            tempratureList.append(t)
            probabilityList.append(minProbability)
            
            print("t" , t ," cost " ,Cost.getCost(self.solver.rlist) , self.solver.getBest())
        
        plt.figure(1)
        plt.plot( probabilityList, tempratureList, 'bo')
        plt.show()
        
        plt.figure(2)
        plt.plot(probabilityList)
        plt.show()
        return bestR , bestC