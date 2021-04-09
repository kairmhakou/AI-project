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
        self.timeSpentLS = 0
        self.timeSpentLA = 0
        self.timeSpentPert = 0
        self.timeSpentChoose = 0
    def steepest_descent(self):
        bestc = None
        bestz = None
        bestr = None
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in self.solver.rlist:
            for c in self.solver.options[r.id]:
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
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

                        best = cost
                        bestc = c
                        bestr = r
            
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
                    
                    
                    best = cost
                    bestc = c
                    bestz = r.zone
                    #print(bestc.id,best,bestz)
                    
        return bestc,bestz,bestr
    
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
        tempStart = time.perf_counter()
        count = 0
        while(1):
            count += 1
            #pick one of the local search methods
            if(steepest_descent):
                bestc,bestz,bestr = self.steepest_descent()
            else:
                bestc,bestz,bestr = self.hill_climbing()#is sneller en beter?
            
            if(bestz is not None):
                bestc.setZone(bestz)
            elif(bestr is not None):
                if(bestr.getCar(self.solver)):#if currently assigned to a car, remove from list
                    bestr.getCar(self.solver).res.remove(bestr)
                #assign to new car
                bestc.addR(bestr)
            else:
                #reached peak
                break
            
            #removing the following improves speed decreases result
            if(not(Code.add(self.solver))):
                print("iets fout met nextcode in localSearch")
        self.timeSpentLS += time.perf_counter()-tempStart
        return count
    def leastAssigned(self):
        tempStart = time.perf_counter()
        lowest = 999999999999999
        ret = None        
        for r in self.solver.rlist:
                if(r.assignCount<lowest):
                    for c in self.solver.options[r.id]:
                        nextcode = Code.formCode(self.solver) 
                        
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
                
                        bestc = c
                        bestr = r
                        lowest = r.assignCount
        if(bestr):                
            bestc.setZone(bestr.zone)
            bestc.addR(bestr) 
            Code.add(self.solver)
            print("assigned least popular r",bestr.id,bestr.assignCount)
        else:
            print("problemen in leastAssigned")       
        self.timeSpentLA += time.perf_counter()-tempStart        
        return ret    
    def findSolution(self):
    	#TODO:
    	#ADD rate of change (% improved in 0.x seconds), shake if too low
        sinceLast = time.perf_counter()
        prevBest = 999999999999999
        result = 999999999999999
        resultRlist,resultCars = copy.deepcopy(self.solver.rlist), copy.deepcopy(self.solver.cars)
        bestSolver = copy.deepcopy(self.solver)
        i = 0
        start = time.perf_counter()
        while(1):            
            if((time.perf_counter()-start) > self.solver.maxtime):
                 print('~~timeisup~~')
                 break   #return because the time is up
            if((time.perf_counter()-sinceLast) > 5):#atleast x% better every y seconds
                sinceLast = time.perf_counter()
                print("checkTime",sinceLast,prevBest,bestSolver.getBest())
                if(not((prevBest-bestSolver.getBest())/prevBest)>0):
                    print("too slow")
                    self.leastAssigned()
                    if(Cost.getCost(self.solver.bestrlist)<result): 
                        result = Cost.getCost(self.solver.bestrlist)
                        resultRlist,resultCars = copy.deepcopy(self.solver.bestrlist), copy.deepcopy(self.solver.bestcars)
                    bestSolver= copy.deepcopy(self.solver)
                    self.solver.setBest()
                prevBest = self.solver.getBest()
            i+=1
            count = self.localSearch(0)
            cost = Cost.getCost(self.solver.rlist)
            if(i%100==0):
                print(i,':',cost,count,self.solver.bestCost)
            if(cost<self.solver.bestCost):
                self.solver.setBest()
                foundNewBest = 1
                sinceLast = time.perf_counter()
            if(foundNewBest):
                foundNewBest = 0
                bestSolver = copy.deepcopy(self.solver)
            else:
                self.solver = copy.deepcopy(bestSolver)
                
            
            changed = self.pertubeer()

            if(not(changed)):
                print("No more changes after:",i)   
                self.leastAssigned()
                if(Cost.getCost(self.solver.bestrlist)<result): 
                    result = Cost.getCost(self.solver.bestrlist)
                    resultRlist,resultCars = copy.deepcopy(self.solver.bestrlist), copy.deepcopy(self.solver.bestcars)
                bestSolver= copy.deepcopy(self.solver)
                self.solver.setBest()
        if(Cost.getCost(self.solver.bestrlist)<result): 
                    result = Cost.getCost(self.solver.bestrlist)
                    resultRlist,resultCars = copy.deepcopy(self.solver.bestrlist), copy.deepcopy(self.solver.bestcars)
        
        print("time spent in localSearch:",self.timeSpentLS) #11.36  /  99.62
        print("time spent in leastAssigned:",self.timeSpentLA) #0    /  0.042
        print("time spent in Pertubeer:",self.timeSpentPert) #6.81   /  88.21
        print("     time spent in Choose:",self.timeSpentChoose) #6.81   /  88.21
        return resultRlist,resultCars
    def findPeak(self,start,margin):
        newBest = 0    
        tempstart = time.perf_counter()      
        for i in range(100):   
            i+=1
            # count = self.localSearch(1) #steepest_descent
            count = self.localSearch(0) #hill_climbing
            cost = Cost.getCost(self.solver.rlist)
            if(i%50==0):
                print("\t\t",i,':',cost,count,self.solver.bestCost)
            if(cost<self.solver.bestCost):
                self.solver.setBest()
                newBest = 1
            elif(cost<self.solver.bestCost + margin*self.solver.bestCost):    
                newBest = 2
 
            changed = self.pertubeer()
            
            if(not(changed)):
                print("No more changes after:",i)
                break
        print("time:",time.perf_counter()-tempstart)
        if(newBest == 2):
            print("margin")
        return newBest

    def shake(self,amount):
        tries = 0
        while(1):
            for i in range(random.randint(1, amount+20)): #pas dit aan -> amount ipv amount+1
                randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                randomCarIndex = random.randint(0, len(self.solver.cars)-1)
                        
                c1 = self.solver.cars[randomCarIndex]
                c1.setZone(randomZoneIndex)
                   
            if(Code.add(self.solver)):
                break
            else:
                tries+=1
                if(tries>10):
                    amount+=1
                    print("violant shaking")
                    tries = 0
        
    def move(self,start):
        foundNewBest = 0
        margin = 0.2
        while(1):
            if(self.findPeak(start,margin)): # via local search
                print("go deeper")
                foundNewBest = 1
                margin = 0
            else:
                return foundNewBest

            
    def VariableNeighbourhoud(self):
        start = time.perf_counter()        
        iteration = 0
        noChange = 0
        bestSolver = copy.deepcopy(self.solver)
        
        maxAmount = int(len(self.solver.cars)/1.5)
        amount = int(len(self.solver.cars)/10)
        
        while(1):
            iteration+=1
            print(iteration,":",self.solver.getBest())
            if((time.perf_counter()-start) > self.solver.maxtime):
                print('~~timeisup~~')
                break   #return because the time is up
            
            self.shake(amount)
            foundNewBest = self.move(start)

            if(not(foundNewBest)):
                self.solver = copy.deepcopy(bestSolver)
                print("RESET")
                noChange+=1 # waarvoor gebruik je dit here? Neighbourhood over tijd vergroten, in het begin 1 auto verwisselen van zone, 
                #maar als hij lang vast zit telkens meer auto's tegelijk veranderen van zone
                if(noChange>=10):
                    noChange = 0
                    amount = min(maxAmount,amount+1)
                    print("new amountMin",amount)
            else:
                bestSolver = copy.deepcopy(self.solver)
                amount = 2
                print("RESET AMOUNT",amount)

        print(Cost.getCost(self.solver.bestrlist))
        return self.solver.bestrlist,self.solver.bestcars

    
    def choose(self,r,minL,bestc,bestr):
        tempStart = time.perf_counter()
        for c in self.solver.options[r.id]:
            if(len(c.res)<minL):    
                        nextcode = Code.formCode(self.solver) 
                        
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
                        #break
        #print(time.perf_counter()-tempStart)
        self.timeSpentChoose += time.perf_counter()-tempStart       
        return bestc,bestr,minL
    def pertubeer(self):
        tempStart = time.perf_counter()
        minL = 99999999999
        bestc = None
        bestr = None
        for r in self.solver.rlist:#sorted_rlist
            
            if(r.notAssigned):
                #print(r.id)
                bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
        #input()
        if(bestr is None):
            #print("try adjecent")
            for r in self.solver.rlist:
                if(r.adjZone):
                    bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
            
        if(bestr):                
            bestc.setZone(bestr.zone)
            bestc.addR(bestr)
           
            if(not(Code.add(self.solver))):
                print("iets fout met nextcode in forceAssign")
            #print(" Forced assign")    
            self.timeSpentPert += time.perf_counter()-tempStart       
            return 1
        else:    
            print("No Forced assign")
            self.timeSpentPert += time.perf_counter()-tempStart                   
            return 0
