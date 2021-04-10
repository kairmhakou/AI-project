import copy
from Cost import Cost
import time
from Code import Code
from Car import Car
import random

class Great_deluge:
    def __init__(self,solver):
        self.solver = solver

    def staydry(self,up):
        print(up)
        b=2
        solver2=copy.deepcopy(self.solver)
        c=0
        a=solver2.getBest()
        while(b<120):
            print('wet -------------')
            solver2.freeData()
            self.tempSolution(solver2)
            cost = Cost.getCost(solver2.rlist)
            print(cost)
            b+=1
            if(cost<=a-up):
                print('improvement')
                solver2.setBest()
                a=solver2.getBest()
                self.solver=copy.deepcopy(solver2)

            else:
                up-=(up/10)
                if(up<=0):
                    up=0
                print('up:',up)
            print(a)
        print(' we are dry')
        return self.solver
        print(a)
    
    def tempSolution(self,solver2):

        l = solver2.rlist
        random.shuffle(l)
        for r in l:
            if(r.notAssigned):
                for c in solver2.options[r.id]:
                        if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
                            c.addR(r)
                            break   
        for r in l:                
            if(r.notAssigned):#could not be assigned to any car
                for c in solver2.options[r.id]:
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
        for r in l:                
            if(r.adjZone):#could not be assigned to any car
                for c in solver2.options[r.id]:
                        if(not(c.overlap(r.start,r.end)) and (c.zone ==r.zone)):
                            c.addR(r)
                            break
            if(r.adjZone):#could not be assigned to any car
                for c in solver2.options[r.id]:               
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break

