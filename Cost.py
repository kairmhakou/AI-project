# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:27:23 2021

@author: Loic Dehan
"""
from State import State
import time
class Cost:
    timeSpentGet = 0
    countGet = 1
    def getCost(rlist):#Kost berekenen
        Cost.countGet+=1
        tempStart = time.perf_counter()
        
        cost=0
        for r in rlist:
            cost += r.notAssigned*r.P1 + r.adjZone*r.P2#r.cost()
        Cost.timeSpentGet+= time.perf_counter()-tempStart   
        
        return cost  
            
    def costAddRSetZ(c,nres,zone):
        #bv momenteel not assign => nres.cost = 50 -> adjZone     50-25 = 25 (25 beter)
        #overlap => nieuwe NotAssigned -> slechter -> -r.P1 ( maar + eventueel P2)

        cost = (nres.notAssigned*nres.P1 + nres.adjZone*nres.P2)-(zone!=nres.zone)*nres.P2 # current cost - new cost of nres
        for rid in c.res:
            if(rid == nres.id):
                continue
            r = State.rlist[rid]
            if(nres.start < r.end and r.start < nres.end):
                #overlap => r zou moeten worden verwijderd
                cost -= (r.P1-(r.notAssigned*r.P1 + r.adjZone*r.P2))
            else:
                cost += r.costNewZone(zone)
        
        return cost
        
    def costToSetZone(c,zone):
        cost = 0
        for rid in c.res:
            cost += State.rlist[rid].costNewZone(zone)
        return cost
    
    def costToAddR(c,nres):
        cost = (nres.notAssigned*nres.P1 + nres.adjZone*nres.P2)-(c.zone!=nres.zone)*nres.P2 # current cost - new cost of nres
        for rID in c.res:
            r = State.rlist[rID] 
            if(nres.start < r.end and r.start < nres.end):
                #overlap => r zou moeten worden verwijderd
                cost -= (r.P1-(r.notAssigned*r.P1 + r.adjZone*r.P2))
        return cost 
    
if __name__ == "__main__":
    pass
