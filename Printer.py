# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:50:39 2021

@author: dehan
"""

class Printer:              
    def printResult(rlist,cars):
        print('Cars:')
        for c in cars:
            print('   ',c)
        print('Reservations:')
        for r in rlist:
            print('   ',r)
            print('   ',r.notAssigned,r.adjZone)
    def printDict(Car):
        print('Dictionaries:')  
        print('   carIDtoStr',Car.carIDtoStr)
        print('   carStrtoID',Car.carStrtoID)
        print('   zoneIDtoStr',Car.zoneIDtoStr)
        print('   zoneStrtoID',Car.zoneStrtoID)
        print('   zoneIDtoADJ',Car.zoneIDtoADJ)
        print('\n'*2)
    def printFinal(bestCost,reservatieLijst,cars,Code):
        print("bestc:",bestCost)
        print("----------------"*2)
        Printer.printResult(reservatieLijst,cars)
        for cd in Code.passedCodesPerL:
            your_list = Code.passedCodesPerL[cd]
            #length of code set , amount in code set , no duplicates(ideally True)
            print(cd,len(your_list),len(your_list) == len(set(your_list)))
            
           
        print("bestc:",bestCost)
        
if __name__ == "__main__":
    pass