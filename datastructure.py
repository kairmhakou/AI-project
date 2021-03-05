class Reservation:
    id = 0
    resIDtoStr = {}
    def __init__(self,day,start,duration,P1,P2,carOptions):
        self.id = Reservation.id
        Reservation.id += 1
        
        self.start = int(day)*1440+int(start) #○convert to minutes (24*60 minutes per day)
        self.end = self.start + int(duration) #cast day, start, duration from txt to int
        
        self.P1 = 7 #P1 # cost for not assigning Reservation
        self.P2 = 15 #P2 # cost for assigning to adjecent zone
        
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
        s =  Car.carIDtoStr[self.id]
        s += " in zone: "+str(Car.zoneIDtoStr[self.zone])
        s += " / res: "
        s += str(self.res)
        return s
    
class ReservatieLijst:
    def __init__(self,lijst=None):
        self.kost=0
        if lijst==None:
            self.lijst=[]
        else:
            self.lijst=lijst
        self.l=len(self.lijst)
        
    def bereken(self):#Kost berekenen
        print ('****************kost berekenen **********************')
        self.kost=0
        i=0
        while i<self.l:
            r=self.lijst[i]
            self.kost+= r.x1*r.P1 + r.x2*r.P2
            i+=1
        print ('De kost is momenteel=', self.kost)
    
    def voegtoe(self,a):
        self.lijst.append(a)
        self.l+=1
        
    def comp(self,a,b):#kijken wat het verschil zou zijn voor een swap
        print ('****************Vergelijk de kost **********************')
        kostA=a.x1*a.P1 + a.x2*a.P2
        kostB=b.x1*b.P1 + b.x2*b.P2
        verschil= kostB-kostA
        print( 'vershil:', verschil)
        return verschil
    
    def swap(self,a,b):# effectief swappen
        print ('****************Swappen **********************')
        i=0
        while i<self.l:
            if self.lijst[i]==a:
                self.lijst[i]=b
                return
            i+=1