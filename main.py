import glob
from readCSV import readCSV
from writeCSV import writeCSV
from Car import Car
import threading
from Reservation import Reservation
from Cost import Cost
from Code import Code
from Printer import Printer
import copy
import time
def handler(signum, frame):
    print("Times up! Exiting...")
    exit(0)
def assignRes(c,r,adj):
    c.res.append(r)
    r.notAssigned = False 
    r.adjZone = adj
    r.car = c
def tryAssign(c,r):
    if(not(c.overlap(r.start,r.end))):
        if(c.zone == r.zone):#car is in zone of r
            #print("    assigned to car:",c.id,'\n')
            adj = False
        elif(c.zone in Car.zoneIDtoADJ[r.zone]):
            #print("    assigned adjecent to car",c.id,'\n')
            adj=True
        else:
            #print("    Swap needed",c.id)
            return False
        assignRes(c,r,adj)
        return True
    else:
        #print("overlap",c.id)
        return False
def initialSolution1(reservatieLijst,cars):
    for r in reservatieLijst:
        if(r.notAssigned):
            for c in r.options:
                    if(tryAssign(c,r)):
                    if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
                        c.addR(r)
                        break            
        if(r.notAssigned):#could not be assigned to any car
            for c in r.options:
                    if(len(c.res)==0):#No other reservations so no problem
                        #print("    change zone of car",c.id,c.zone,'\n')
                        c.zone = r.zone
                        adj = False
                        assignRes(c,r,adj)
                        c.setZone(r.zone)
                        c.addR(r)
                        break
                    

def localSearch(rlist,cars):
def localSearch(rlist,cars,Cost):
    count = 0
    while(1):
        count += 1
        best = 0 #verbetering >0
        bestc = None
        bestz = None
        bestr = None
        
        #All possible 'assigned car' swaps
        for r in rlist:
            for c in r.options:
                if((c.zone==r.zone) or (c.zone in Car.zoneIDtoADJ[r.zone])):#only swap if car is in possible zone
                    cost =  c.costToAddr(r)
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        best = cost
                        bestc = c
                        bestr = r
                        #print(bestc.id,best,bestr)
        
        #All sensible 'car zone' swaps
        for c in cars:
            for r in c.res:
                cost =  c.costToSetZ(r.zone)
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    best = cost
                    bestc = c
                    bestz = r.zone
                    #print(bestc.id,best,bestz)
        if(bestz is not None):
            bestc.setZone(bestz)
        elif(bestr is not None):
            if(bestr.car):#if currently assigned to a car, remove from list
                bestr.car.res.remove(bestr)
            #assign to new car
            bestc.addr(bestr)
            bestc.addR(bestr)
        else:
            return count
   
def forceAssign(rlist,cars):
    minL = 99999999999
    bestc = None
    bestr = None
    nextcode = Code.formCode(rlist,cars)
    for r in rlist:
        if(r.notAssigned):
            for c in r.options:
                if(len(c.res)<minL):
                    """
                    NIET AANPASSEN 
                    ga voor problemen zorgen
                    """
                    nextcode = Code.formCode(rlist,cars)
                    nextcode = c.changeCode(r,nextcode)
                    if(Code.inMemory(nextcode)):
                        continue
                    """
                    NIET AANPASSEN
                    """
                    minL = len(c.res)
                    bestc = c
                    bestr = r
    if(bestr):
        nextcode = Code.formCode(rlist,cars)
        nextcode = bestc.changeCode(bestr,nextcode)
        if(Code.inMemory(nextcode)):
            input("was in memory HOW")
    
            
        bestc.setZone(bestr.zone)
        bestc.addr(bestr)
        bestc.addR(bestr)
        return 1
    else:
        print("No Forced assign")
        return 0
                    
    
def main(f):
    cars, reservatieLijst = readCSV(Car,Reservation,'./csv/'+f+'.csv')

    Printer.printDict(Car)
    #base state of solution
    cost = Cost.getCost(reservatieLijst)
    code = Code.formCode(reservatieLijst,cars,cost)
    Code.add(code)
    

    initialSolution1(reservatieLijst,cars)
    initialCost = Cost.getCost(reservatieLijst)
    
    #initialise best solution
    bestCost = initialCost
    bestcars=None
    bestreservatieLijst=None
    Printer.printResult(reservatieLijst,cars)
    bestcars = copy.deepcopy(cars)
    bestreservatieLijst =copy.deepcopy(reservatieLijst)
    
    print("----------------"*2)
    print("\ni,bestcost,swaps")
    i = 0
    while(1):
        if((time.perf_counter() - start_time)>300):   #set  time it may run , 5min=300sec
            print('~~timeisup~~')
            break   #return because the time is up
        i+=1
        count = localSearch(reservatieLijst,cars,Cost)
        if(i%100==0):
            print(i,bestCost,count)
        
        cost = Cost.getCost(reservatieLijst)
        code = Code.formCode(reservatieLijst,cars,cost)
        Code.add(code)
        if(cost<bestCost):
            code = Code.formCode(reservatieLijst,cars,cost)
            print("newBest",cost)
            bestcars = copy.deepcopy(cars)
            bestreservatieLijst =copy.deepcopy(reservatieLijst)
            Code.add(code)
            bestCost = cost
            
            
        changed = forceAssign(reservatieLijst,cars)
        cost = Cost.getCost(reservatieLijst)
        code = Code.formCode(reservatieLijst,cars,cost)
        Code.add(code)
        if(not(changed)):
            print("No more changes after:",i)
            break

    writeCSV(bestCost,Car,bestcars,bestreservatieLijst,f)

    
    Printer.printFinal(bestCost,reservatieLijst,cars,Code)
  
if __name__ == "__main__":
    arr = glob.glob(".\csv\*.csv")
    print('options:')
    i = 0
    filenames = []
    for f in arr:
        file = f.split('\\')[-1]
        filenames.append(file.split('.')[0])
        print(i,":",filenames[i])
        i+=1
        
    fnr = int(input("Choose file nr: "))
    f = filenames[fnr]
    start_time = time.perf_counter()
    main(f)
    print("--- %s seconds ---" % (time.perf_counter() - start_time))