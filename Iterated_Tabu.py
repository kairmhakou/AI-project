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

class Iterated_Tabu:
   
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

    def hill_climbing(self):
        tempStart = time.perf_counter()
        best = 0 #verbetering >0
        currCost = Cost.getCost(State.rlist)
        #All possible 'assigned car' swaps assign to ideal zone
        for r in State.rlist:
            if(r.notAssigned or r.adjZone):
                for cid in State.options[r.id]:
                    c = State.cars[cid]
                    if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                        cost = Cost.costToAddR(c,r)
                        if(cost>best):
                            if(currCost - cost<State.backupCost):
                                return c,None,r,1
                            else:
                                nextcode = Code.formCode() 
                                for temprID in c.res:
                                    tempr = State.rlist[temprID]
                                    if(r.overlap(tempr.start,tempr.end)):
                                        nextcode[0][tempr.id]='x'
                                nextcode[0][r.id]=c.id
                                if(Code.inMemory(nextcode)):
                                    continue
                            self.timeClimbing += (time.perf_counter()-tempStart)
                            self.countClimbing += 1 
                            return c,None,r,0
        
        #All possible 'assigned car' swaps assign to adj zone
        for r in State.rlist:
            if(r.notAssigned):
                adjZones = Car.zoneIDtoADJ[r.zone]
                for cid in State.options[r.id]:
                    c = State.cars[cid]
                    for zid in adjZones:         
                        cost = Cost.costAddRSetZ(c,r,zid)
                        if(cost>best):
                            if(currCost - cost<State.backupCost):  
                                return c,zid,r,1
                            else:
                                nextcode = Code.formCode() 
                                nextcode[1][c.id] = zid 
                                for temprID in c.res:
                                    tempr = State.rlist[temprID]
                                    if(tempr.zone == zid):
                                        pass
                                    elif(tempr.zone in Car.zoneIDtoADJ[zid]):
                                        pass
                                    else:
                                        nextcode[0][tempr.id]='x'
                                    if(r.overlap(tempr.start,tempr.end)):
                                        nextcode[0][tempr.id]='x'
                                nextcode[0][r.id]=c.id
                                if(Code.inMemory(nextcode)):
                                    continue
                            self.timeClimbing += (time.perf_counter()-tempStart)
                            self.countClimbing += 1 
                            return c,zid,r,0   
        """
        #All sensible 'car zone' swaps #overbodig?
        for c in State.cars:
            for rid in c.res:
                zid = r.zone
                r = State.rlist[rid]
                cost =  Cost.costToSetZone(c,zid)
                if(cost>best):
                    nextcode = Code.formCode() 
                    nextcode[1][c.id] = zid
                    for temprID in c.res:
                        tempr = State.rlist[temprID]
                        if(tempr.zone == zid):
                            pass
                        elif(tempr.zone in Car.zoneIDtoADJ[zid]):
                            pass
                        else:
                            nextcode[0][tempr.id]='x'
                    if(Code.inMemory(nextcode)):
                        continue
                    self.timeClimbing += (time.perf_counter()-tempStart)
                    self.countClimbing += 1                     
                    return c,zid,None,0
        self.timeClimbing += (time.perf_counter()-tempStart)
        self.countClimbing += 1 
        """
        
        
        
        return None,None,None,0

    def localSearch(self):
        tempStart = time.perf_counter()
        count = 0
        while(1):
            count += 1

            bestc,bestz,bestr,newBackup = self.hill_climbing()
            
            if(bestz is not None):
                bestc.setZone(bestz)
            if(bestr is not None):
                if(bestr.getCar()):#if currently assigned to a car, remove from rlist
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

        self.timeSpentLS += time.perf_counter()-tempStart
        self.countLS += 1
        return count
    def leastAssigned(self):
        tempStart = time.perf_counter()
        ret = None   
        bestr = None     
        while(1):
            #find least frequently assigned reservation r 
            lowest = 999999999999999           
            for r in State.rlist:
                if(r.notAssigned or r.adjZone):
                    if(State.RassignCount[r.id]<lowest):
                        bestr = r
                        lowest = State.RassignCount[r.id]
            #find best car c to assign it to
            best = -9999999999999999
            bestc = None
            for cid in State.options[bestr.id]:
                c = State.cars[cid]
                cost = Cost.costToAddR(c,bestr)
                if(cost>best):
                    bestc = c
                    best = cost
            #assign r to c
            bestc.setZone(bestr.zone)
            bestc.addR(bestr) 
            if(not(Code.inMemory(Code.formCode()))):
                Code.add()
                break
            #print("assigned least popular r",bestr.id,bestr.assignCount)
        else:
            print("geen opties meer voor leastAssigned => ") 
            changed = self.localSearch()
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
            

            if((time.perf_counter()-sinceLast) > 10):#atleast x% better every y seconds
                sinceLast = time.perf_counter()
                print("checkTime",sinceLast-start,prevBest,State.backupCost,"cur:",Cost.getCost(State.rlist), "best:",State.getBest())
                if(not((prevBest-State.backupCost)/prevBest)>0):
                    print("too slow")
                    State.restore()
                    
                    for _ in range(len(State.rlist)):
                        self.leastAssigned()
                    count = self.localSearch()
                    
     
                    
                    cost = Cost.getCost(State.rlist)
                    if(cost < State.getBest()): 
                        State.setBestResult(cost)
 
                    State.backup(Cost.getCost(State.rlist))
                    print("Toslow setBackup:",State.backupCost)
                prevBest = State.backupCost
                State.backup(Cost.getCost(State.rlist))
                
            
            self.timeSpent1 += time.perf_counter()-tempStart    

            
            count = self.localSearch()
            
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
                for _ in range(len(State.rlist)):
                    self.leastAssigned()
                count = self.localSearch()
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
            count = self.localSearch() #hill_climbing
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
