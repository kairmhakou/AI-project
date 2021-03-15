# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:27:23 2021

@author: dehan
"""

class Cost:
    def getCost(lijst):#Kost berekenen
        cost=0
        for r in lijst:
            cost += r.cost()
        return cost    
    
    def costToSetZone(c,zone):
        cost = 0
        for r in c.res:
            cost += r.costNewZone(zone)
        return cost
    
    def costToAddR(c,nres):
        cost = nres.cost()-(c.zone!=nres.zone)*nres.P2
        for r in c.res:
            if(nres.overlap(r.start,r.end)):
                #overlap => r zou moeten worden verwijderd
                cost -= (r.P1-r.cost())
        return cost
    
    
if __name__ == "__main__":
    pass