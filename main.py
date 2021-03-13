from readCSV import readCSV
from datastructure import Car
from datastructure import Reservation
from datastructure import Cost
        
def assignRes(c,r,adj):
    c.res.append(r)
    r.notAssigned = False 
    r.adjZone = adj
    r.carID = c.id
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
def initialSolution1(reservatieLijst,cars,Car):
    for r in reservatieLijst:
        if(r.notAssigned):
            print(r)
            for c in cars:
                if(c.id in r.options):#car is a valid option for r
                    if(tryAssign(c,r)):
                        break            
        if(r.notAssigned):#could not be assigned to any car
            for c in cars:
                if(c.id in r.options):#car is a valid option for r
                    if(len(c.res)==0):#No other reservations so no problem
                        print("    change zone of car",c.id,c.zone,'\n')
                        c.zone = r.zone
                        adj = False
                        assignRes(c,r,adj)
                        break
    
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
    initialSolution1(reservatieLijst,cars,Car)
    Cost.getCost(reservatieLijst)
    print('Cars:')
    for c in cars:
        print('   ',c)
    print('Reservations:')
    for r in reservatieLijst:
        print('   ',r)
        print('   ',r.notAssigned,r.adjZone)
    
if __name__ == "__main__":
    main()