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
#global variables
START_TEMPRATURE = 100
END_TEMPRATURE= 10
NUM_ITERATIONS= 25
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
        # for r in self.sort(self.solver.rlist):
        # for r in self.solver.sorted_rlist:

            for c in r.options:
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        best = cost
                        bestc = c
                        bestr = r
        
        # for r in self.solver.rlist:
            
        #     if(r.notAssigned):
        #         print(r.id)
        # print("cars")
        # for c in self.solver.cars:
        #     if(c.res == None):
        #         print(c.id)


        # for c in self.solver.cars:
        #     for r in c.res:
        #         cost =  Cost.costToSetZone(c,r.zone)
        #         #print("zoneCost:",cost)
        #         if(cost>best):
        #             best = cost
        #             bestc = c
        #             bestz = r.zone
        
        
        # for r in self.solver.rlist:
        #     if(r.notAssigned):
        #         for c in r.options:
        #                 if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
        #                     c.addR(r)
        #                     break

        return bestc ,bestz,bestr, best
    
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
           
            # self.start(0)
            # self.forceAssign()
            if(bestz is not None):
                bestc.setZone(bestz)
            elif(bestr is not None):
                if(self.solver.rlist[bestr.id].car):#if currently assigned to a car, remove from list
                    self.solver.rlist[bestr.id].car.res.remove(self.solver.rlist[bestr.id])
                #assign to new car
                self.solver.cars[bestc.id].addR(self.solver.rlist[bestr.id])
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
                    print("----the start")
                    Printer.printCars(self.solver.cars)
                    tempcars = copy.deepcopy(self.solver.cars)
                    if((time.perf_counter()-start) > self.solver.maxtime):
                        print('~~timeisup~~')
                        break   #return because the time is up
                    
                    # for j in range(random.randint(1, len(self.solver.cars))):
                    while (1):
                        randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                        randomCarIndex = random.randint(0, len(self.solver.cars)-1)
                        if(self.solver.cars[randomCarIndex].zone == randomZoneIndex):
                            continue
                        # c1 = self.solver.cars[randomCarIndex]
                        # c1.setZone(randomZoneIndex)
                        self.solver.cars[randomCarIndex].setZone(randomZoneIndex)
                        break
                    print("car ", randomCarIndex, " zone ",randomZoneIndex )
                    print("--after changing the zone ")
                    Printer.printCars(self.solver.cars)
                    
                    self.localSearch(1)
                    newCost= Cost.getCost(self.solver.rlist)
                    print("--after the local search------- ")
                    Printer.printCars(self.solver.cars)
                    # print(newCost, " ",currCost, randomZoneIndex, randomCarIndex)
                    diff = newCost - currCost
                    
                    if diff < 0:
                        #print("diff < 0" , newCost , diff, self.solver.getBest())
                        # print("new peak")
                        # currReservationList = copy.deepcopy(self.solver.rlist)
                        # currCarList= copy.deepcopy(self.solver.cars) 
                        # currCost = Cost.getCost(self.solver.rlist)
                        
                        
                        if(currCost<self.solver.getBest()):
                            # print("new best cost")
                            bestR = copy.deepcopy(self.solver.rlist)
                            bestC = copy.deepcopy(self.solver.cars)
                            bestCost = currCost
                            self.solver.setBest() #print the setNewBest
                    
                    else:
                        
                        probability= math.exp(-(diff/t))
                        
                        
                        
                        if(random.uniform(0,1) < probability):
                            # print("probability" , probability)
                            if(probability<minProbability):
                                minProbability =probability
                            # currReservationList = copy.deepcopy(self.solver.rlist)
                            # currCarList= copy.deepcopy(self.solver.cars) 
                            # currCost = Cost.getCost(self.solver.rlist)
                    
                        else:
                            # coolCounter += 0.00001
                            # print("---------------current ------")
                            # Printer.printCars(currCarList)
                            # print("---------------selfsolver ------")
                            # Printer.printCars(self.solver.cars)
                            # self.solver.rlist =copy.deepcopy(currReservationList) 
                            # self.solver.cars =copy.deepcopy(currCarList)
                            
                            # print("---------------after ------")
                            # Printer.printCars(self.solver.cars)
                            print("---- before temp")
                            Printer.printCars(self.solver.cars)
                            print("----  temp")
                            Printer.printCars(tempcars)
                            self.solver.cars = copy.deepcopy(tempcars)
                            print("---- after temp")
                            Printer.printCars(self.solver.cars)
                            
                    
                    """ if(i == NUM_ITERATIONS/2 and checkBest == bestCost):
                        self.cars = bestR
                        # break """
                    i += 1
                    # checkBest = self.solver.getBest()
                t *= COOLING_RATE
                # t *= coolCounter
                tempratureList.append(t)
                probabilityList.append(minProbability)
                
                print("t" , t ," cost " ,Cost.getCost(self.solver.rlist) , self.solver.getBest())
        
        """ plt.figure(1)
        plt.plot( probabilityList, tempratureList, 'bo')
        plt.show()
        
        plt.figure(2)
        plt.plot(probabilityList)
        plt.show() """
        return bestR , bestC
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
    def forceAssign(self):
            minL = 99999999999
            bestc = None
            bestr = None

            for r in self.solver.rlist:
                if(r.notAssigned):
                    for c in r.options:
                        if(len(c.res)<minL):
                            nextcode = copy.deepcopy(self.solver.curcode)

                            #addR and setZone will remove conflicts: r not in zone/adjZone, overlap
                            for tempr in c.res:
                                #tempr not in zone/adjZone
                                if(not(tempr.zone == r.zone or tempr.zone in Car.zoneIDtoADJ[r.zone])):
                                    nextcode[0][tempr.id] = 'x' #r can no longer assigned
                                #overlap
                                elif(r.overlap(tempr.start,tempr.end)):
                                    nextcode[0][tempr.id] = 'x'
                            
                            nextcode[0][r.id] = c.id #r would be assign to c (addR)
                            nextcode[1][c.id] = r.zone #c would be placed in r's zone (setZone)
                            if(Code.inMemory(nextcode)):
                                continue

                            minL = len(c.res)
                            bestc = c
                            bestr = r
            if(bestr):                
                bestc.setZone(bestr.zone)
                bestc.addR(bestr)
                code = Code.formCode(self.solver)
                self.solver.curcode = code
                
                if(Code.inMemory(code)):
                    print("iets fout met nextcode in forceAssign")
                else:
                    Code.add(code)
                return 1
            else:    
                print("No Forced assign")
                return 0