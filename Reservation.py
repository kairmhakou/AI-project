class Reservation:
    id = 0
    resIDtoStr = {}
    zoneIDtoADJ = {}
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
        #How the cost for this reservation improves if the new zone is assigned
        if(self.zone==zone):
            return self.cost()-0
        elif(self.zone in Reservation.zoneIDtoADJ[zone]):
            return self.cost()-self.P2
        else:
            return self.cost()-self.P1
    
    def overlap(self,start,end):
        if(self.start<=start<=self.end):
            return True
        if(self.start<=end<=self.end):
            return True
        if(start<=self.start<=end):
            return True
        return False
    def code(self):
        if(self.car == None):
            return 'x'
        return self.car.id
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

