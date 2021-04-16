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
from State import State

class Tabu_Search:
    def initialSolution():
        for r in State.rlist:
            if(r.notAssigned):
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
                            c.addR(r)
                            break   
        for r in State.rlist:                
            if(r.notAssigned):#could not be assigned to any car
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
        for r in State.rlist:                
            if(r.adjZone):#could not be assigned to any car
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.zone ==r.zone)):
                            c.addR(r)
                            break
            if(r.adjZone):#could not be assigned to any car
                for cid in State.options[r.id]:    
                        c = State.cars[cid]           
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
    def __init__(self,solver):
        self.solver = solver
        self.timeSpentLS = 0
        self.countLS = 0

        self.timeSpentLA = 0
        self.timeSpentPert = 0
        self.countPert = 0
        self.timeSpentChoose = 0
        self.countChoose = 0
        self.timeSpent1 = 0
        self.timeSpent2 = 0

        self.timeClimbing = 0
        self.countClimbing = 0

    def steepest_descent(self,best = -999999999999999999):
        bestc = None
        bestz = None
        bestr = None
        #best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in State.rlist:
            for cid in State.options[r.id]:
                c = State.cars[cid]
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        #nextcode = copy.deepcopy(self.solver.curcode)
                        nextcode = Code.formCode() 
                        for temprid in c.res:
                            tempr = State.rlist[temprid]
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
        
        for c in State.cars:
            for rid in c.res:
                r = State.rlist[rid]
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    
                    
                    #nextcode = copy.deepcopy(self.solver.curcode)
                    nextcode = Code.formCode() 
                    nextcode[1][c.id] = r.zone 
                    for temprid in c.res:
                        tempr = State.rlist[temprid]
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
        #print(bestc.id,bestz,bestr.id)  
        print("steepest_descent:",best)
        return bestc,bestz,bestr
    
    def hill_climbing(self):
        tempStart = time.perf_counter()
        best = 0 #verbetering >0
        currCost = Cost.getCost(State.rlist)
        #All possible 'assigned car' swaps
        for r in State.rlist:
            if(r.notAssigned or r.adjZone):
                for cid in State.options[r.id]:
                    c = State.cars[cid]
                    if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                        cost = Cost.costToAddR(c,r)
                        if(cost>best):
                            if(currCost - cost<State.backupCost):
                                #print("Pog")
                                return c,None,r,1
                            else:
                            
                                #nextcode = copy.deepcopy(self.solver.curcode)
                                nextcode = Code.formCode() 
                                for temprID in c.res:
                                    tempr = State.rlist[temprID]
                                    if(r.overlap(tempr.start,tempr.end)):
                                        #overlap => r zou moeten worden verwijderd
                                        nextcode[0][tempr.id]='x'
                                nextcode[0][r.id]=c.id
                                if(Code.inMemory(nextcode)):
                                    continue
                            self.timeClimbing += (time.perf_counter()-tempStart)
                            self.countClimbing += 1 
                            return c,None,r,0
           
        #All sensible 'car zone' swaps
        for c in State.cars:
            for rid in c.res:
                r = State.rlist[rid]
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    
                    #nextcode = copy.deepcopy(self.solver.curcode)
                    nextcode = Code.formCode() 
                    nextcode[1][c.id] = r.zone 
                    for temprID in c.res:
                        tempr = State.rlist[temprID]
                        if(tempr.zone == r.zone):
                            pass
                        elif(tempr.zone in Car.zoneIDtoADJ[r.zone]):
                            pass
                        else:
                            nextcode[0][tempr.id]='x'
                    if(Code.inMemory(nextcode)):
                        continue
                    self.timeClimbing += (time.perf_counter()-tempStart)
                    self.countClimbing += 1                     
                    return c,r.zone,None,0
        self.timeClimbing += (time.perf_counter()-tempStart)
        self.countClimbing += 1 
        return None,None,None,0

    def localSearch(self,steepest_descent = 0):
        tempStart = time.perf_counter()
        count = 0
        while(1):
            count += 1
            #pick one of the local search methods
            if(steepest_descent):
                bestc,bestz,bestr = self.steepest_descent()
                newBackup = 0
            else:
                bestc,bestz,bestr,newBackup = self.hill_climbing()#is sneller en beter?
            
            if(bestz is not None):
                bestc.setZone(bestz)
            elif(bestr is not None):
                if(bestr.getCar()):#if currently assigned to a car, remove from list
                    #print(bestr.id,bestr.getCar().res)
                    bestr.getCar().res.remove(bestr.id)
                #assign to new car
                bestc.addR(bestr)
            else:
                #reached peak
                break
            if(newBackup):
                State.backup(Cost.getCost(State.rlist))
                Code.add()
            elif(not(Code.add())):
                print("iets fout met nextcode in localSearch")
            if(steepest_descent == 1):
                break
        self.timeSpentLS += time.perf_counter()-tempStart
        self.countLS += 1
        return count
    def leastAssigned(self):
        tempStart = time.perf_counter()
        lowest = 999999999999999
        ret = None   
        bestr = None     
        for r in State.rlist:
                if(r.assignCount<lowest):
                    for cid in State.options[r.id]:
                        c = State.cars[cid]
                        nextcode = Code.formCode() 
                        
                        #addR and setZone will remove conflicts: r not in zone/adjZone, overlap
                        for temprID in c.res:
                            tempr = State.rlist[temprID]
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
            Code.add()
            #print("assigned least popular r",bestr.id,bestr.assignCount)
        else:
            print("geen opties meer voor leastAssigned => ") 
            changed = self.localSearch(1)
            #self.shake(len(State.cars))
            #self.initialSolution()
            return ret
        self.timeSpentLA += time.perf_counter()-tempStart        
        return ret    
    def findSolution(self):
    	#TODO:
    	#
        sinceLast = time.perf_counter()
        prevBest = 999999999999999

        State.backup(Cost.getCost(State.rlist))
        i = 0
        start = time.perf_counter()
        while(1):     
            tempStart = time.perf_counter()       
            i+=1            
            if((time.perf_counter()-start) > self.solver.maxtime):
                 print('~~timeisup~~')
                 break   #return because the time is up
            

            if((time.perf_counter()-sinceLast) > 300):#atleast x% better every y seconds
                sinceLast = time.perf_counter()
                print("checkTime",sinceLast,prevBest,State.backupCost,"cur:",Cost.getCost(State.rlist), "best:",State.getBest())
                if(not((prevBest-State.backupCost)/prevBest)>0):
                    print("too slow")
                    State.restore()
                    
                    self.leastAssigned()
                    count = self.localSearch(0)
                    

                    
                    
                    cost = Cost.getCost(State.rlist)
                    if(cost < State.getBest()): 
                        State.setBestResult(cost)
 
                    State.backup(Cost.getCost(State.rlist))
                    print("Toslow setBackup:",State.backupCost)
                prevBest = State.backupCost
                State.backup(Cost.getCost(State.rlist))
                
            
            self.timeSpent1 += time.perf_counter()-tempStart    

            
            count = self.localSearch(0)
            
            tempStart = time.perf_counter()  
            cost = Cost.getCost(State.rlist)

            if(i%100==0):
                print(i,':',cost,count,State.getBest(),State.backupCost)
            if(cost<State.getBest()):
                State.setBestResult(cost)
                sinceLast = time.perf_counter()
            if(cost<State.backupCost):
                State.backup(Cost.getCost(State.rlist))
                print("Better=>setBackupCost2:",State.backupCost)

            else:
                State.restore()

                
            self.timeSpent2 += time.perf_counter()-tempStart   
            changed = self.pertubeer()
            
            if(not(changed)):
                print("No more changes after:",i)   
                self.leastAssigned()
                cost = Cost.getCost(State.rlist)
                if(cost<State.getBest()): 
                    State.setBestResult(cost)
                State.backup(Cost.getCost(State.rlist))
                

        if(Cost.getCost(State.rlist)<State.getBest()): 
            State.setBestResult(Cost.getCost(State.rlist))
        
        print("time spent in localSearch:",self.timeSpentLS,self.countLS,self.timeSpentLS/self.countLS) #11.36  /  99.62
        print("     time spent in Climbing:",self.timeClimbing,self.countClimbing,self.timeClimbing/self.countClimbing)        
        
        print("time spent in leastAssigned:",self.timeSpentLA) #0    /  0.042

        print("time spent in Pertubeer:",self.timeSpentPert,self.countPert) #6.81   /  88.21
        print("     time spent in Choose:",self.timeSpentChoose,self.countChoose,self.timeSpentChoose/self.countChoose) 
        
        print("time spent in 1:",self.timeSpent1) 
        print("time spent in 2:",self.timeSpent2) 

    def findPeak(self,start,margin):
        newBest = 0    
        tempstart = time.perf_counter()      
        for i in range(100):   
            i+=1
            # count = self.localSearch(1) #steepest_descent
            count = self.localSearch(0) #hill_climbing
            cost = Cost.getCost(State.rlist)
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

    def shake(self,amount):
        tries = 0
        while(1):
            for i in range(random.randint(1, amount+20)): #pas dit aan -> amount ipv amount+1
                randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                randomCarIndex = random.randint(0, len(State.cars)-1)
                        
                c1 = State.cars[randomCarIndex]
                c1.setZone(randomZoneIndex)
                   
            if(Code.add()):
                break
            else:
                tries+=1
                if(tries>10):
                    amount+=1
                    print("violant shaking")
                    tries = 0
        
    
            
    def VariableNeighbourhoud(self):
        start = time.perf_counter()        
        iteration = 0
        noChange = 0
        bestSolver = copy.deepcopy(self.solver)
        
        maxAmount = int(len(State.cars)/1.5)
        amount = int(len(State.cars)/10)
        
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
        for cid in State.options[r.id]:
            c = State.cars[cid]
            if(len(c.res)<minL):   
                nextcode = Code.formCode()      
                #addR and setZone will remove conflicts: r not in zone/adjZone, overlap
                for temprID in c.res:
                    tempr = State.rlist[temprID]
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
        self.countChoose +=1    
        return bestc,bestr,minL
    def pertubeer(self):
        self.countPert+=1
        tempStart = time.perf_counter()
        minL = 99999999999
        bestc = None
        bestr = None
        for r in State.rlist:
            if(r.notAssigned):
                bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
                if(bestr):
                    pass
        if(bestr is None):
            #print("try adjecent")
            for r in State.rlist:
                if(r.adjZone):
                    bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
         
        if(bestr is None):
            #print("try all others")
            for r in State.rlist:
                if(not(r.adjZone or r.notAssigned)):
                    bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
          
        if(bestr):                
            bestc.setZone(bestr.zone)
            bestc.addR(bestr)
           
            if(not(Code.add())):
                print("iets fout met nextcode in forceAssign")
            #print(" Forced assign")    
            self.timeSpentPert += time.perf_counter()-tempStart       
            return 1
        else:    
            print("No Forced assign")
            self.timeSpentPert += time.perf_counter()-tempStart                   
            return 0
