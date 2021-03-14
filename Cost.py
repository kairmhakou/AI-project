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
        print("cost:",cost)
        return cost
        
    def comp(a,b):#kijken wat het verschil zou zijn voor een swap
        kostA=a.notAssigned*a.P1 + a.adjZone*a.P2
        kostB=b.notAssigned*b.P1 + b.adjZone*b.P2
        verschil= kostB-kostA
        print( 'vershil:', verschil)
        return verschil
    