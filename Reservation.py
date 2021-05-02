from State import State
class Reservation:
    id = 0
    resIDtoStr = {}
    zoneIDtoADJ = {}
    def __init__(self,zone,day,start,duration,P1,P2,inc = 1):
        self.id = Reservation.id
        Reservation.id += inc
        self.carID = -1
        self.zone = zone
        if(day!=-1):
            self.start = int(day)*1440+int(start) #convert to minutes (24*60 minutes per day)
            self.end = self.start + int(duration) #cast day, start, duration from txt to int
        self.P1 = P1  # cost for not assigning Reservation
        self.P2 = P2  # cost for assigning to adjecent zone
        
        self.notAssigned = True #True -> not assigned
        self.adjZone = False    #True -> assigned to adjecent zone

    def clone(self):
        cloneRes = Reservation(self.zone,-1,self.start,-1,self.P1,self.P2,inc = 0)
        cloneRes.notAssigned = self.notAssigned
        cloneRes.adjZone = self.adjZone

        cloneRes.start = self.start
        cloneRes.end = self.end
        
        cloneRes.carID = self.carID
        cloneRes.id = self.id
        return cloneRes
    def getCar(self):
        if(self.carID == -1):
            return None
        return State.cars[self.carID]
    #_functions: Function call takes longer than the function itself
    def _setCar(self,car):
        self.carID = car

    def _cost(self):
        return self.notAssigned*self.P1 + self.adjZone*self.P2
    
    def costNewZone(self,zone):
        #How the cost for this reservation improves if the new zone is assigned
        if(self.zone==zone):
            return self.notAssigned*self.P1 + self.adjZone*self.P2  -   0
            
        elif(self.zone in Reservation.zoneIDtoADJ[zone]):
            return self.notAssigned*self.P1 + self.adjZone*self.P2  -   self.P2
            
        else:
            return self.notAssigned*self.P1 + self.adjZone*self.P2  -   self.P1
    
    def _overlap(self,start,end):
        return (self.start < end and start < self.end)

    def _code(self):
        if(self.carID == -1):#None
            return 'x'
        return self.carID
    
    def __str__(self):
        s = str(self.id)+ " "
        s += Reservation.resIDtoStr[self.id]
        s+=", zone: "+str(self.zone)
        s+= ", P1/P2: "+str(self.P1)+'/'+str(self.P2)
        s+= ", s/e: "+str(self.start)+'/'+str(self.end)
        s+=str(self.carID)
        return s
  
if __name__ == "__main__":
    pass
