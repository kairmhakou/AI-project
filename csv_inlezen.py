import csv


reservationList=[]
zonesList=[]
carsList=[]

with open('toy1.csv', mode='r') as csv_file:
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
        else: #car
            carsList.append(row[0])
            
            
print(reservationList)
print(carsList)
print(zonesList)