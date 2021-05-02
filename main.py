import sys

from readCSV import readCSV
from writeCSV import writeCSV
from Car import Car
from Reservation import Reservation
from Cost import Cost
from Tabu import Tabu
from tabu_search import Tabu_Search
from simulated_annealing import Simulated_Annealing
from great_deluge import Great_deluge
from State import State

class Solver:
    def __init__(self,f,maxtime, random_seed):
        self.maxtime = maxtime
        self.f = f

        self.simulated_annealing = Simulated_Annealing(self.maxtime,random_seed)
        self.tabu_search = Tabu_Search(self.maxtime-(self.maxtime))   
       
        
        self.sorted_rlist = []
        for e in State.rlist:
            index = 0
            for i in self.sorted_rlist:
                if(e.P1>i.P1):
                    break
                index+=1
            self.sorted_rlist.insert(index,e)

    def freeData(self):
        for r in State.rlist:
            r.car = None
            r.notAssigned=True
            r.adjZone=False
        for c in State.cars:
            c.res=[]

    def initialSolution(self):
        # Voor elke r:
        #   Not assigned -> Look for car in the right zone -> no overlap? -> add r
        #   Not assigned -> Look for car in the adjecent zone -> no ovlerap -> add r
        #   If a car has no reservations yet -> move car to r.zone and add r
        
        #order by r.id(State.rlist)             : #32690 -> 15290
        #ordered by P1(self.sorted_rlist): #32690 -> 12360 
        for r in self.sorted_rlist:
            if(r.notAssigned):
                for cid in State.options[r.id]:
                    c = State.cars[cid]
                    if(not(c.overlap(r.start,r.end)) and (c.zone == r.zone or c.zone in Car.zoneIDtoADJ[r.zone])):
                        c.addR(r)
                        break   
                    elif(len(c.res)==0):#No other reservations so no problem
                        c.setZone(r.zone)
                        c.addR(r)
                        break

        for r in self.sorted_rlist:                
            if(r.adjZone):
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.zone == r.zone)):
                            c.addR(r)
                            break       
                        elif(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
                            
def main(argTime,argFile,argFileOut,argSeed):
    State.cars, State.rlist,State.options,State.zones = readCSV(Car,Reservation,argFile)#Read data from csv file
    State.RassignCount = [0]*len(State.rlist)
    
    solver = Solver(argFile,argTime,argSeed)
    solver.freeData()#Initialize empty solution
   
    print("Empty solution cost:",Cost.getCost(State.rlist))
    solver.initialSolution()
    print("Initial solution cost:",Cost.getCost(State.rlist))
    State.curCost = Cost.getCost(State.rlist)
    
    print("----------------"*2)#Choose Method
    solver.simulated_annealing.simulatedAnnealing()
    #solver.tabu_search.Tabu_Search()
    print("----------------"*2)

    print(Cost.getCost(State.resultRlist))
    writeCSV(argFileOut)
    
def oneTime():
    argFile=sys.argv[1]
    argFileOut=sys.argv[2]
    argTime=int(sys.argv[3])
    argSeed=int(sys.argv[4])
    argThreads=int(sys.argv[5])#unused
    
    main(argTime,argFile,argFileOut,argSeed)

def resetAll():
    Reservation.id = 0
    Car.id = 0
    State.reset()
    Tabu.tabuList = set()

    
if __name__ == "__main__":
    oneTime()
 
  

    
        
