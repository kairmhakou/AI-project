# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 23:50:06 2021

@author: dehan
"""
import csv
def writeCSV(solver,Car):
    f = solver.f
    cars  = solver.bestcars
    cost  = solver.bestCost
    rlist = solver.bestrlist
    
    with open('./csv_solutions/'+f+'_solution.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow([str(cost)])
        writer.writerow(['+Vehicle', 'assignments'])
        for c in cars:
            writer.writerow([Car.carIDtoStr[c.id]] + [Car.zoneIDtoStr[c.zone]])
        writer.writerow(['+Assigned', 'requests'])
        for r in rlist:
            if(not(r.notAssigned)):
                writer.writerow(["req"+str(r.id)] + [Car.carIDtoStr[r.car.id]])
                
        writer.writerow(['+Unassigned', 'requests'])
        for r in rlist:
            if(r.notAssigned):
                writer.writerow(["req"+str(r.id)])
