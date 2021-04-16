# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 23:50:06 2021

@author: dehan
"""
import csv
from State import State
from Car import Car
def writeCSV(f):
    
    num = 0
    print(f)
    f = f.split('/')[-1]
    #f = f.split('\\')[-1] #een van deze twee splits afh. van OS denk ik
    #bij errors misschien vervangen
    
    f = f.split('.')[0]
    print(f)
    num +=1

    rlist,cars,cost = State.resultRlist,State.resultCars,State.result
    with open('./csv_solutions/'+f+'_solution_'+str(num)+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow([str(cost)])
        writer.writerow(['+Vehicle', 'assignments'])
        for c in cars:
            writer.writerow([Car.carIDtoStr[c.id]] + [Car.zoneIDtoStr[c.zone]])
        writer.writerow(['+Assigned', 'requests'])
        for r in rlist:
            if(not(r.notAssigned)):
                writer.writerow(["req"+str(r.id)] + [Car.carIDtoStr[r.carID]])
                
        writer.writerow(['+Unassigned', 'requests'])
        for r in rlist:
            if(r.notAssigned):
                writer.writerow(["req"+str(r.id)])
