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
class Code:
    memCount = 0
    #passedCodes = [] #split single list of all passed codes into dictionary of lists divided based on len(code)
    passedCodesPerL = {}
    passedCodes = set()
    def formCode():
        rcode,ccode = [],[]
        for r in State.rlist:
            rcode.append(r.code())
        for c in State.cars:
            ccode.append(c.code())
        return [rcode,ccode]
    def add():
        ncode = Code.formCode() 
        State.curcode = ncode
        if(Code.inMemory(ncode)):
            return 0
    
        #which-is-faster-hash-lookup-or-binary-search
        #https://stackoverflow.com/questions/360040/which-is-faster-hash-lookup-or-binary-search
        #test: set 173 sec, array + binary search : 141 sec
        #binary search without splitting codes in dictionary: 156 sec
        c = Code.codeToStr(ncode)
        
        Code.passedCodes.add(c)
        return 1
        
        lenC = len(c)
        if(lenC in Code.passedCodesPerL):
            #Code.passedCodesPerL[lenC].append(c)
            bisect.insort(Code.passedCodesPerL[lenC], c) 
        else:
            Code.passedCodesPerL[lenC] = []
            Code.passedCodesPerL[lenC].append(c)  
        return 1
      
    def codeToStr(code):
        s = ''
        for r in code[0]:
            if(r == 'x'):
                s+="x"
            else:
                s+=str(r)
 
        for c in code[1]:
            s+=str(c)

        return s
    def find(L, target):
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
 
        codeString = Code.codeToStr(code)
        if(codeString in Code.passedCodes):
            return True
        else:
            return False
        
        lenCodeString = len(codeString)
        if(not(lenCodeString in Code.passedCodesPerL)):
            return False # No other codes of this length
        if(Code.find(Code.passedCodesPerL[lenCodeString],codeString)):
            Code.memCount += 1
            return True # Code found in memory
        else:
            return False

if __name__ == "__main__":
    pass
