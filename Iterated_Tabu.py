# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:45:53 2021

@author: Loic Dehan
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
        self.countLS = 1

        self.timeSpentLA = 0
        self.timeSpentPert = 0
        self.countPert = 1
        self.timeSpentChoose = 0
        self.countChoose = 1
        self.timeSpent1 = 0
        self.timeSpent2 = 0

        self.timeClimbing = 0
        self.countClimbing = 1
    def steepest_descent(self,best = 999999999999999999):
        bestc = None
        bestz = None    
        
        for c in State.cars:
            for z in range(State.zones):
                if(c.zone == z):
                    continue
                cost =  Cost.costToSetZone(c,z)
                if(cost<best):
                    nextcode = Code.formCode() 
                    nextcode[1][c.id] = z
                    for temprid in c.res:
                        tempr = State.rlist[temprid]
                        if(tempr.zone == z):
                            pass
                        elif(tempr.zone in Car.zoneIDtoADJ[z]):
                            pass
                        else:
                            nextcode[0][tempr.id]='x'
                        
                    if(Code.inMemory(nextcode)):
                        continue
                    
                    best = cost
                    bestc = c
                    bestz = z

        return bestc,bestz
        
    def hill_climbing(self,exp):
        """
        Find first improvement that is not tabu
            Assign a reservation to a (new) car
            Assign a reservation to a (new) car in adjecent zone
            Switch zone of car to an adjecent zone (unused)
        
        """
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
                                return c,None,r,1,None
                            else:
                                nextcode = Code.formCode() 
                                for temprID in c.res:
                                    tempr = State.rlist[temprID]
                                    if(r.start < tempr.end and tempr.start < r.end):#(r.overlap(tempr.start,tempr.end)):
                                        nextcode[0][tempr.id]='x'
                                nextcode[0][r.id]=c.id
                                if(Code.inMemory(nextcode)):
                                    continue
                            self.timeClimbing += (time.perf_counter()-tempStart)
                            self.countClimbing += 1 
                            return c,None,r,0,nextcode
        
        if(exp == 1):
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
                                    return c,zid,r,1,None
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
                                        if(r.start < tempr.end and tempr.start < r.end):#(r.overlap(tempr.start,tempr.end)):
                                            nextcode[0][tempr.id]='x'
                                    nextcode[0][r.id]=c.id
                                    if(Code.inMemory(nextcode)):
                                        continue
                                self.timeClimbing += (time.perf_counter()-tempStart)
                                self.countClimbing += 1 
                                return c,zid,r,0,nextcode   
        if(1):
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
                        return c,zid,None,0,nextcode
            self.timeClimbing += (time.perf_counter()-tempStart)
            self.countClimbing += 1 
     
        return None,None,None,0,None

    def localSearch(self,method = 0,exp = 0):
        tempStart = time.perf_counter()
        
        count,newBackup,finishBackup = 0,0,0

        while(1):
            count += 1
            if(method == 0):#first improvement until local best
                bestc,bestz,bestr,newBackup,nextcode = self.hill_climbing(exp)
                if(bestz is not None):
                    bestc.setZone(bestz)
                  
                if(bestr is not None):

                    if(bestr.getCar()):#if currently assigned to a car, remove from rlist
                        bestr.getCar().res.remove(bestr.id)
                    #assign to new car
                    bestc.addR(bestr)
                    
                else:#reached peak
                    break
                if(newBackup):
                    finishBackup = 1
                    backupCost = Cost.getCost(State.rlist)
                    Code.add(Code.formCode() )
                elif(not(Code.add(Code.formCode()))):
                    print("iets fout met nextcode in localSearch")
                
            else: #least bad step away from local best
                bestc,bestz = self.steepest_descent()
                if(bestz is not None):
                    bestc.setZone(bestz)
                    if(not(Code.add(Code.formCode() ))):
                        print("iets fout met nextcode in localSearch")
                break
            
        if(finishBackup):
            pre = State.backupCost
            State.backup(Cost.getCost(State.rlist))
            #print("finish backup",State.backupCost,pre,State.backupCost-pre<0)
        self.timeSpentLS += time.perf_counter()-tempStart
        self.countLS += 1
        return count
    def leastAssigned(self,amount):
        tempStart = time.perf_counter()
        bestr = None     
        used = []
        while(len(used)<amount):
            #find least frequently assigned reservation r 
            lowest = 999999999999999           
            for r in State.rlist:
                if(not(r.id in used)):
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
            used.append(bestr.id)
            
            Code.add(Code.formCode())

        self.timeSpentLA += time.perf_counter()-tempStart        
   
    def Tabu_Search_base(self):
        start = time.perf_counter()
        i = 0
        while(1):     
            tempStart = time.perf_counter()       
            i+=1            
            if((time.perf_counter()-start) > self.solver.maxtime):
                 print('~~timeisup~~')
                 break   #return because the time is up 
                 
            self.localSearch(exp = 1) #find local minimum of cost 
            cost = Cost.getCost(State.rlist)
            if(cost<State.result):
                State.setBestResult(cost)
            self.localSearch(method = 1) # take 1 step that increases the cost the least
            
                
            if(i%100==0):
                print(time.perf_counter()-start,i,':',cost,State.result,State.backupCost)
    def Iterated_local_search(self):
        sinceLast = time.perf_counter()
        prevBest = 999999999999999

        State.backup(Cost.getCost(State.rlist))
        State.setBestResult(Cost.getCost(State.rlist))
        
        i = 0
        start = time.perf_counter()
        amount = min(len(State.rlist)/10,1)
        while(1):         
            i+=1            
            if((time.perf_counter()-start) > self.solver.maxtime):
                 print('~~timeisup~~')
                 break   #return because the time is up
            
            if((time.perf_counter()-sinceLast) > 5):#check atleast x% better every y seconds
                sinceLast = time.perf_counter()
                print("checkTime",sinceLast-start,prevBest)#State.backupCost,"cur:",Cost.getCost(State.rlist), "best:",State.result)
                if(not((prevBest-State.backupCost)/prevBest)>0):#No improvement since last check
                    print("too slow")
                    self.leastAssigned(amount)
                    State.backup(Cost.getCost(State.rlist))    
                prevBest = State.backupCost
                
            
            count = self.localSearch(exp = 1)#local search naar lokaal minimum voor cost
            
            #slaag beste resultaat op voor eindresultaat
            cost = Cost.getCost(State.rlist)
            if(cost<State.result):
                State.setBestResult(cost)
                sinceLast = time.perf_counter()
                
            
            #intensificatie voor meest recente minimum -> ga terug naar backup
            if(cost<State.backupCost):
                State.backup(Cost.getCost(State.rlist))
            else:
                State.restore()

  
            changed = self.perturbeer()
            if(not(changed)):#All options for perturbeer are tabu
                print("=> leastAssigned")
                self.leastAssigned(amount)
                State.backup(Cost.getCost(State.rlist))    
                prevBest = State.backupCost
            
            ############
            if(i%100==0):
                print(time.perf_counter()-start,i,':',"cur:",Cost.getCost(State.rlist), "best:",State.result,"backup:",State.backupCost)
                
 
        print("time spent in localSearch:",self.timeSpentLS,self.countLS,self.timeSpentLS/self.countLS) #11.36  /  99.62
        print("     time spent in Climbing:",self.timeClimbing,self.countClimbing,self.timeClimbing/self.countClimbing)        
        
        print("time spent in leastAssigned:",self.timeSpentLA) #0    /  0.042

        print("time spent in Perturbeer:",self.timeSpentPert,self.countPert) #6.81   /  88.21
        print("     time spent in Choose:",self.timeSpentChoose,self.countChoose,self.timeSpentChoose/self.countChoose) 
        
        print("time spent in 1:",self.timeSpent1) 
        print("time spent in 2:",self.timeSpent2) 
        
        print("time spent in getCost:",Cost.timeSpentGet,Cost.timeSpentGet/Cost.countGet) 
    
    def choose(self,r,minL,bestc,bestr):
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
                    elif(r.start < tempr.end and tempr.start < r.end):#(r.overlap(tempr.start,tempr.end)):
                        nextcode[0][tempr.id] = 'x'
                nextcode[0][r.id] = c.id #r would be assign to c (addR)
                nextcode[1][c.id] = r.zone #c would be placed in r's zone (setZone)
                if(Code.inMemory(nextcode)):
                    continue
                minL = len(c.res)
                bestc = c
                bestr = r
        return bestc,bestr,minL
    def perturbeer(self):
        self.countPert+=1
        tempStart = time.perf_counter()
        
            
        minL = 99999999999
        bestc = None
        bestr = None
        #Look through not assigned reservations
        for r in State.rlist:
            if(r.notAssigned):
                bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
        
        #Look through not assigned reservations
        if(bestr is None):
            for r in State.rlist:
                if(r.adjZone):
                    bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
        """
        #Look through all others
        if(bestr is None):
            for r in State.rlist:
                if(not(r.adjZone or r.notAssigned)):
                    bestc,bestr,minL = self.choose(r,minL,bestc,bestr)
        """  
        
        #Assign bestr to bestc and add to tabu list
        if(bestr):                
            bestc.setZone(bestr.zone)
            bestc.addR(bestr)
            Code.add(Code.formCode())
   
            self.timeSpentPert += time.perf_counter()-tempStart       
            return 1
        else:    
            #All assignments are tabu
            print("No Forced assign")
            self.timeSpentPert += time.perf_counter()-tempStart                   
            return 0
        
