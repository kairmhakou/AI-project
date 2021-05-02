#Unused file
import copy
import time
import random

from Cost import Cost
from Car import Car
from State import State

class Great_deluge:
    def __init__(self,solver):
        self.solver = solver

    def staydry(self,up):
        print(up)
        b=2
        State.backup(Cost.getCost(State.rlist))
        #solver2=copy.deepcopy(self.solver)
        c=0
        a=State.getBest()
        while(b<120):
            print('wet -------------')
            self.solver.freeData()
            self.tempSolution()
            self.localSearch()
            cost = Cost.getCost(State.rlist)
            print(cost)
            b+=1
            if(cost<=a-up):
                print('improvement')
                State.setBestResult(Cost.getCost(State.rlist))
                a=State.getBest()
                #self.solver=copy.deepcopy(solver2)
                #State.restore()

            else:
                up-=(up/10)
                if(up<=0):
                    up=0
                print('up:',up)
            print(a)
        print(' we are dry')
        return State.resultRlist , State.resultCars
        print(a)
    
    def tempSolution(self):
        l = State.rlist
        random.shuffle(l)
        for r in l:
            if(r.notAssigned):
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
                            c.addR(r)
                            break   
        for r in l:                
            if(r.notAssigned):#could not be assigned to any car
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
        for r in l:                
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
                    print(bestr.getCar().res)
                    print(bestr.id)
                    bestr.getCar().res.remove(bestr.id)
                #assign to new car
                bestc.addR(bestr)
            else:
                #reached peak
                return

