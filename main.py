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
from Printer import Printer
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
        """
        self.sorted_rlist = []
        for e in self.rlist:
            index = 0
            for i in self.sorted_rlist:
                if(len(self.options[e.id])<len(self.options[i.id])):
                    break
                index+=1
            self.sorted_rlist.insert(index,e)"""

    def freeData(self):
        for r in State.rlist:
            r.car = None
            r.notAssigned=True
            r.adjZone=False
        for c in State.cars:
            c.res=[]

    def initialSolution():
        for r in State.rlist:
            if(r.notAssigned):
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.zone == r.zone or c.zone in Car.zoneIDtoADJ[r.zone])):
                            c.addR(r)
                            break   
        for r in State.rlist:                
            if(r.notAssigned):#could not be assigned to any car
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
        for r in State.rlist:                
            if(r.adjZone):#could not be assigned to any car
                for cid in State.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.zone ==r.zone)):
                            c.addR(r)
                            break
            if(r.adjZone):#could not be assigned to any car
                for cid in State.options[r.id]:    
                        c = State.cars[cid]           
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
        

def main(argTime,argFile,fileNum):
    State.cars, State.rlist,State.options,State.zones = readCSV(Car,Reservation,argFile)
    State.RassignCount = [0]*len(State.rlist)
    
    solver = Solver(argFile,argTime)
    solver.freeData()
    Solver.initialSolution()

    print("----------------"*2)#Choose Method
    
    #solver.simulated_annealing.simulatedAnnealing()
    
    #solver.Iterated_Tabu.Iterated_local_search()
    #solver.Iterated_Tabu.Tabu_Search_base()
    
    solver.tabu_search.Iterated_local_search()

    # solver.great_deluge.staydry(Cost.getCost(State.rlist)/20)
    
    print("----------------"*2)

    print(Cost.getCost(State.resultRlist))
    writeCSV(argFile,fileNum)
    #Printer.printFinal()
    
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
 
  

    
        
