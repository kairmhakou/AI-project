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


class Solver:
    def __init__(self,f,maxtime, random_seed = 10):
        self.maxtime = maxtime
        print(maxtime)
        self.f = f
        self.cars, self.rlist = readCSV(Car,Reservation,self.f)
        
        self.tabu_search = Tabu_Search(self)
        self.simulated_annealing = Simulated_Annealing(self,Code,Car)
        
        
        
        self.sorted_rlist = []
        for e in self.rlist:
            index = 0
            for i in self.sorted_rlist:
                if(len(e.options)<len(i.options)):
                    break
                index+=1
            self.sorted_rlist.insert(index,e)
        
        self.bestCost = None
        self.bestcars = None
        self.bestrlist = None
        
        #base state of solution
        self.curcode = Code.formCode(self)
        Code.add(self.curcode)
        
    def freeData(self):
        for r in self.rlist:
            r.car = None
            r.notAssigned=True
            r.adjZone=False
        for c in self.cars:
            c.res=[]
            
    def setBest(self,):
        cost = Cost.getCost(self.rlist)
        self.bestCost = cost
        self.bestcars = copy.deepcopy(self.cars)
        self.bestrlist = copy.deepcopy(self.rlist)
        # print("SetnewBest",cost) #uncomment this
    def getBest(self):
        return self.bestCost
        
    def initialSolution(self,most_strict):
        if(most_strict):
            l = self.sorted_rlist
        else:
            l = self.rlist
        for r in l:
            if(r.notAssigned):
                for c in r.options:
                        if(not(c.overlap(r.start,r.end)) and (c.inZone(r))):
                            c.addR(r)
                            break   
        for r in l:                
            if(r.notAssigned):#could not be assigned to any car
                for c in r.options:
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
        for r in l:                
            if(r.adjZone):#could not be assigned to any car
                for c in r.options:
                        if(not(c.overlap(r.start,r.end)) and (c.zone ==r.zone)):
                            c.addR(r)
                            break
            if(r.adjZone):#could not be assigned to any car
                for c in r.options:               
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break

    
def main(argTime,argFile):
    solver = Solver(argFile,argTime)
    Printer.printDict(Car)
    
    solver.initialSolution(1)
    Printer.printResult(solver.rlist,solver.cars)
    solver.setBest()
    
    print("----------------"*2)
    
    #solver.tabu_search.findSolution()
    # solver.bestrlist,solver.bestcars = solver.tabu_search.findSolution2()
    
    solver.bestrlist , solver.bestcars =solver.simulated_annealing.simulatedAnnealing()
    
    print("----------------"*2)
    
    solver.bestCost = Cost.getCost(solver.bestrlist)
    print(Cost.getCost(solver.bestrlist))
    # Printer.printResult(solver.bestrlist,solver.cars)
    writeCSV(solver,Car)
    Printer.printFinal(solver,Code)
    
  
if __name__ == "__main__":
    # argTime=int(sys.argv[1])
    # argFile=sys.argv[2]
    argTime=200000000000000000000000000000
    argFile='./csv/toy1.csv'
    main(argTime,argFile)
    