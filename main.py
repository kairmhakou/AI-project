from readCSV import readCSV
from writeCSV import writeCSV
from datastructure import Car
from datastructure import Reservation
from datastructure import Cost
        
def assignRes(c,r,adj):
    c.res.append(r)
    r.notAssigned = False 
    r.adjZone = adj
    r.car = c
def tryAssign(c,r):
    if(not(c.overlap(r.start,r.end))):
        if(c.zone == r.zone):#car is in zone of r
            print("    assigned to car:",c.id,'\n')
            adj = False
        elif(c.zone in Car.zoneIDtoADJ[r.zone]):
            print("    assigned adjecent to car",c.id,'\n')
            adj=True

        else:
            print("    Swap needed",c.id)
            return False
        assignRes(c,r,adj)
        return True
    else:
        print("overlap",c.id)
        return False
def initialSolution1(reservatieLijst,cars):
    for r in reservatieLijst:
        if(r.notAssigned):
            print(r)
            for c in r.options:
                    if(tryAssign(c,r)):
                        break            
        if(r.notAssigned):#could not be assigned to any car
            for c in r.options:
                    if(len(c.res)==0):#No other reservations so no problem
                        print("    change zone of car",c.id,c.zone,'\n')
                        c.zone = r.zone
                        adj = False
                        assignRes(c,r,adj)
                        break
                    

def localSearch(rlist,cars):
    best = 0 #verbetering >0
    bestc = None
    bestz = None
    bestr = None
    
    #All possible 'assigned car' swaps
    for r in rlist:
        for c in r.options:
            cost =  c.costToAddr(r)
            if(cost>best):
                best = cost
                bestc = c
                bestr = r
                print(bestc.id,best,bestr)
    
    #All sensible 'car zone' swaps
    for c in cars:
        for r in c.res:
            cost =  c.costToSetZ(r.zone)
            print("zoneCost:",cost)
            if(cost>best):
                best = cost
                bestc = c
                bestz = r.zone
                print(bestc.id,best,bestz)
    if(bestz):
        bestc.setZone(bestz)
    elif(bestr):
        if(bestr.car):
            bestr.car.res.remove(bestr)
        bestc.add(bestr)
    else:
        return 0
    return 1
    
def forceAssign(rlist,cars):
    minL = 99999999999 
    bestc = None
    bestr = None
    for r in rlist:
        print(r)
        if(r.notAssigned):
            for c in r.options:
                if(len(c.res)<minL):
                    minL = len(c.res)
                    bestc = c
                    bestr = r
    if(bestr):
        print("forceAssign",bestr.id,bestc.id)
        bestc.setZone(bestr.zone)
        bestc.add(bestr)
        
                    
def printResult(Cost,rlist,cars):
    Cost.getCost(rlist)
    print('Cars:')
    for c in cars:
        print('   ',c)
    print('Reservations:')
    for r in rlist:
        print('   ',r)
        print('   ',r.notAssigned,r.adjZone)
def main():
    cars, reservatieLijst = readCSV(Car,Reservation,'toy1.csv')
    print('Cars:')
    for c in cars:
        print('   ',c)

    print('Dictionaries:')  
    print('   carIDtoStr',Car.carIDtoStr)
    print('   carStrtoID',Car.carStrtoID)
    print('   zoneIDtoStr',Car.zoneIDtoStr)
    print('   zoneStrtoID',Car.zoneStrtoID)
    print('   zoneIDtoADJ',Car.zoneIDtoADJ)
    print('\n'*2)
    
    
    Cost.getCost(reservatieLijst)
    #initialSolution1(reservatieLijst,cars)
    
    printResult(Cost,reservatieLijst,cars)

    
    for i in range(20):
        changed = localSearch(reservatieLijst,cars)
        if(not(changed)):
            forceAssign(reservatieLijst,cars)
        printResult(Cost,reservatieLijst,cars)
        #•input() 
    
    cost = Cost.getCost(reservatieLijst)
    writeCSV(cost,Car,cars,reservatieLijst)
if __name__ == "__main__":
    main()