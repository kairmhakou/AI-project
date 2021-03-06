import glob
import copy
import time
import sys

from readCSV import readCSV , average
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
    def __init__(self,f,maxtime, random_seed = 10):
        self.maxtime = maxtime
        self.f = f

        self.tabu_search = Tabu_Search(self)
        self.simulated_annealing = Simulated_Annealing(self.maxtime)
        self.great_deluge = Great_deluge(self)
        
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
        #   Not assigned -> kijk of er een auto in juiste zone staat -> geen overlap? -> add
        #   Not assigned -> kijk of er een auto in adj zone staat -> geen ovlerap -> add
        #   Kijk of er een auto nog geen reservaties heeft -> verplaats auto naar r.zone en add
        
        #Volgorde r.id(State.rlist)             : #32690 -> 15290
        #Volgorde grootste P1(self.sorted_rlist): #32690 -> 12360 
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
                            
def main(argTime,argFile,fileNum):
    State.cars, State.rlist,State.options,State.zones = readCSV(Car,Reservation,argFile)
    State.RassignCount = [0]*len(State.rlist)
    
    solver = Solver(argFile,argTime)
    solver.freeData()
   
    print("Pre-initial cose:",Cost.getCost(State.rlist))
    solver.initialSolution()
    print("initial cose:",Cost.getCost(State.rlist))
    State.curCost = Cost.getCost(State.rlist)
    print("----------------"*2)#Choose Method
    
    #solver.simulated_annealing.simulatedAnnealing()
    solver.tabu_search.Tabu_Search()
    
    #solver.tabu_search.random_restart()#unused
    #solver.tabu_search.Tabu_Search_base()#unused
    
    # solver.great_deluge.staydry(Cost.getCost(State.rlist)/20)#unused
    
    print("----------------"*2)

    print(Cost.getCost(State.resultRlist))
    writeCSV(argFile,fileNum)
    
def oneTime():
    argTime=int(sys.argv[1])
    argFile=sys.argv[2]
    main(argTime,argFile,1)

def resetAll():
    Reservation.id = 0
    Car.id = 0
    State.reset()
    
    Tabu.tabuList = set()
def averageX():
    fileNum = 0
    
    argTime=int(sys.argv[1])
    argFile=sys.argv[2]
    while(fileNum < 5):
        resetAll()
        averageCost, bestCost, bestCsvNum = average(argFile,fileNum) 
        print('average cost ',averageCost, ', best cost ', bestCost, ' best csv ' , bestCsvNum)
        Car.zoneIDtoADJ=[]
        fileNum+=1
        main(argTime,argFile , fileNum)

    averageCost, bestCost, bestCsvNum = average(argFile,fileNum) 
    print('average cost ',averageCost, ', best cost ', bestCost, ' best csv ' , bestCsvNum)
    averages = open("averages.txt","a")#write mode
    string = 'average cost '+str(averageCost)+ ', best cost '+str(bestCost)+ ' best csv ' + str(bestCsvNum)
    averages.write(string+"\n")
    averages.close()

    
if __name__ == "__main__":
    oneTime()
    #averageX() 
 
  

    
        
