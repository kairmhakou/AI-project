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
START_TEMPERATURE = 100 #100
END_TEMPERATURE= 0
NUM_ITERATIONS= 25
COOLING_RATE = 0.995#Moet lichtelijk anders zijn voor elk probleem 
"""
@Karim
Een van de paramters moet 'dynamish' zijn/ worden aangepast 
bv 100_5_14_25.csv is vrij klein => localSearch is snel klaar => numIterations worden sneller uitgevoerd dan bij een groot probleem ie. 360_5_71_25.csv
 als het x keer sneller is wordt de temperatuur x keer meer afgekoelt bij kleinere problemen
Ik denk dat de COOLING_RATE afhankelijk moet zijn van hoe lang het duurt om 'numIteration' uit te voeren
    tijd meten kan met startpunt =  time.perf_counter()

"""


class Simulated_Annealing:
    def __init__(self,maxtime ):
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
    def hill_climbing(self, experimental = 1):
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in State.rlist:
            for cid in State.options[r.id]:
                c = State.cars[cid]
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost = Cost.costToAddR(c,r)
                    if(cost>best):
                        return c,None,r
        #All possible 'assigned car' swaps assign to adj zone
        if(experimental):
            for r in State.rlist:
                if(r.notAssigned):
                    adjZones = Car.zoneIDtoADJ[r.zone]
                    for cid in State.options[r.id]:
                        c = State.cars[cid]
                        for zid in adjZones:         
                            cost = Cost.costAddRSetZ(c,r,zid)
                            if(cost>best):
                                return c,zid,r  
                          
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
            if(bestr is not None):
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
        print(len(State.rlist))
        start = time.perf_counter()
        
        while(1):
            if((time.perf_counter()-start) > self.maxtime):
                    print('~~timeisup~~')
                    break   #return because the time is up
            #select random  zone and assign it to random car 
            t = START_TEMPERATURE
            
            
            #list for the plot
            temperatureList =[]
            probabilityList = []
            iterations =[] #for diff/t values
            times = [0]
            temperatureList.append(t)
            probabilityList.append(1)
            iterations.append(0)
            minProbability = 99999999
            numOfIteration=1
            
            
            
            while t > END_TEMPERATURE:
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
                            print("New Best:",newCost,end = "->")
                            State.setBestResult(newCost)
                    else:
                        
                        probability= math.exp(-((diff)/t))
                        # print(probability)
                        if(random.uniform(0,1) < probability):
                            # print("probability" , probability)
                            if(probability<minProbability):
                                minProbability =probability
                            
                            State.backup(newCost)
                            currCost = newCost
                        else:
                            
                            State.restore()
                            currCost = Cost.getCost(State.rlist)


                    i += 1
                #Independant of problem size
                secondsPassed = int((time.perf_counter()-start)/(self.maxtime/150))
                t = 100*(1.03**(-secondsPassed))    #https://www.desmos.com/calculator/3fisjexbvp
                
                    
                # Gometric
                #t *= COOLING_RATE 

                #de beste cooling mainer
                # exponential cooling
                #t= START_TEMPRATURE * COOLING_RATE**numOfIteration 
                
                # logarithmical cooling
                # t= startTemperature/(1 * math.log( numOfIteration+1))
                
                # #linear multiplicative  cooling
                # t= startTemperature / (1+coolingRate*numOfIteration)

                # Quadratic multiplicative cooling
                # t= startTemperature / (1+coolingRate*(numOfIteration)**2)

                #deze manier werkt ni denk ik; verschil in t is te klein om effect te hebben op numOfIteration => t verandert niet => numIt =>...
                # numOfIteration = NUM_ITERATIONS *(1 - t/START_TEMPRATURE) +10
                # numOfIteration= math.ceil(numOfIteration)
                
                #of deze 
                numOfIteration +=1.2

                print(numOfIteration)
                temperatureList.append(t)
                probabilityList.append(minProbability)
                iterations.append(numOfIteration)
                
                times.append(time.perf_counter()-start)
                print(time.perf_counter()-start,"t" , t ," cost " ,"best:",State.result,"current",newCost,"Backup",State.backupCost)
                
        """
        plt.figure(1)
        plt.plot( probabilityList, tempratureList, 'bo')
        plt.show()
        plt.figure(2)
        plt.plot(tempratureList, iterations)
        plt.show()
        plt.figure(3)
        plt.plot(probabilityList, iterations)
        plt.show()
        """
        """
        #Moet in de tijd lijken op de exponentiele daling niet ten opzichte van het aantal iteraties
        plt.figure(4)
        print(tempratureList)
        print(times)
        plt.plot(tempratureList, times)
        plt.show()
        """
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

