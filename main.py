from readCSV import readCSV
from datastructure import Car
from datastructure import Reservation
    
def main():

    cars, reservatieLijst = readCSV(Car,Reservation,'toy1.csv')

    """   
    Kost.bereken()
    Kost.comp(Kost.lijst[3],Kost.lijst[7])
    Kost.swap(Kost.lijst[3],Kost.lijst[7])
    """   
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