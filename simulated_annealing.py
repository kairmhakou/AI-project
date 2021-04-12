# -*- coding: utf-8 -*-

"""
Created on Tue Mar 23 22:46:11 2021

@author: dehan
# """
# #%%
# from main import Solver
from Printer import Printer
import random
import copy

import  matplotlib.pyplot as plt
from Cost import Cost
from Code import Code
import time
import math
from Car import Car
from State import State
#global variables
START_TEMPRATURE = 200 #100
END_TEMPRATURE= 0#10 #waarom 10 ipv 0? 
NUM_ITERATIONS= 1000
COOLING_RATE = 0.99 #Moet lichtelijk anders zijn voor elk probleem 

class Simulated_Annealing:
    def __init__(self,maxtime):
        self.maxtime = maxtime
        # self.sortedResPen = self.sort(State.rlist)
    
    def hill_climbing_zonder_zones(self):
        #All possible 'assigned car' swaps

        for r in State.rlist:
            for cid in State.options[r.id]:
                c = State.cars[cid]
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    
                    cost =  Cost.costToAddR(c,r)
                    #print(cost)
                    if(cost>0):#any improvement
                        #print(r.id,":",c.id)
                        return c,None,r
        return None,None,None
    def hill_climbing(self):
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in State.rlist:
            for cid in State.options[r.id]:
                c = State.cars[cid]
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost = Cost.costToAddR(c,r)
                    if(cost>best):
                        return c,None,r
            
        #All sensible 'car zone' swaps
        for c in State.cars:          
            for rid in c.res:
                r = State.rlist[rid]
                cost =  Cost.costToSetZone(c,r.zone)
                if(cost>best):
                    return c,r.zone,None
        
        return None,None,None

    def localSearch(self):
        while(1):
            bestc,bestz,bestr = self.hill_climbing()
            if(bestz is not None):
                bestc.setZone(bestz)
            elif(bestr is not None):
                if(bestr.getCar()):#if currently assigned to a car, remove from list
                    bestr.getCar().res.remove(bestr.id)
                #assign to new car
                bestc.addR(bestr)
            else:
                #reached peak
                return
       
            
    def simulatedAnnealing(self):
        currCost = Cost.getCost(State.rlist)	
        State.setBestResult(currCost)        
        State.backup(currCost)
        
        start = time.perf_counter()
        
        while(1):
            if((time.perf_counter()-start) > self.maxtime):
                    print('~~timeisup~~')
                    break   #return because the time is up
            #select random  zone and assign it to random car 
            t = START_TEMPRATURE
            #list for the plot
            tempratureList =[]
            probabilityList = []
            iterations =[] #for diff/t values
            tempratureList.append(t)
            probabilityList.append(1)
            iterations.append(0)
            minProbability =99999999
            numOfIteration=1
            
            
            while t > END_TEMPRATURE:
                if((time.perf_counter()-start) > self.maxtime):
                    print('~~timeisup~~')
                    break   #return because the time is up
                i =0 
               
                while(i < numOfIteration):
                    if((time.perf_counter()-start) > self.maxtime):
                        print('~~timeisup~~')
                        break   #return because the time is up
                    
                    for _ in range(1):
                        randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                        randomCarIndex = random.randint(0, len(State.cars)-1)
                        if(State.cars[randomCarIndex].zone == randomZoneIndex):
                            continue
                        c1 = State.cars[randomCarIndex]
                        c1.setZone(randomZoneIndex)

                    self.localSearch()
                    newCost= Cost.getCost(State.rlist)
                    diff = newCost - currCost                    
                    
                    if diff < 0:
                        
                        #print("diff < 0" , newCost , diff, State.getBest())
                        # print("new peak")
                        
                        currCost = newCost
                        State.backup(newCost)

                        if(newCost<State.result):
                            # print("new best cost")
                            State.setBestResult(newCost)
                    else:
                        
                        probability= math.exp(-((diff)/t))
                        #print(probability)
                        if(random.uniform(0,1) < probability):
                            # print("probability" , probability)
                            if(probability<minProbability):
                                minProbability =probability
                            
                            State.backup(newCost)
                            currCost = newCost
                        else:
                            # coolCounter += 0.00001
                            State.restore()
                            currCost = Cost.getCost(State.rlist)


                    i += 1
                # Gometric
                # t *= COOLING_RATE 

                #de beste cooling mainer
                # exponential cooling
                t= START_TEMPRATURE * COOLING_RATE**numOfIteration 
                
                # logarithmical cooling
                # t= START_TEMPRATURE/(1 * math.log(numOfIteration+1)) 
                
                # #linear multiplicative  cooling
                # t= START_TEMPRATURE / (1+COOLING_RATE*numOfIteration)

                # Quadratic multiplicative cooling
                # t= START_TEMPRATURE / (1+COOLING_RATE*numOfIteration**2)

                #deze manier 
                # numOfIteration = NUM_ITERATIONS *(1 - t/START_TEMPRATURE) +10
                # numOfIteration= math.ceil(x)
                
                #of deze 
                numOfIteration +=1.2

                print(numOfIteration)
                tempratureList.append(t)
                probabilityList.append(minProbability)
                iterations.append(numOfIteration)
                print(time.perf_counter()-start,"t" , t ," cost " ,"best:",State.result,"current",newCost,"Backup",State.backupCost)
                
        
        # plt.figure(1)
        # plt.plot( probabilityList, tempratureList, 'bo')
        # plt.show()
        # plt.figure(1)
        # plt.plot(tempratureList, iterations)
        # plt.show()
        # plt.figure(2)
        # plt.plot(probabilityList, iterations)
        # plt.show()
        
        return State.resultRlist , State.resultCars
    def sort(self,array):
        if len(array)<2:
            return array
        
        middle = array[random.randint(0, len(array)-1)].P1
        low , high , same =[], [] ,[]

        for r in array:
            if r.P1>middle:
                high.append(r)
            elif r.P1<middle:
                low.append(r)
            else:
                same.append(r)

        return self.sort(high) + same + self.sort(low)
