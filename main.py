import glob
from readCSV import readCSV
from writeCSV import writeCSV
from Car import Car
from Reservation import Reservation
from Cost import Cost
from Code import Code
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
            #print(r)
            for c in r.options:
                    if(tryAssign(c,r)):
                        break            
        if(r.notAssigned):#could not be assigned to any car
            for c in r.options:
                    if(len(c.res)==0):#No other reservations so no problem
                        #print("    change zone of car",c.id,c.zone,'\n')
                        c.zone = r.zone
                        adj = False
                        assignRes(c,r,adj)
                        break
                    

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
                if((c.zone==r.zone) or (c.zone in Car.zoneIDtoADJ[r.zone])):#only swap if car is in possible zone
                    cost =  c.costToAddr(r)
                    if(cost>best):
                        best = cost
                        bestc = c
                        bestr = r
                        #print(bestc.id,best,bestr)
        
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

def methaheuristiek():
    """
    Metaheuristiek toepassen
    """
    pass
def forceAssign(rlist,cars):
    """
    
    Zoekruimte uitbreiden naar adjZone
    
    """
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
def main(config):
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
    Code.add(code)
    
    
    initialSolution1(reservatieLijst,cars)
    initialCost = Cost.getCost(reservatieLijst)
    bestCost = initialCost
    
    printResult(reservatieLijst,cars)
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
                strCode = Code.codeToStr(code)
                """
                save beste code
                als timer afgaat: 
                        converteer code terug naar reservatielijst,cars,cost
                        save met writeCSV(cost,Car,cars,reservatieLijst,f)
                """
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
    sum2 = 0
    for cd in Code.passedCodesPerL:
        print(len( Code.passedCodesPerL[cd]))
        sum2+=len( Code.passedCodesPerL[cd])
    print("bestc:",bestCost)
    print(sum2)

  
if __name__ == "__main__":
    config = None
    """
    Lees parameters in 
    "input_file" "solution_file" "time_limit" "random_seed" "num_threads"
    config
    """
    start_time = time.perf_counter()
    main(config)
    print("--- %s seconds ---" % (time.perf_counter() - start_time))