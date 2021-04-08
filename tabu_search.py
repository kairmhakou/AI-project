# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:45:53 2021

@author: dehan
"""
import copy
from Cost import Cost
import time
import random

from Code import Code
from Car import Car

class Tabu_Search:
    def __init__(self,solver):
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
                        nextcode = copy.deepcopy(self.solver.curcode)
                        for tempr in c.res:
                            if(r.overlap(tempr.start,tempr.end)):
                                #overlap => r zou moeten worden verwijderd
                                nextcode[0][tempr.id]='x'
                        nextcode[0][r.id]=c.id
                        if(Code.inMemory(nextcode)):
                            continue

                        best = cost
                        bestc = c
                        bestr = r
            
        #All sensible 'car zone' swaps
        
        for c in self.solver.cars:
            for r in c.res:
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    
                    
                    nextcode = copy.deepcopy(self.solver.curcode)
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
                    
                    
                    best = cost
                    bestc = c
                    bestz = r.zone
                    #print(bestc.id,best,bestz)
                    
        return bestc,bestz,bestr
    
    def hill_climbing(self):
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in self.solver.rlist:
            for c in r.options:
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        nextcode = copy.deepcopy(self.solver.curcode)
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
                    
                    nextcode = copy.deepcopy(self.solver.curcode)
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
            
            #removing the following improves speed decreases result
            code = Code.formCode(self.solver) 
            self.solver.curcode = code
            if(Code.inMemory(code)):
                pass#☻print("iets fout met nextcode in localSearch")
            else:
                Code.add(code)
        
    def findSolution(self):
        i = 0
        start = time.perf_counter()
        while(1):            
            # if((time.perf_counter()-start) > self.solver.maxtime):
            #     print('~~timeisup~~')
            #     break   #return because the time is up
            i+=1
            count = self.localSearch(Cost)
            cost = Cost.getCost(self.solver.rlist)
            if(i%100==0):
                print(i,':',cost,count,self.solver.bestCost)
            if(cost<self.solver.bestCost):
                self.solver.setBest()
                
            changed = self.forceAssign()
            
            if(not(changed)):
                print("No more changes after:",i)
                break
            
    def findPeak(self,start):
        newBest = 0
        #while(1):            
        for i in range(100):   
            # if((time.perf_counter()-start) > self.solver.maxtime):
            #     print('~~timeisup~~')
            #     break   #return because the time is up
            i+=1
            # count = self.localSearch(1) #steepest_descent
            count = self.localSearch() #hill_climbing
            cost = Cost.getCost(self.solver.rlist)
            if(i%50==0):
                print("\t\t",i,':',cost,count,self.solver.bestCost)
            if(cost<self.solver.bestCost):
                self.solver.setBest()
                newBest = 1
                
            changed = self.forceAssign()
            
            if(not(changed)):
                print("No more changes after:",i)
                break
        return newBest
    def findSolution2(self):
        iteration = 0
        sinceLast = 0

        maxAmount = int(len(self.solver.cars)/1.5)
        amount = int(len(self.solver.cars)/10)
        start = time.perf_counter()
        backupSolver = copy.deepcopy(self.solver)
        
        bestrlist = self.solver.rlist
        bestcars = self.solver.cars
        
        code = Code.formCode(self.solver)
        self.solver.curcode = code
        if(not(Code.inMemory(code))):
            Code.add(code)
        while(1):
            iteration+=1
            print(iteration,":",self.solver.getBest())
            if((time.perf_counter()-start) > self.solver.maxtime):
                print('~~timeisup~~')
                self.solver = copy.deepcopy(backupSolver)
                break   #return because the time is up
            while(1):
                for i in range(random.randint(1, amount+20)): #pas dit aan -> amount ipv amount+1
                    randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                    randomCarIndex = random.randint(0, len(self.solver.cars)-1)
                        
                    c1 = self.solver.cars[randomCarIndex]
                    c1.setZone(randomZoneIndex)
                code = Code.formCode(self.solver)
                if(not(Code.inMemory(code))):
                    Code.add(code)
                    self.solver.curcode = code
                    break

            
                    
            code = Code.formCode(self.solver)
            self.solver.curcode = code
            if(not(Code.inMemory(code))):
                Code.add(code)
                   
            newBest = 0
            while(1):
                if(self.findPeak(start)): # here lead us to local search
                    newBest = 1
                else:
                    break
                print("go deeper")
            
            if(not(newBest)):
                self.solver.rlist = self.solver.bestrlist
                self.solver.cars = self.solver.bestcars
                bestrlist = self.solver.bestrlist
                bestcars = self.solver.bestcars
                self.solver = copy.deepcopy(backupSolver)
                
                sinceLast+=1 # waarvoor gebruik je dit here?
                if(sinceLast>=10):
                    sinceLast = 0
                    amount = min(maxAmount,amount+1)
                    print("new amountMin",amount)
            else:
                backupSolver = copy.deepcopy(self.solver)

                amount = 2
                print("new amountMax",amount)

        print(Cost.getCost(self.solver.bestrlist))
        return bestrlist, bestcars
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