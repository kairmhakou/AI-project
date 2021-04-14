# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: dehan
"""

"""
To Do: Vervang bisect.insort door gwn een loop 
"""
import bisect  
from State import State
import time
class Code:
    memCount = 0
    #passedCodes = [] #split single list of all passed codes into dictionary of lists divided based on len(code)
    passedCodesPerL = {}
    passedCodes = set()
    
    timeSpentForm = 0
    countForm = 1
    
    timeSpentAdd = 0
    countAdd = 1
    
    timeSpentStr = 0
    countStr = 1
    
    timeSpentFind = 0
    countFind = 1
    
    timeSpentIn = 0
    countIn = 1
  
    def printTimes():
        print("Formcode:",Code.timeSpentForm,Code.timeSpentForm/Code.countForm)
        print("Add:",Code.timeSpentAdd,Code.timeSpentAdd/Code.countAdd)
        print("ToStr:",Code.timeSpentStr,Code.timeSpentStr/Code.countStr)
        print("Find:",Code.timeSpentFind,Code.timeSpentFind/Code.countFind)
        print("InMemeory:",Code.timeSpentIn,Code.timeSpentIn/Code.countIn)
        
    def formCode():
        tempStart = time.perf_counter()
        Code.countForm += 1
                    
        rcode,ccode = [],[]
        for r in State.rlist:
            rcode.append(r.code())
        for c in State.cars:
            ccode.append(c.code())
            
        Code.timeSpentForm += time.perf_counter()-tempStart   
        return [rcode,ccode]
    def add():
        tempStart = time.perf_counter()
        Code.countAdd += 1
        
        ncode = Code.formCode() 
        State.curcode = ncode
        if(Code.inMemory(ncode)):
            Code.timeSpentAdd += time.perf_counter()-tempStart  
            return 0
        c = Code.codeToStr(ncode)
        #which-is-faster-hash-lookup-or-binary-search
        #https://stackoverflow.com/questions/360040/which-is-faster-hash-lookup-or-binary-search
        #test: set 173 sec, array + binary search : 141 sec
        #binary search without splitting codes in dictionary: 156 sec
        
        
        """
        Code.passedCodes.add(c)
        Code.timeSpentAdd += time.perf_counter()-tempStart  
        return 1
        """
        lenC = len(c)
        if(lenC in Code.passedCodesPerL):
            Code.passedCodesPerL[lenC].add(c)
            #bisect.insort(Code.passedCodesPerL[lenC], c) 
        else:
            Code.passedCodesPerL[lenC] = set()
            Code.passedCodesPerL[lenC].add(c)  
        return 1
      
    def codeToStr(code):
        tempStart = time.perf_counter()
        Code.countStr += 1
        s = ''
        for r in code[0]:
            if(r == 'x'):
                s+="x"
            else:
                s+=str(r)
 
        for c in code[1]:
            s+=str(c)

        Code.timeSpentStr += time.perf_counter()-tempStart  
        return s
    def find(L, target):
        tempStart = time.perf_counter()
        Code.countFind += 1
        #binary search trough list
        start = 0
        end = len(L) - 1
        while start <= end:
            middle = int((start + end)/ 2)
            midpoint = L[middle]
            if midpoint > target:
                end = middle - 1
            elif midpoint < target:
                start = middle + 1
            else:
                Code.timeSpentFind += time.perf_counter()-tempStart  
                return midpoint
    def inMemory(code):
        """
        op basis van de lengtes moet er vaak niet eens gezocht worden door de memory
            De code bestaat uit ids
            De id's kunnen elk 1/2/3 lang zijn
            Voor elk van de 360 reservaties staat er een id in de code
            => lage kans dat twee verschillende code dezelfde lengte hebben
        => moeten meestal niet zoeken door een lijst van duizende code
        """
        tempStart = time.perf_counter()
        Code.countIn += 1
        codeString = Code.codeToStr(code)
        """
        
        if(codeString in Code.passedCodes):
            Code.timeSpentIn += time.perf_counter()-tempStart  
            return True
        else:
            Code.timeSpentIn += time.perf_counter()-tempStart  
            return False
        """
        lenCodeString = len(codeString)
        if(not(lenCodeString in Code.passedCodesPerL)):
            return False # No other codes of this length
        if(codeString in Code.passedCodesPerL[lenCodeString]):#(Code.find(Code.passedCodesPerL[lenCodeString],codeString)):
            Code.memCount += 1
            Code.timeSpentIn += time.perf_counter()-tempStart  
            return True # Code found in memory
        else:
            Code.timeSpentIn += time.perf_counter()-tempStart  
            return False

if __name__ == "__main__":
    pass
