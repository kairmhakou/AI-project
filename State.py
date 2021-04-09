# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: dehan
"""



import copy
class State:
    cars = None    
    rlist = None
    bestCost = 9999999999999999999
    backupCars = None
    backupRlist = None
    backupCost = 99999999999999
    def restore():
        """print(State.cars)
        print(State.rlist)
        print("backupCars",State.backupCars)
        print(State.backupRlist)"""
        State.cars = [x.clone() for x in State.backupCars]#copy.deepcopy(State.backupCars)
        State.rlist = [x.clone() for x in State.backupRlist]#copy.deepcopy(State.backupRlist)
    def backup(cost):
        State.backupCars = [x.clone() for x in State.cars]#copy.deepcopy(State.cars)
        State.backupRlist = [x.clone() for x in State.rlist]#copy.deepcopy(State.rlist)
        State.backupCost = cost
if __name__ == "__main__":
    pass
