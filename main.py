from readCSV import readCSV
from datastructure import Car
from datastructure import Reservation
from datastructure import Cost
    
def main():
    cars, reservatieLijst = readCSV(Car,Reservation,'toy1.csv')
    cost = Cost.getCost(reservatieLijst)
    
    print("cost:",cost)
    print('Reservations:')
    for r in reservatieLijst:
        print('   ',r)
    print('Cars:')
    for c in cars:
        print('   ',c)

    print('Dictionaries:')  
    print('   carIDtoStr',Car.carIDtoStr)
    print('   carStrtoID',Car.carStrtoID)
    print('   zoneIDtoStr',Car.zoneIDtoStr)
    print('   zoneStrtoID',Car.zoneStrtoID)
    print('   zoneIDtoADJ',Car.zoneIDtoADJ)

if __name__ == "__main__":
    main()