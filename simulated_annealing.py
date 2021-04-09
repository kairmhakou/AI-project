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
from Code import Code
import time
import math
from Car import Car
#global variables
START_TEMPRATURE = 100
END_TEMPRATURE= 10
NUM_ITERATIONS= 25
COOLING_RATE = 0.99

class Simulated_Annealing:
    def __init__(self,solver,Code, Car):
        self.solver = solver
        # self.sortedResPen = self.sort(self.solver.rlist)
        self.timeSpent = 0
        self.deepCount = 0
    
    def hill_climbing_zonder_zones(self):
        #All possible 'assigned car' swaps

        for r in self.solver.rlist:
            for c in self.solver.options[r.id]:
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
        for r in self.solver.rlist:
    
            for c in self.solver.options[r.id]:

                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost = Cost.costToAddR(c,r)
                    if(cost>best):
                        #nextcode = copy.deepcopy(self.solver.curcode)
                        nextcode = Code.formCode(self.solver) 
                        for tempr in c.res:
                            if(r.overlap(tempr.start,tempr.end)):
                                #overlap => r zou moeten worden verwijderd
                                nextcode[0][tempr.id]='x'
                        nextcode[0][r.id]=c.id
                        if(Code.inMemory(nextcode)):
                            continue
                        return c,None,r
            
        #All sensible 'car zone' swaps
        for c in self.solver.cars:          
            for r in c.res:
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    
                    #nextcode = copy.deepcopy(self.solver.curcode)
                    nextcode = Code.formCode(self.solver) 
                    nextcode[1][c.id] = r.zone 
                    for tempr in c.res:
                        if(tempr.zone == r.zone):
                            pass
                        elif(tempr.zone in Car.zoneIDtoADJ[r.zone]):
                            pass
                        else:
                            nextcode[0][tempr.id]='x'
                    if(Code.inMemory(nextcode)):
                        continue
                    return c,r.zone,None
        
        return None,None,None

    def localSearch(self,steepest_descent = 0):

        count = 0
        while(1):
            count += 1
            #pick one of the local search methods
            if(steepest_descent):
                pass#bestc,bestz,bestr,bestCost = self.steepest_descent()
            else:
                bestc,bestz,bestr = self.hill_climbing()


            if(bestz is not None):
                bestc.setZone(bestz)
            elif(bestr is not None):
                if(bestr.getCar(self.solver)):#if currently assigned to a car, remove from list
                    bestr.getCar(self.solver).res.remove(bestr)
                #assign to new car
                bestc.addR(bestr)
            else:
                #reached peak
                return count
    
       
            
    def simulatedAnnealing(self):
       
        saveSolver = copy.deepcopy(self.solver)
        bestSolver = copy.deepcopy(self.solver)
        currCost = Cost.getCost(self.solver.rlist)
        start = time.perf_counter()

        # sortedListP
        # sortedResPen=self.sort(self.solver.rlist)
        # for r in self.sortedResPen:
        #     print(r.P1)

        
        while(1):
            if((time.perf_counter()-start) > self.solver.maxtime):
                    print('~~timeisup~~')
                    break   #return because the time is up
            #select random  zone and assign it to random car 
            t = START_TEMPRATURE
            
            #list for the plot
            tempratureList =[]
            probabilityList = []
            diffTempList =[] #for diff/t values
            tempratureList.append(t)
            probabilityList.append(1)
            minProbability =99999999
            
            coolCounter=0.50
            while t > END_TEMPRATURE:
                if((time.perf_counter()-start) > self.solver.maxtime):
                    print('~~timeisup~~')
                    break   #return because the time is up
                checkBest = self.solver.getBest()
                i =0 
                while(i < NUM_ITERATIONS):
                    if((time.perf_counter()-start) > self.solver.maxtime):
                        print('~~timeisup~~')
                        break   #return because the time is up
                    
                    # for j in range(random.randint(1, len(self.solver.cars))):
                    for _ in range(2):
                        randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                        randomCarIndex = random.randint(0, len(self.solver.cars)-1)
                        if(self.solver.cars[randomCarIndex].zone == randomZoneIndex):
                            continue
                        c1 = self.solver.cars[randomCarIndex]
                        c1.setZone(randomZoneIndex)
                    """
                    @Karim
                    Alle reservatie lijsten van de auto's (c.res) zijn leeg
                    Maar alle reservaties.notAssigned staan op false
                    => elke reservatie zegt dat die al is toegewezen, maar geen enkele reservatie is toegewezen 
                    => local search kan geen verbetering vinden => blijft altijd op zelfde cost hangen
                    

                    aantalResOpAutos = 0
                    for c in self.solver.cars:
                        aantalResOpAutos+=(len(c.res))    
                    print(aantalResOpAutos)
                    aantalResOpAutos = 0
                    for r in self.solver.rlist:
                        aantalResOpAutos+=not(r.notAssigned)
                    print(aantalResOpAutos)     
                    """

                    self.localSearch()
     
                    newCost= Cost.getCost(self.solver.rlist)
                    #print(newCost)
                    #print(newCost, " ",currCost, randomZoneIndex, randomCarIndex)
                    diff = newCost - currCost                    
                    #input(diff)
                    
                    
                    if diff < 0:
                        
                        #print("diff < 0" , newCost , diff, self.solver.getBest())
                        # print("new peak")
                        
                        tempstart = time.perf_counter()
			
                        saveSolver = copy.deepcopy(self.solver)
                        self.timeSpent += time.perf_counter()- tempstart
                        self.deepCount +=1
                        currCost = Cost.getCost(self.solver.rlist)
                        
                        currCost = newCost
                        if(newCost<self.solver.getBest()):
                            # print("new best cost")
                            
                            tempstart = time.perf_counter()
			
 
                            

                            self.timeSpent += time.perf_counter()- tempstart
                            self.deepCount +=1
                            bestCost = currCost
                            self.solver.setBest() #print the setNewBest
                            if(newCost<bestSolver.getBest()):
                                bestSolver = copy.deepcopy(self.solver)
                    else:
                        
                        probability= math.exp(-((diff)/t))
                        #print(probability)
                        if(random.uniform(0,1) < probability):
                            # print("probability" , probability)
                            if(probability<minProbability):
                                minProbability =probability
                            
                            tempstart = time.perf_counter()
                        
                            saveSolver = copy.deepcopy(self.solver)
                            self.timeSpent += time.perf_counter()- tempstart
                            self.deepCount +=1
                            
                            currCost = newCost
                        else:
                            # coolCounter += 0.00001
                            tempstart = time.perf_counter()
                            self.solver = copy.deepcopy(saveSolver)
                            currCost = Cost.getCost(self.solver.rlist)
                            self.timeSpent += time.perf_counter()- tempstart
                            self.deepCount +=1

                    i += 1
                    # checkBest = self.solver.getBest()
                t *= COOLING_RATE
                # t *= coolCounter
                tempratureList.append(t)
                probabilityList.append(minProbability)
                
                print("t" , t ," cost " ,"best:",bestSolver.getBest(),"current",Cost.getCost(self.solver.rlist))
        
        """ plt.figure(1)
        plt.plot( probabilityList, tempratureList, 'bo')
        plt.show()
        
        plt.figure(2)
        plt.plot(probabilityList)
        plt.show() """
        print("timeSpent:",self.timeSpent)
        print("timeSpent:",self.timeSpent)
        print("timeSpent:",self.deepCount)
        return bestSolver.rlist , bestSolver.cars
    def sort(self,array):
        if len(array)<2:
            return array
        
        middle= array[random.randint(0, len(array)-1)].P1
        low , high , same =[], [] ,[]

        for r in array:
            if r.P1>middle:
                high.append(r)
            elif r.P1<middle:
                low.append(r)
            else:
                same.append(r)

        return self.sort(high) + same + self.sort(low)
    
