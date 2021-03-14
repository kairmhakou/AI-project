# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 23:50:06 2021

@author: dehan
"""
"""
+Vehicle	assignments
car0	z1
car1	z4
car2	z3
car3	z4
car4	z0
car5	z2
+Assigned	requests
req0	car4
req1	car1
req2	car3
req4	car5
req5	car4
req6	car2
req7	car1
req8	car0
req9	car3
+Unassigned	requests
req3	

"""
import csv
def writeCSV(cost,Car,cars,rlist):
    #input("writingResult")
    with open('solution.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow([str(cost)])
        print(str(cost))
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