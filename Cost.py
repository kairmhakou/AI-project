# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:27:23 2021

@author: Loic Dehan
"""
from State import State
class Cost:
    #Calculate cost of a list of reservation (sum of penalties for not assigning (P1) and assigning to an adjecent zone (P2))
    def getCost(rlist):
        cost=0
        for r in rlist:
            cost += r.notAssigned*r.P1 + r.adjZone*r.P2#r.cost()
        return cost  
    
    #How would the cost change if car c was placed in zone zone and if reservation nres was assigned to car c
    def costAddRSetZ(c,nres,zone):
        #ie. currently not assign => nres.cost = 50 -> adjZone     50-25 = 25 (improvement of 25)
        #overlap => new NotAssigned -> worse -> -r.P1 ( sometimes + r.P2)

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
        
    #How would the cost change if car c was placed in zone zone
    def costToSetZone(c,zone):
        cost = 0
        for rid in c.res:
            cost += State.rlist[rid].costNewZone(zone)
        return cost
    
    #How would the cost change if reservation nres was assigned to car c
    def costToAddR(c,nres):
        cost = (nres.notAssigned*nres.P1 + nres.adjZone*nres.P2)-(c.zone!=nres.zone)*nres.P2 # current cost - new cost of nres
        for rID in c.res:
            r = State.rlist[rID] 
            #Overlapping reservations would be removed
            if(nres.start < r.end and r.start < nres.end):
                cost -= (r.P1-(r.notAssigned*r.P1 + r.adjZone*r.P2))
        return cost 
    
if __name__ == "__main__":
    pass
