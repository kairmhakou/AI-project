import glob
import copy
import time
#
from readCSV import readCSV
from writeCSV import writeCSV
from Car import Car
from Reservation import Reservation
from Cost import Cost
from Code import Code
from Printer import Printer


class Solver:
    def __init__(self,f,maxtime = 300, random_seed = 10):

        self.maxtime = maxtime
        self.f = f
        self.cars, self.rlist = readCSV(Car,Reservation,'./csv/'+self.f+'.csv')
        
        self.sorted_rlist = []
        
        """
        #niet nuttig
        self.overlaps = []
        for r in self.rlist:
            o = []
            for r2 in self.rlist:
                if(r.id != r2.id):
                    if(r.overlap(r2.start,r2.end)):
                        o.append(r2)
            self.overlaps.append(o)
        """

        
        
        
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
            if(r.notAssigned):#could not be assigned to any car
                for c in r.options:
                        if(len(c.res)==0):#No other reservations so no problem
                            c.setZone(r.zone)
                            c.addR(r)
                            break
    
    def setBest(self):
        cost = Cost.getCost(self.rlist)
        self.bestCost = cost
        self.bestcars = copy.deepcopy(self.cars)
        self.bestrlist = copy.deepcopy(self.rlist)
      
    def steepest_descent(self):
        bestc = None
        bestz = None
        bestr = None
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in self.rlist:
            for c in r.options:
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        nextcode = copy.deepcopy(self.curcode)
                        
                        
                        for tempr in c.res:
                            if(r.overlap(tempr.start,tempr.end)):

                                #overlap => r zou moeten worden verwijderd
                                nextcode[0][tempr.id]='x'
                        nextcode[0][r.id]=c.id
                        if(Code.inMemory(nextcode)):
                            continue
                        best = cost
                        bestc = c
                        bestr = r
            
        #All sensible 'car zone' swaps
        for c in self.cars:
            for r in c.res:
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    
                    
                    nextcode = copy.deepcopy(self.curcode)
                    nextcode[1][c.id] = r.zone 
                    for tempr in c.res:
                        if(tempr.zone == r.zone):
                            pass
                        elif(tempr.zone in Car.zoneIDtoADJ[r.zone]):
                            pass
                        else:
                            nextcode[0][tempr.id]='x'
                    if(Code.inMemory(nextcode)):
                        continue
                    
                    
                    best = cost
                    bestc = c
                    bestz = r.zone
                    #print(bestc.id,best,bestz)
        return bestc,bestz,bestr
    def hill_climbing(self):
        best = 0 #verbetering >0
        #All possible 'assigned car' swaps
        for r in self.rlist:
            for c in r.options:
                if(r.zone == c.zone or r.zone in Car.zoneIDtoADJ[c.zone]):    
                    cost =  Cost.costToAddR(c,r)
                    if(cost>best):
                        nextcode = copy.deepcopy(self.curcode)
                        for tempr in c.res:
                            if(r.overlap(tempr.start,tempr.end)):
                                #overlap => r zou moeten worden verwijderd
                                nextcode[0][tempr.id]='x'
                        nextcode[0][r.id]=c.id
                        if(Code.inMemory(nextcode)):
                            continue
                        return c,None,r
            
        #All sensible 'car zone' swaps
        for c in self.cars:
            for r in c.res:
                cost =  Cost.costToSetZone(c,r.zone)
                #print("zoneCost:",cost)
                if(cost>best):
                    
                    nextcode = copy.deepcopy(self.curcode)
                    nextcode[1][c.id] = r.zone 
                    for tempr in c.res:
                        if(tempr.zone == r.zone):
                            pass
                        elif(tempr.zone in Car.zoneIDtoADJ[r.zone]):
                            pass
                        else:
                            nextcode[0][tempr.id]='x'
                    if(Code.inMemory(nextcode)):
                        continue
                    return c,r.zone,None
        return None,None,None

    def localSearch(self,Cost):

        count = 0
        while(1):
            count += 1
            #pick one of the local search methods
            #bestc,bestz,bestr = self.hill_climbing()
            bestc,bestz,bestr = self.steepest_descent()
            
            if(bestz is not None):
                bestc.setZone(bestz)
            elif(bestr is not None):
                if(bestr.car):#if currently assigned to a car, remove from list
                    bestr.car.res.remove(bestr)
                #assign to new car
                bestc.addR(bestr)
            else:
                #reached peak
                return count
            
            #removing the following improves speed decreases result
            code = Code.formCode(self) 
            self.curcode = code
            if(Code.inMemory(code)):
                print("iets fout met nextcode in localSearch")
            else:
                Code.add(code)
    def findSolution(self):
        i = 0
        start = time.perf_counter()
        while(1):
            
                            
            if((time.perf_counter()-start) > self.maxtime):
                print('~~timeisup~~')
                break   #return because the time is up
            i+=1
            count = self.localSearch(Cost)
            cost = Cost.getCost(self.rlist)
            if(i%100==0):
                print(i,':',cost,count,self.bestCost)
            if(cost<self.bestCost):
                print("newBest",cost)
                self.setBest()
                
            
            changed = self.forceAssign()
            if(not(changed)):
                print("No more changes after:",i)
                break
            
            
    def forceAssign(self):
        minL = 99999999999
        bestc = None
        bestr = None
        for r in self.rlist:
            if(r.notAssigned):
                for c in r.options:
                    if(len(c.res)<minL):
                        nextcode = copy.deepcopy(self.curcode)
                        #addR and setZone will remove conflicts: r not in zone/adjZone, overlap
                        for tempr in c.res:
                            #tempr not in zone/adjZone
                            if(not(tempr.zone == r.zone or tempr.zone in Car.zoneIDtoADJ[r.zone])):
                                nextcode[0][tempr.id] = 'x' #r can no longer assigned
                            #overlap
                            elif(r.overlap(tempr.start,tempr.end)):
                                nextcode[0][tempr.id] = 'x'
                        
                        nextcode[0][r.id] = c.id #r would be assign to c (addR)
                        nextcode[1][c.id] = r.zone #c would be placed in r's zone (setZone)
                        if(Code.inMemory(nextcode)):
                            continue

                        minL = len(c.res)
                        bestc = c
                        bestr = r
        if(bestr):                
            bestc.setZone(bestr.zone)
            bestc.addR(bestr)
            code = Code.formCode(self)
            self.curcode = code
            if(Code.inMemory(code)):
                print("iets fout met nextcode in forceAssign")
            else:
                Code.add(code)
            
            return 1
        else:
                
            print("No Forced assign")
            return 0
    
    def heuristiek(self):
        """
        @Karim zet hier u code voor de heuristiek 
        en vervang forceAssign self.forceAssign in findSolution met deze functie
        om te testen
    
        """
        pass
    
def main(f):
    solver = Solver(f)
    Printer.printDict(Car)
    
    solver.initialSolution(1)
    Printer.printResult(solver.rlist,solver.cars)
    solver.setBest()
    
    print("----------------"*2)
    print("\ni,cost,swaps,bestCost")
    solver.findSolution()
    
    writeCSV(solver,Car)
    Printer.printFinal(solver,Code)
    
  
if __name__ == "__main__":
    """
    Parameters inlezen ideaal iets met config
    
    """
    arr = glob.glob(".\csv\*.csv")
    print('options:')
    i = 0
    filenames = []
    for f in arr:
        file = f.split('\\')[-1]
        filenames.append(file.split('.')[0])
        print(i,":",filenames[i])
        i+=1
        
    fnr = int(input("Choose file nr: "))
    f = filenames[fnr]
    start_time = time.perf_counter()
    main(f)
    print("--- %s seconds ---" % (time.perf_counter() - start_time))