# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:50:39 2021

@author: dehan
"""
import random
from State import State
class Printer:              
    def printResult(rlist,cars):
        print('Cars:')
        for c in cars:
            print('   ',c)
        print('Reservations:')
        for r in rlist:
            print('   ',r)
            print('   ',r.notAssigned,r.adjZone)
    def printCars(cars):
        print('Cars:')
        for c in cars:
            print('   ',c)
    def printDict(Car):
        print('Dictionaries:')  
        print('   carIDtoStr',Car.carIDtoStr)
        print('   carStrtoID',Car.carStrtoID)
        print('   zoneIDtoStr',Car.zoneIDtoStr)
        print('   zoneStrtoID',Car.zoneStrtoID)
        print('   zoneIDtoADJ',Car.zoneIDtoADJ)
        print('\n'*2)
    def printFinal(solver,Code):
        
        print("bestc:",State.result)
        print("----------------"*2)
        #Printer.printResult(solver.bestrlist,solver.bestcars)
        
if __name__ == "__main__":
    random.seed = 10 
    print(random.random())
    print(random.random())
    random.seed = 10 
    print("----")
    print(random.random())
    print(random.random())
