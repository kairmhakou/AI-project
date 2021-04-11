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
          

            
    def costAddRSetZ(c,nres,zone):
        #bv momenteel not assign => nres.cost = 50 -> adjZone     50-25 = 25 (25 beter)
        #overlap => nieuwe NotAssigned -> slechter -> -r.P1 ( maar + eventueel P2)
        #
        cost = nres.cost()-(zone!=nres.zone)*nres.P2
        for rid in c.res:
            if(rid == nres.id):
                continue
            r = State.rlist[rid]
            if(nres.overlap(r.start,r.end)):
                #overlap => r zou moeten worden verwijderd
                cost -= (r.P1-r.cost())
            else:
                cost += r.costNewZone(zone)
        
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
