import csv
def readCSV(Car,Reservation,f = 'toy1.csv'):
    reservationList=[]
    zonesList=[]
    carsList=[]
    # read from csv file
    with open(f, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file , delimiter=";")
        for row in csv_reader:

            if(row[0][:2]=="+Z"):
                Zones = int(row[0].split(' ')[1])
            if row[0][0]=="r": #reservation
                tempReservation=[]
                for i in range(len(row)):
                    
                    if(i==5): #index of the car's list
                        cars= row[i].split(',')
                        tempReservation.append(cars)
                    else:
                        tempReservation.append(row[i])
                reservationList.append(tempReservation)
            elif row[0][0] == "z": # zone
                tempZone=[]
                tempZone.append(row[0])
                zones = row[1].split(',')
                tempZone.append(zones)
                zonesList.append(tempZone)
            elif row[0][0] == "c": # car
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
    Car.zoneIDtoADJ = []
    for zone in zonesList:# loop over zone lines a second time otherwise zoneIDtoADJ will return keyError
        AdjectentZone = zone[1] 
        #convert string IDs to numerical IDs
        IDset = set()
        for z in AdjectentZone:
            IDset.add(Car.zoneStrtoID[z])
        Car.zoneIDtoADJ.append(IDset)
        i+=1
    Reservation.zoneIDtoADJ = Car.zoneIDtoADJ
    j = 0
    for car in carsList: #read car lines of csv 
        cars.append(Car())
        c = car
        Car.carIDtoStr[j] =  c
        Car.carStrtoID[c] = j
        j+=1
        
    k = 0
    options = []
    for res in reservationList:
        ID = res[0]
        zone = Car.zoneStrtoID[res[1]]
        day = res[2]
        startTime = res[3]
        duration = res[4]
        P1 = int(res[6])
        P2 = int(res[7])
	
        OptionalCars = []
    
        for o in res[5]:
            OptionalCars.append(Car.carStrtoID[o])
        options.append(OptionalCars)    
        r = Reservation(zone,day,startTime,duration,P1,P2)
    
        reservatieLijst.append(r) 
        Reservation.resIDtoStr[k] = ID
           
        k+=1
    return cars, reservatieLijst,options,Zones

def average(csvFile,rond):
    if(rond==0):
        return 0,999999999,0
    num , sum =0, 0
    min=99999999999
    csvFile = csvFile.split('/')[-1]
    csvFile = csvFile.split('.')[0]
    for i in range(rond):
        file= './csv_solutions/'+csvFile+'_solution_'+str(i+1)+'.csv'
        print(file)
        with open(file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file , delimiter=";")
            for row in csv_reader:
                cost=int(row[0])
                sum+=cost
                num+=1
                if(cost<min):
                    min=cost
                    csvNum=i+1
                break
                
    
    return sum/num , min , csvNum

    
