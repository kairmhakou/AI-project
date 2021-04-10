# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:50:39 2021

@author: dehan
"""
import random
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
        
        print("bestc:",solver.bestCost)
        print("----------------"*2)
        #Printer.printResult(solver.bestrlist,solver.bestcars)
        
        codecount = 0
        for cd in Code.passedCodesPerL:
            your_list = Code.passedCodesPerL[cd]
            #length of code set , amount in code set , no duplicates(ideally True)
            print(cd,len(your_list),len(your_list) == len(set(your_list)))
            codecount += len(your_list)
        print(codecount,Code.memCount)
            
           
        print("bestc:",solver.bestCost)
        
if __name__ == "__main__":
    random.seed = 10 
    print(random.random())
    print(random.random())
    random.seed = 10 
    print("----")
    print(random.random())
    print(random.random())