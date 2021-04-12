from State import State
class Reservation:
    id = 0
    resIDtoStr = {}
    zoneIDtoADJ = {}
    def __init__(self,zone,day,start,duration,P1,P2,inc = 1):
        self.id = Reservation.id
        Reservation.id += inc
        self.carID = -1#None
        self.zone = zone
        if(day!=-1):
            self.start = int(day)*1440+int(start) #convert to minutes (24*60 minutes per day)
            self.end = self.start + int(duration) #cast day, start, duration from txt to int
        self.P1 = P1  # cost for not assigning Reservation
        self.P2 = P2  # cost for assigning to adjecent zone
        
        self.notAssigned = True #1 -> not assigned
        self.adjZone = False #1 -> assigned to adjecent zone

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
        #return self.car
    
    def setCar(self,car):
        self.carID = car

    def cost(self):
        return self.notAssigned*self.P1 + self.adjZone*self.P2

    def costNewZone(self,zone):
        #How the cost for this reservation improves if the new zone is assigned
        if(self.zone==zone):
            return self.cost()-0
        elif(self.zone in Reservation.zoneIDtoADJ[zone]):
            return self.cost()-self.P2
        else:
            return self.cost()-self.P1
    
    def overlap(self,start,end):
        #https://stackoverflow.com/questions/13513932/algorithm-to-detect-overlapping-periods
        return (self.start < end and start < self.end)

    
    def code(self):
        
        if(self.carID == -1):#None
            return 'x'
        return self.carID
        #return self.car
    """
    def __str__(self):
        s = str(self.id)+ " "
        s += Reservation.resIDtoStr[self.id]
        s+=", zone: "+str(self.zone)
        s+= ", P1/P2: "+str(self.P1)+'/'+str(self.P2)
        s+= ", s/e: "+str(self.start)+'/'+str(self.end)
        s += " / len(CarOptions):"+ str(len(self.options))+" assign to: "
        if(self.car):
            s+=str(self.car)#.id)
        return s
    """
if __name__ == "__main__":
    pass
