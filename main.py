import glob
import copy
import time

import sys
#
from readCSV import readCSV , average
from writeCSV import writeCSV
from Car import Car
from Reservation import Reservation
from Cost import Cost
from Code import Code
from Printer import Printer
from tabu_search import Tabu_Search
from Iterated_Tabu import Iterated_Tabu
from simulated_annealing import Simulated_Annealing
from great_deluge import Great_deluge
from State import State

class Solver:
    def __init__(self,f,maxtime, random_seed = 10):
        self.maxtime = maxtime
        print(maxtime)
        self.f = f
        print(f)
        State.cars, State.rlist,State.options,State.zones = readCSV(Car,Reservation,self.f)
        
        self.tabu_search = Tabu_Search(self)
        self.Iterated_Tabu = Iterated_Tabu(self)
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
        self.bestCost = None
        self.bestcars = None
        self.bestrlist = None
        
        #base state of solution
        Code.add(Code.formCode() )
        
    def freeData(self):
        for r in State.rlist:
            r.car = None
            r.notAssigned=True
            r.adjZone=False
        for c in State.cars:
            c.res=[]
            
    def setBest(self):
        cost = Cost.getCost(State.rlist)
        self.bestCost = cost
        self.bestcars = copy.deepcopy(State.cars)
        self.bestrlist = copy.deepcopy(State.rlist)

        print("SetnewBest",cost) 
    def getBest(self):
        return self.bestCost
        
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
    solver = Solver(argFile,argTime)
    #Printer.printDict(Car)
    
    Solver.initialSolution()
    #Printer.printResult(solver.rlist,solver.cars)
    solver.setBest()
    Code.add(Code.formCode() )
    print("----------------"*2)    
    
    solver.simulated_annealing.simulatedAnnealing()
    
    #solver.Iterated_Tabu.Iterated_local_search()
    #solver.Iterated_Tabu.Tabu_Search_base()
    
    #solver.tabu_search.findSolution()
    #solver.tabu_search.VariableNeighbourhoud()

    
    #solver.bestrlist , solver.bestcars = solver.great_deluge.staydry(Cost.getCost(State.rlist)/20)
    print("----------------"*2)
    
    solver.bestCost = State.result
    print(Cost.getCost(solver.bestrlist))
    # Printer.printResult(solver.bestrlist,solver.cars)
    
    writeCSV(solver.f,fileNum)
    Printer.printFinal(solver,Code)
    
def oneTime():
    argTime=int(sys.argv[1])
    argFile=sys.argv[2]
    main(argTime,argFile ,  1)
def averageX():
    rond =0
    fileNum= 0
    
    argTime=int(sys.argv[1])
    argFile=sys.argv[2]
    while(rond <50):
        Reservation.id =0
        Car.id =0
        State.reset()
        averageCost, bestCost, bestCsvNum = average(argFile,rond) 
        print('average cost ',averageCost, ', best cost ', bestCost, ' best csv ' , bestCsvNum)
        Car.zoneIDtoADJ=[]
        fileNum+=1
        main(argTime,argFile , fileNum)
        rond+=1
    averageCost, bestCost, bestCsvNum = average(argFile,rond) 
    file1 = open("averages.txt","a")#write mode
    string = 'average cost '+str(averageCost)+ ', best cost '+str(bestCost)+ ' best csv ' + str(bestCsvNum)
    file1.write(string+"\n")
    file1.close()
    
    #the average of the costs generated from simulated annealing alogrithm 
    
if __name__ == "__main__":
    #oneTime()
    averageX() 
 
  

    
        
