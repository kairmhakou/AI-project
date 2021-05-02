# -*- coding: utf-8 -*-

"""
Created on Tue Mar 23 22:46:11 2021

@author: dehan
# """
import random
import copy
import time
import math
import matplotlib.pyplot as plt

from Cost import Cost
from Car import Car
from State import State

START_TEMPERATURE = 500 
END_TEMPERATURE= 0

MIN_ITERATIONS = 10#10
MAX_ITERATIONS = 1000#500

#NUM_ITERATIONS= 125
#COOLING_RATE = 0.995

class Simulated_Annealing:
    def __init__(self,maxtime ):
        self.maxtime = maxtime
    
    def hill_climbing(self):
        best = 0 #improvement => >0
        #All possible 'assigned car' swaps
        #   Can only lead to an improvement if r is currently notAssigned or assigned to Adjecent zone
        for r in State.rlist:
            if(r.notAssigned or r.adjZone):
                for cid in State.options[r.id]:
                    c = State.cars[cid]
                    if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                        if(Cost.costToAddR(c,r)>best):
                            return c,None,r
            
        #All possible 'assigned car' swaps assign to adj zone
        #   Can only lead to an improvement if r is currently notAssigned
        for r in State.rlist:
            if(r.notAssigned):
                adjZones = Car.zoneIDtoADJ[r.zone]
                for cid in State.options[r.id]:
                    c = State.cars[cid]
                    for zid in adjZones:         
                        if(Cost.costAddRSetZ(c,r,zid)>best):
                            return c,zid,r  
                          
        #All sensible 'carzone' swaps
        for c in State.cars:          
            for rid in c.res:
                r = State.rlist[rid]
                if(Cost.costToSetZone(c,r.zone)>best):
                    return c,r.zone,None
        #Reached peak
        return None,None,None

    def localSearch(self):
        #Repeat hill_climbing to a local optimum
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
        lenZones = len(Car.zoneIDtoADJ)-1
        lenCars = len(State.cars)-1
        
        currCost = Cost.getCost(State.rlist)	
        State.setBestResult(currCost)        
        State.backup(currCost)
        start = time.perf_counter()
        
        while(1):
            if((time.perf_counter()-start) > self.maxtime):
                    print('~~timeisup~~')
                    break   #return because the time is up

            t = START_TEMPERATURE
            numOfIteration=MIN_ITERATIONS
            minProbability = 1#99999999
            #list for the plot
            temperatureList =[t]
            probabilityList = [minProbability]
            iterations =[numOfIteration] #for diff/t values
            times = [0]

            while t > END_TEMPERATURE:
                if((time.perf_counter()-start) > self.maxtime):
                    break #return because the time is up
                
                i =0 
                while(i < numOfIteration):
                    if((time.perf_counter()-start) > self.maxtime):
                        break #return because the time is up
                    
                    for _ in range(1):
                        randomZoneIndex = random.randint(0, lenZones)
                        randomCarIndex = random.randint(0, lenCars)
                        if(State.cars[randomCarIndex].zone == randomZoneIndex):#Allready in zone
                            continue
                        State.cars[randomCarIndex].setZone(randomZoneIndex)

                    self.localSearch()# Find local optimum
                    
                    newCost= Cost.getCost(State.rlist)
                    diff = newCost - currCost                    
                    if diff < 0:#improvement
                        currCost = newCost
                        State.backup(newCost)
                        if(newCost<State.result):
                            State.setBestResult(newCost)
                            
                    else:#worse
                        probability= math.exp(-((diff)/t))
                        # print(probability)
                        if(random.uniform(0,1) < probability): #accept anyway
                            # print("probability" , probability)
                            if(probability<minProbability):
                                minProbability =probability
                            
                            State.backup(newCost)
                            currCost = newCost
                        else:
                            currCost = State.restore() #Go back to previous local peaks

                    i += 1
                #Independant of problem size by using secondspassed/given maxtime
                #   mapped onto math functions https://www.desmos.com/calculator
                secondsPassed = time.perf_counter()-start
                secondsPassedScaled = (secondsPassed/self.maxtime)*300
                
                ##########################################################################
                # 1) Exponential cooling
                #t = 110*(1.01**(-secondsPassedScaled))- 5.4 # y=110\left(1.01^{-x}\right)-5.4
                
                # 2) Logaritmic cooling:
                #t = -44*math.log(0.6*(secondsPassedScaled+1.5),10)+99.5 # y=-44\cdot\log\left(0.6\left(x+1.5\right)\right)+99.5
                
                # 3) Linear cooling:
                t = START_TEMPERATURE + ((END_TEMPERATURE-START_TEMPERATURE)/300)*secondsPassedScaled
                
                # 4) Gometric: ni zeker wat Gometric is maar werkt wel goed
                #t = 0.99**(secondsPassedScaled-460)-4.8 # y=0.99^{x\ -\ 460\ }-4.8
                #   t *= COOLING_RATE 

                # Linear increase of iterations over time
                numOfIteration = MIN_ITERATIONS + ((MAX_ITERATIONS-MIN_ITERATIONS)/300)*secondsPassedScaled
                #y=25+\frac{\left(100-25\right)}{300}x


                #Not (yet) independant of problem size
                # #linear multiplicative  cooling
                # t= startTemperature / (1+coolingRate*numOfIteration)

                # Quadratic multiplicative cooling
                # t= startTemperature / (1+coolingRate*(numOfIteration)**2)
                ##########################################################################
                
                #append to list for matplotlib graph
                temperatureList.append(t)
                probabilityList.append(minProbability)
                iterations.append(numOfIteration)
                times.append(time.perf_counter()-start)
                
                #print progress
                #print(time.perf_counter()-start,numOfIteration,"t" , t ," cost " ,"best:",State.result,"current",newCost,"Backup",State.backupCost)
        
        #Graph x - Time
        """
        plt.plot(times,iterations)
        plt.show()
        plt.plot(times,temperatureList)
        plt.show()
        plt.plot(times, probabilityList)
        plt.show()
        """
        
        return State.resultRlist , State.resultCars

