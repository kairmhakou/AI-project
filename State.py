# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: dehan
"""



import copy
class State:
    maxC = 9999999999999999999
    options = None
    cars,rlist,bestCost = None,None,maxC  
    
    backupCars,backupRlist,backupCost = None,None,maxC
    
    resultRlist,resultCars,result = None,None,maxC
    def restore():
        """print(State.cars)
        print(State.rlist)
        print("backupCars",State.backupCars)
        print(State.backupRlist)"""
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
        
    def getBest():
        return State.result
if __name__ == "__main__":
    pass
