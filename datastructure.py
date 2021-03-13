class Reservation:
    id = 0
    resIDtoStr = {}
    def __init__(self,zone,day,start,duration,P1,P2,carOptions):
        self.id = Reservation.id
        Reservation.id += 1
        self.car = None
        self.zone = zone
        self.start = int(day)*1440+int(start) #convert to minutes (24*60 minutes per day)
        self.end = self.start + int(duration) #cast day, start, duration from txt to int
        
        self.P1 = P1  # cost for not assigning Reservation
        self.P2 = P2  # cost for assigning to adjecent zone
        
        self.notAssigned = True #1 -> not assigned
        self.adjZone = False #1 -> assigned to adjecent zone
        
        self.options = carOptions #id of possible cars
        
    def cost(self):
        if(self.notAssigned):
            return self.P1
        if(self.adjZone):
            return self.P2
        return 0
    def costNewZone(self,zone):
        #How cost for this reservation improves if the new zone is assigned
        if(self.zone==zone):
            return self.cost()-0
        elif(zone == -1):
            return self.cost()-self.P1
        else:
            return self.cost()-self.P2
    
    def overlap(self,start,end):
        if(self.start<=start<=self.end):
            return True
        if(self.start<=end<=self.end):
            return True
        if(start<=self.start<=end):
            return True
        return False
    def __str__(self):
        s = str(self.id)+ " "
        s += Reservation.resIDtoStr[self.id]
        s+=", zone: "+str(self.zone)
        s+= ", P1/P2: "+str(self.P1)+'/'+str(self.P2)
        s+= ", start/end: "+str(self.start)+'/'+str(self.end)
      
        s += " / CarOptions: ["
        for c in self.options:
            s+=str(c.id)+','
        s+=']'
        if(self.car):
            s+=str(self.car.id)
        return s
class Car:
    id = 0
    carIDtoStr = {}
    carStrtoID = {}
    zoneIDtoStr = {}
    zoneStrtoID = {}
    zoneIDtoADJ = []
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
    
    def swap(self,c2,r):
        #https://stackoverflow.com/questions/1835756/using-try-vs-if-in-python#:~:text=As%20far%20as%20the%20performance,than%20using%20if%20statement%20everytime.&text=As%20a%20general%20rule%20of,handling%20stuff%20to%20control%20flow.
        #As far as the performance is concerned, using try block for code that normally doesn’t raise exceptions is faster than using if statement everytime.
        try:
            self.res.remove(r)
            c2.res.append(r)
            if(c2.zone==r.zone):
                r.adjZone=0
            else:
                r.adjZone=1
        except:
            print("Error: swap failed")


    def costToAddr(self,nres):
        cost = nres.cost()-(self.zone!=nres.zone)*nres.P2
        if(nres.id==7):
            print("add:",nres.id,'to car',self.id,cost,end =",")
        for r in self.res:
            if(nres.id==7):
                print(nres.id,r.id)
                print(nres.start,nres.end,r.start,r.end)
            if(nres.overlap(r.start,r.end)):
                #overlap => r zou moeten worden verwijderd
                cost -= (r.P1-r.cost())
        if(nres.id==7):
            print("->",cost)
        return cost
    def add(self,nres):
        i = 0
        while(i<len(self.res)):
            r = self.res[i]
            if(nres.overlap(r.start,r.end)):
                tempr = self.res.pop(i)
                print("removed:",tempr.id)
                tempr.car = None
                tempr.notAssigned = True
                tempr.adjZone =False
                i-=1
            i+=1
        nres.car = self
        nres.notAssigned = False
        nres.adjZone = nres.zone!=self.zone
        self.res.append(nres)
    
    def costToSetZ(self,zone):
        cost = 0
        for r in self.res:
            cost += r.costNewZone(zone)
        return cost
    def setZone(self,zone):
        self.zone= zone
        i = 0
        while(i<len(self.res)):
            r = self.res[i]
            if(r.zone == zone):
                r.adjZone = False
            elif(r.zone in Car.zoneIDtoADJ[zone]):
                r.adjZone = True
            else:
                #DIT GAAT MOGELIJKS FOUT
                r.adjZone = False
                r.notAssigned = True
                r.car = None
                self.res.pop(i)
                i-=1
            i+=1
                
    def __str__(self):
        s = str(self.id)+" "
        s +=  Car.carIDtoStr[self.id]
        s += " in zone: "+str(Car.zoneIDtoStr[self.zone])
        s += " / reservations: ["
        for r in self.res:
            s+=str(r.id)+','
        s+=']'
        return s
    
class Cost:
    def getCost(lijst):#Kost berekenen
        cost=0
        for r in lijst:
            cost += r.cost()
        print("cost:",cost)
        return cost
        
    def comp(a,b):#kijken wat het verschil zou zijn voor een swap
        kostA=a.notAssigned*a.P1 + a.adjZone*a.P2
        kostB=b.notAssigned*b.P1 + b.adjZone*b.P2
        verschil= kostB-kostA
        print( 'vershil:', verschil)
        return verschil
    
