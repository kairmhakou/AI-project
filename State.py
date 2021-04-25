# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: Loic Dehan
"""

class State:
    Zones = None
    
    maxC = 9999999999999999999
    options = None
    cars,rlist,bestCost = None,None,maxC  
    
    backupCars,backupRlist,backupCost = None,None,maxC
    
    resultRlist,resultCars,result = None,None,maxC
    

    def restore():
        State.cars = [x.clone() for x in State.backupCars]
        State.rlist = [x.clone() for x in State.backupRlist]
        return State.backupCost
    def backup(cost):
        State.backupCars = [x.clone() for x in State.cars]
        State.backupRlist = [x.clone() for x in State.rlist]
        State.backupCost = cost

    def setBestResult(cost):
        State.resultRlist = [x.clone() for x in State.rlist]
        State.resultCars = [x.clone() for x in State.cars]
        State.result = cost

    def reset():
        State.Zones = None

        State.maxC = 9999999999999999999
        State.options = None
        State.cars,State.rlist,State.bestCost = None,None,State.maxC  
    
        State.backupCars,State.backupRlist,State.backupCost = None,None,State.maxC
    
        State.resultRlist,State.resultCars,State.result = None,None,State.maxC


if __name__ == "__main__":
    pass
