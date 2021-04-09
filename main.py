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
from simulated_annealing import Simulated_Annealing
from great_deluge import Great_deluge
from State import State
class Methods():
    def __init__(self,solver):
        self.tabu_search = Tabu_Search(solver)
        self.simulated_annealing = Simulated_Annealing(solver,Code,Car)
        self.great_deluge = Great_deluge(solver)
class Solver:
    def __init__(self,f,maxtime, random_seed = 10):
        self.maxtime = maxtime
        print(maxtime)
        self.f = f
        self.cars2, self.rlist2,self.options = readCSV(Car,Reservation,self.f)
        State.cars = self.cars2
        State.rlist = self.rlist2
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
        Code.add(self)
        
    def createCopy(self):
        copySolver = Solver(self.f,self.maxtime)
        copySolver.cars = copy.deepcopy(self.cars)#[copy.deepcopy(c) for c in self.cars]        
        copySolver.rlist = copy.deepcopy(self.rlist)#[copy.deepcopy(r) for r in self.rlist] 

        copySolver.options = self.options
        copySolver.bestCost = self.bestCost
        return copySolver
    def freeData(self):
        for r in State.rlist:
            r.car = None
            r.notAssigned=True
            r.adjZone=False
        for c in self.cars:
            c.res=[]
            
    def setBest(self):
        cost = Cost.getCost(State.rlist)
        self.bestCost = cost
        self.bestcars = copy.deepcopy(State.cars)
        self.bestrlist = copy.deepcopy(State.rlist)

        print("SetnewBest",cost) 
    def getBest(self):
        return self.bestCost
        
    def initialSolution(self):
        for r in State.rlist:
            if(r.notAssigned):
                for cid in self.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
                            c.addR(r)
                            break   
        for r in State.rlist:                
            if(r.notAssigned):#could not be assigned to any car
                for cid in self.options[r.id]:
                        c = State.cars[cid]
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
        for r in State.rlist:                
            if(r.adjZone):#could not be assigned to any car
                for cid in self.options[r.id]:
                        c = State.cars[cid]
                        if(not(c.overlap(r.start,r.end)) and (c.zone ==r.zone)):
                            c.addR(r)
                            break
            if(r.adjZone):#could not be assigned to any car
                for cid in self.options[r.id]:    
                        c = State.cars[cid]           
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break


def main(argTime,argFile):
    solver = Solver(argFile,argTime)
    methods = Methods(solver)
    Printer.printDict(Car)
    
    solver.initialSolution()
    #Printer.printResult(solver.rlist,solver.cars)
    solver.setBest()
    Code.add(solver)
    print("----------------"*2)    
    
    solver.bestrlist,solver.bestcars = methods.tabu_search.findSolution()
    #solver.bestrlist,solver.bestcars = methods.tabu_search.VariableNeighbourhoud()
    
    #solver.bestrlist , solver.bestcars =methods.simulated_annealing.simulatedAnnealing()
    
    #methods.great_deluge.staydry(Cost.getCost(solver.rlist)/20)
    print("----------------"*2)
    
    solver.bestCost = Cost.getCost(solver.bestrlist)
    print(Cost.getCost(solver.bestrlist))
    # Printer.printResult(solver.bestrlist,solver.cars)
    writeCSV(solver,Car)
    Printer.printFinal(solver,Code)
    
  
if __name__ == "__main__":
    argTime=int(sys.argv[1])
    argFile=sys.argv[2]
    #argTime=300
    #argFile='./csv/210_5_33_25.csv'
    main(argTime,argFile)
    
