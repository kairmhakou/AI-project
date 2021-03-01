import csv

class Reservation:
    id = 0
    resIDtoStr = {}
    def __init__(self,day,start,duration,P1,P2,carOptions):
        self.id = Reservation.id
        Reservation.id += 1
        
        self.start = day*1440+start #○convert to minutes (24*60 minutes per day)
        self.end = self.start + duration
        
        self.P1 = P1 # cost for not assigning Reservation
        self.P2 = P2 # cost for assigning to adjecent zone
        
        self.x1 = 1 #1 -> not assigned
        self.x2 = 0 #1 -> assigned to adjecent zone
        
        self.options = [] #id of possible cars
        for c in carOptions:
            self.options.append(Car.carStrtoID[c])
    
    def overlap(self,start,end):
        if(self.start<=start<=self.end):
            return True
        if(self.start<=end<=self.end):
            return True
        return False
    def __str__(self):
        s = Reservation.resIDtoStr[self.id]
        s+= ", CarOptions: "+ str(self.options)
        s+= ", start/end:"+str(self.start)+'/'+str(self.end)
        s+= ", P1/P2:"+str(self.P1)+'/'+str(self.P2)
        return s
class Car:
    id = 0
    carIDtoStr = {}
    carStrtoID = {}
    zoneIDtoStr = {-1:"Not Assigned"}
    zoneStrtoID = {}
    zoneIDtoADJ = {}
    def __init__(self):
        self.id = Car.id
        Car.id += 1
    
        self.res = [] #list of reservations assigned to this car
        self.zone = -1
        
    def overlap(self,day,start,duration):
        start = day*1440+start
        end = start+duration
        for r in self.res:
            if(r.overlap(start,end)):
                return True
        return False
        

    def __str__(self):
        s =  Car.carIDtoStr[self.id]
        s += " in zone: "+str(Car.zoneIDtoStr[self.zone])
        s += " / res: "
        s += str(self.res)
        return s
    
"""
@Karim:
    Vervang deze while lussen met het inlezen van de CSV file 

"""
i = 0
#read csv file

with open('toy1.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file , delimiter=";")
    
    for row in csv_reader:
        if row[0][0]== "z":
        # while(1): #read zone lines of csv 
            
            z =  row[0] #replace = '...' by the zoneID from csv
            Car.zoneIDtoStr[i] = z  
            Car.zoneStrtoID[z] = i
            i+=1
            # if(i>=5):#if last car line
            #     break
            
        i = 0
        if row[0][0]== "z":
        # while(1):# loop over zone lines a second time otherwise zoneIDtoADJ will return keyError
            zones= row[1].split(',')
            AdjectentZone = zones #replace by list in CSV file
            #convert string IDs to numerical IDs
            arr = []
            for z in AdjectentZone:
                arr.append(Car.zoneStrtoID[z])
            Car.zoneIDtoADJ[i] = arr
            i+=1
            # if(i>=5):#if last car line
            #     break
        j = 0
        cars = []
        if row[0][0]== "c": #read car lines of csv 
            cars.append(Car())
            c = row[0] #replace = ... by the carID from csv
            Car.carIDtoStr[j] =  c
            Car.carStrtoID[c] = j
            j+=1
            # if(j>=5):#if last car line
            #     break
            
        k = 0
        reservations = []
        # while(1):
        if row[0][0]== "r":
            #Replace these variables by values in csv file
            ID = row[0]
            day = row[2]
            startTime = row[3]
            duration = row[4]
            P1 = row[6]
            P2 = row[7]
            autos= row[5].split(',')
            OptionalCars = autos
            r = Reservation(day,startTime,duration,P1,P2,OptionalCars) 
            reservations.append(r)
            Reservation.resIDtoStr[k] = ID 
            
            k+=1
            # if(i>=1):
            #     break
print('Reservations:')
for r in reservations:
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