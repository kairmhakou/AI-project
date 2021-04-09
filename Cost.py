# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:27:23 2021

@author: dehan
"""
from State import State

class Cost:
    def getCost(rlist):#Kost berekenen
        cost=0
        for r in rlist:
            cost += r.cost()
        return cost    
    
    def costToSetZone(c,zone):
        cost = 0
        for rid in c.res:
            r = State.rlist[rid]
            cost += r.costNewZone(zone)
        return cost
    
    def costToAddR(c,nres):
        cost = nres.cost()-(c.zone!=nres.zone)*nres.P2
        for rID in c.res:
            r = State.rlist[rID] 
            if(nres.overlap(r.start,r.end)):
                #overlap => r zou moeten worden verwijderd
                cost -= (r.P1-r.cost())
        return cost 
    
if __name__ == "__main__":
    pass
