import glob
from readCSV import readCSV
from writeCSV import writeCSV
from Car import Car
from Reservation import Reservation
from Cost import Cost
from Code import Code
import time
import random
import math


START_TEMPRATURE = 10000
END_TEMPRATURE= 10
NUM_ITERATIONS= 1000
COOLING_RATE = 0.95
STEP = 15

def handler(signum, frame):
    print("Times up! Exiting...")
    exit(0)
def assignRes(c,r,adj):
    c.res.append(r)
    r.notAssigned = False 
    r.adjZone = adj
    r.car = c
    # print("assign request id ",r.id, " to car id", c.id )
def tryAssign(c,r):
    if(not(c.overlap(r.start,r.end))):
        # print("no overlap",c.zone , r.zone)
        if(c.zone == r.zone):#car is in zone of r
            # print("adj false    assigned to car:",c.id,'\n')
            adj = False
        elif(c.zone in Car.zoneIDtoADJ[r.zone]):
            # print("adj true    assigned adjecent to car",c.id,'\n')
            adj=True

        else:
            # print("    Swap needed",c.id)
            return False
        assignRes(c,r,adj)
        return True
    else:
        # print("overlap",c.id)
        return False
def initialSolution1(reservatieLijst,cars):
    for r in reservatieLijst:
        if(r.notAssigned):
            #print(r)#add
            for c in r.options:
                    #print(c)#add
                    if(tryAssign(c,r)):
                        break
        #  print(r.notAssigned, " before the second if")            
        if(r.notAssigned):#could not be assigned to any car, because first the cars zone are 0. The car could have be assiged to a request but duo to the initialization they have zone 0
            for c in r.options:
                    if(len(c.res)==0):#No other reservations so no problem
                         #print("    change zone of car",c.id,c.zone,'\n')
                        c.zone = r.zone
                        adj = False
                        assignRes(c,r,adj)
                         # print("second if  assign")
                        break
def solution(reservatieLijst,cars):
    for r in reservatieLijst:
        if(r.notAssigned):
            # print(r)#add
            for c in r.options:
                    # print(c)#add
                    if(tryAssign(c,r)):
                        break   
    return reservatieLijst , cars
        # if(r.notAssigned):
        #     for c in r.options:
        #         adj = False
        #         assignRes(c,r,adj)
        #         break

def freeData(currReservationList, currCarList):
    for r in currReservationList:
        r.car = None
        r.notAssigned=True
        r.adjZone=False
    for c in currCarList:
        c.res=[]
def simulatedAnnealing(reservatieLijst, cars, currCost):
    bestReservationList, bestCarsList ,bestCost =reservatieLijst, cars,currCost
    currReservationList , currCarList= reservatieLijst,cars
    # printResult(bestResvationList,besCarsList)
    #select random  zone and assign it to random car 
    t = START_TEMPRATURE
    while t > END_TEMPRATURE:
        i =0 
        while(i < NUM_ITERATIONS):
            while True:
                randomZoneIndex = random.randint(0, len(Car.zoneIDtoADJ)-1)
                randomCarIndex = random.randint(0, len(cars)-1)
                car=bestCarsList[randomCarIndex]
                if(car.zone != randomZoneIndex):
                    break
            
            car.zone= randomZoneIndex
        
            freeData(currReservationList, currCarList)
            
            # print ( "assign zone ",randomZoneIndex," to car " ,randomCarIndex )
            # printResult(currReservationList,currCarList)
            
            newReservationsList, newCarsList=solution(currReservationList,currCarList)
            # printResult(newReservationsList,newCarsList)
            newCost = Cost.getCost(newReservationsList)
            
            # print(newCost, "==", currCost )
            diff = newCost-currCost
            
            if diff < 0:
                currReservationList= newReservationsList
                currCarList=newCarsList
                currCost=newCost
                # print("lesser")
            else:
                probability= math.exp(-diff/t)
                if(random.uniform(0,1) < probability):
                    # print("probability")
                    currReservationList= newReservationsList
                    currCarList=newCarsList
                    currCost=newCost
            i += 1
        t = t * COOLING_RATE
        print(t)
    # carReservationRegister = car.res
    return currReservationList , currCarList, currCost        


