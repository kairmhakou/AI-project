class Reservation:
    id = 0
    resIDtoStr = {}
    def __init__(self,day,start,duration,P1,P2,carOptions):
        self.id = Reservation.id
        Reservation.id += 1
        
        self.start = int(day)*1440+int(start) #○convert to minutes (24*60 minutes per day)
        self.end = self.start + int(duration) #cast day, start, duration from txt to int
        
        self.P1 = P1  # cost for not assigning Reservation
        self.P2 = P2  # cost for assigning to adjecent zone
        
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
        s = str(self.id)+ " "
        s += Reservation.resIDtoStr[self.id]
        s+= ", CarOptions: "+ str(self.options)
        s+= ", start/end: "+str(self.start)+'/'+str(self.end)
        s+= ", P1/P2: "+str(self.P1)+'/'+str(self.P2)
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
        s = str(self.id)+" "
        s +=  Car.carIDtoStr[self.id]
        s += " in zone: "+str(Car.zoneIDtoStr[self.zone])
        s += " / reservations: "
        s += str(self.res)
        return s
    
class Cost: #Was reservatieLijt
    def getCost(lijst):#Kost berekenen
        cost=0
        for r in lijst:
            cost+= r.x1*r.P1 + r.x2*r.P2
        return cost
        
    def comp(a,b):#kijken wat het verschil zou zijn voor een swap
        kostA=a.x1*a.P1 + a.x2*a.P2
        kostB=b.x1*b.P1 + b.x2*b.P2
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