import csv
def readCSV(Car,Reservation,f = 'toy1.csv'):
    reservationList=[]
    zonesList=[]
    carsList=[]
    # read from csv file
    with open(f, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file , delimiter=";")
        for row in csv_reader:
            if row[0][0]=="r": #reservation
                tempReservation=[]
                for i in range(len(row)):
                    
                    if(i==5): #index of the auto's list
                        autos= row[i].split(',')
                        tempReservation.append(autos)
                    else:
                        tempReservation.append(row[i])
                reservationList.append(tempReservation)
            elif row[0][0] == "z": # zone
                tempZone=[]
                tempZone.append(row[0])
                zones= row[1].split(',')
                tempZone.append(zones)
                zonesList.append(tempZone)
            else: 
                carsList.append(row[0])
                
    # enter into datastructures        
    cars = []
    reservatieLijst = []
    i = 0
    for zone in zonesList: 
        z = zone[0] #zoneID
        Car.zoneIDtoStr[i] = z  
        Car.zoneStrtoID[z] = i
        i+=1
       
    i = 0
    for zone in zonesList:# loop over zone lines a second time otherwise zoneIDtoADJ will return keyError
        AdjectentZone = zone[1] 
        #convert string IDs to numerical IDs
        arr = []
        for z in AdjectentZone:
            arr.append(Car.zoneStrtoID[z])
        Car.zoneIDtoADJ[i] = arr
        i+=1
        
    j = 0
    for car in carsList: #read car lines of csv 
        cars.append(Car())
        c = car #carID
        Car.carIDtoStr[j] =  c
        Car.carStrtoID[c] = j
        j+=1
        
    k = 0
    print(reservationList)
    for res in reservationList:
        ID = res[0]
        day = res[2]
        startTime = res[3]
        duration = res[4]
        P1 = int(res[6])
        P2 = int(res[7])
        OptionalCars = res[5]
        r = Reservation(day,startTime,duration,P1,P2,OptionalCars)
        reservatieLijst.append(r) 
        #Kost.voegtoe(r)
        Reservation.resIDtoStr[k] = ID
           
        k+=1
    return cars, reservatieLijst