def localSearch(rlist,cars):
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
                # print("reservationID ",r.id, " --> carid ", c.id," in zone " ,c.zone, ",,, r zone ",r.zone)
                if((c.zone==r.zone) or (c.zone in Car.zoneIDtoADJ[r.zone])):#only swap if car is in possible zone
                    cost =  c.costToAddr(r)
                    if(cost>best):
                        best = cost
                        bestc = c
                        bestr = r
                        # print(bestc.id,best,bestr)
        # print(best,bestc,bestr)
        #All sensible 'car zone' swaps
        for c in cars:
            for r in c.res:
                cost =  c.costToSetZ(r.zone)
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
        else:
            return count
# def metaheuristiek(reservationList ,carsList):
#     for r in reservationList:
#         for c in r.options:

def forceAssign(rlist,cars):
    minL = 99999999999 
    bestc = None
    bestr = None
    nextcode = Code.formCode(rlist,cars)
    for r in rlist:
        #print(r)
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
                        #print("was in memory")
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
    
        #print("forceAssign",bestr.id,bestc.id)
        bestc.setZone(bestr.zone)
        bestc.addr(bestr)
        return 1
    else:
        print("No Forced assign")
        return 0
                    
def printResult(rlist,cars):
    print('Cars:')
    for c in cars:
        print('   ',c)
    print('Reservations:')
    for r in rlist:
        print('   ',r)
        print('   ',r.notAssigned,r.adjZone)
def main():
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
    cars, reservatieLijst = readCSV(Car,Reservation,'./csv/'+f+'.csv')
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
    
    cost = Cost.getCost(reservatieLijst)
    code = Code.formCode(reservatieLijst,cars,cost)
    #code = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], [0, 0, 0, 0, 0, 0], 1000]
    #gves the code to the dictionary Code.passedCodesPerL
    Code.add(code)
    
    
    initialSolution1(reservatieLijst,cars)
    initialCost = Cost.getCost(reservatieLijst)
    bestCost = initialCost
    printResult(reservatieLijst,cars)
    # print(bestCost)
    
    [bestRList, bestCList,optimalCost]=simulatedAnnealing(reservatieLijst, cars, bestCost)
    printResult(bestRList,bestCList)
    print("optimal ", optimalCost)
    #everything is clear until here
    
    print("----------------"*2)
    print("\ni,bestcost,swaps")
    for i in range(10000):
        count = localSearch(reservatieLijst,cars)
        if(i%100==0):
            print(i,bestCost,count)
        
        if(not(0)):
            cost = Cost.getCost(reservatieLijst)
            if(cost<bestCost):
                writeCSV(cost,Car,cars,reservatieLijst,f)
                code = Code.formCode(reservatieLijst,cars,cost)
                Code.add(code)
                bestCost = cost
            changed = forceAssign(reservatieLijst,cars)
            if(not(changed)):
                print("No more changes after:",i)
                break
            code = Code.formCode(reservatieLijst,cars,cost)
            Code.add(code)
        code = Code.formCode(reservatieLijst,cars)
        #print(code)
        cost = Cost.getCost(reservatieLijst)
    
    cost = Cost.getCost(reservatieLijst)
    if(cost<bestCost):
        writeCSV(cost,Car,cars,reservatieLijst,f)
        code = Code.formCode(reservatieLijst,cars,cost)
        Code.add(code)
        bestCost = cost
    print("bestc:",bestCost)
    print("----------------"*2)
    printResult(reservatieLijst,cars)
    for cd in Code.passedCodesPerL:
        pass#print(cd)
    print("bestc:",bestCost)

  
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    print("--- %s seconds ---" % (time.perf_counter() - start_time))