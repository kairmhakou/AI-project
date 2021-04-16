# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: Loic Dehan
"""



import copy
class State:
    Zones = 0
    RassignCount = [0]*1000
    
    maxC = 9999999999999999999
    options = None
    cars,rlist,bestCost = None,None,maxC  
    
    backupCars,backupRlist,backupCost = None,None,maxC
    
    resultRlist,resultCars,result = None,None,maxC
    
    curCode = None
    def restore():
        State.cars = [x.clone() for x in State.backupCars]
        State.rlist = [x.clone() for x in State.backupRlist]
    def backup(cost):
        State.backupCars = [x.clone() for x in State.cars]
        State.backupRlist = [x.clone() for x in State.rlist]
        State.backupCost = cost

    def setBestResult(cost):
        State.resultRlist = [x.clone() for x in State.rlist]
        State.resultCars = [x.clone() for x in State.cars]
        State.result = cost

if __name__ == "__main__":
    pass
