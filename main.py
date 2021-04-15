import glob
import copy
import time

import sys
#
from readCSV import readCSV
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
        State.cars, State.rlist,State.options = readCSV(Car,Reservation,self.f)
        
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
        Code.add()
        
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
                        if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
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


def main(argTime,argFile):
    solver = Solver(argFile,argTime)
    #Printer.printDict(Car)
    
    Solver.initialSolution()
    #Printer.printResult(solver.rlist,solver.cars)
    solver.setBest()
    Code.add()
    print("----------------"*2)    
    #startTemperature, endTemperature, first num of iterations, increase factor, coolingrate
    solver.simulated_annealing.simulatedAnnealing(10000, 0, 2, 1, 0.99)
    #solver.tabu_search.findSolution()
    #solver.Iterated_Tabu.findSolution()
    #solver.tabu_search.VariableNeighbourhoud()
    
    #solver.simulated_annealing.simulatedAnnealing()
    
    #solver.bestrlist , solver.bestcars = solver.great_deluge.staydry(Cost.getCost(State.rlist)/20)
    print("----------------"*2)
    
    solver.bestCost = State.getBest()
    print(Cost.getCost(solver.bestrlist))
    # Printer.printResult(solver.bestrlist,solver.cars)
    writeCSV(solver.f)
    Printer.printFinal(solver,Code)
    
  
if __name__ == "__main__":
    argTime=int(sys.argv[1])
    argFile=sys.argv[2]
    #argTime=300
    #argFile='./csv/100_5_14_25.csv'
    main(argTime,argFile)
    
