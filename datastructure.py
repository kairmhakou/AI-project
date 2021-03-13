class Reservation:
    id = 0
    resIDtoStr = {}
    def __init__(self,zone,day,start,duration,P1,P2,carOptions):
        self.id = Reservation.id
        Reservation.id += 1
        self.carID = -1
        self.zone = zone
        self.start = int(day)*1440+int(start) #○convert to minutes (24*60 minutes per day)
        self.end = self.start + int(duration) #cast day, start, duration from txt to int
        
        self.P1 = P1  # cost for not assigning Reservation
        self.P2 = P2  # cost for assigning to adjecent zone
        
        self.notAssigned = True #1 -> not assigned
        self.adjZone = False #1 -> assigned to adjecent zone
        
        self.options = carOptions #id of possible cars
        
    
    def overlap(self,start,end):
        if(self.start<=start<=self.end):
            return True
        if(self.start<=end<=self.end):
            return True
        return False
    def __str__(self):
        s = str(self.id)+ " "
        s += Reservation.resIDtoStr[self.id]
        s+=", zone: "+str(self.zone)
        s+= ", P1/P2: "+str(self.P1)+'/'+str(self.P2)
        s+= ", start/end: "+str(self.start)+'/'+str(self.end)
        s+= ", CarOptions: "+ str(self.options)
        return s
class Car:
    id = 0
    carIDtoStr = {}
    carStrtoID = {}
    zoneIDtoStr = {}
    zoneStrtoID = {}
    zoneIDtoADJ = {}
    def __init__(self):
        self.id = Car.id
        Car.id += 1
    
        self.res = [] #list of reservations assigned to this car
        self.zone = 0
        
    def overlap(self,start,end):

        for r in self.res:
            if(r.overlap(start,end)):
                return True
        return False
        

    def __str__(self):
        s = str(self.id)+" "
        s +=  Car.carIDtoStr[self.id]
        s += " in zone: "+str(Car.zoneIDtoStr[self.zone])
        s += " / reservations: ["
        for r in self.res:
            s+=str(r.id)+','
        s+=']'
        return s
    
class Cost: #Was reservatieLijt
    def getCost(lijst):#Kost berekenen
        cost=0
        for r in lijst:
            cost+= r.notAssigned*r.P1 + r.adjZone*r.P2
        print("cost:",cost)
        return cost
        
    def comp(a,b):#kijken wat het verschil zou zijn voor een swap
        kostA=a.notAssigned*a.P1 + a.adjZone*a.P2
        kostB=b.notAssigned*b.P1 + b.adjZone*b.P2
        verschil= kostB-kostA
        print( 'vershil:', verschil)
        return verschil
    
    def swap(self,a,b):# effectief swappen (dit swapt niet echt iets tho)
        i=0
        while i<self.l:
            if self.lijst[i]==a:
                self.lijst[i]=b
                return
            i+=1