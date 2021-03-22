# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: dehan
"""
import bisect 
class Code:
    #passedCodes = []
    passedCodesPerL = {}
    def formCode(rlist,cars,cost=0):
        ccode = []
        rcode = []
        for r in rlist:
            rcode.append(r.code())
        for c in cars:
            ccode.append(c.code())
        return [rcode,ccode,cost]
    def add(ncode):
        c = Code.codeToStr(ncode)
        lenC = len(c)
        #plaat op juiste plaats (gesorteerd)
        #bisect.insort(Code.passedCodes, c) 
    
        #which-is-faster-hash-lookup-or-binary-search
        #https://stackoverflow.com/questions/360040/which-is-faster-hash-lookup-or-binary-search
        #test: set 173 sec, array + binary search : 141 sec
        #binary search without splitting codes in dictionary: 156 sec
        if(lenC in Code.passedCodesPerL):
            #Code.passedCodesPerL[lenC].append(c)
            bisect.insort(Code.passedCodesPerL[lenC], c) 
            # print(Code.passedCodesPerL)
        else:
            Code.passedCodesPerL[lenC] = []
            Code.passedCodesPerL[lenC].append(c)
            #Code.passedCodesPerL = {16: ['xxxxxxxxxx000000']}
            
            
    def codeToStr(code):
        s = ''
        for r in code[0]:
            s+=str(r)
        for c in code[1]:
            #s+=str(r)
            s+=str(c)
        #print(s)
        #example: s= xxxxxxxxxx000000
        return s
    def find(L, target):
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
            De id kunnen elk 1/2/3 lang zijn
            Voor elk van de 360 reservaties staat er een id in de code
            => lage kans dat twee verschillende code dezelfde lengte hebben
        => moeten meestal niet zoeken door een lijst van duizende code
        """
        
        
        codeString = Code.codeToStr(code)
        lenCodeString = len(codeString)
        if(not(lenCodeString in Code.passedCodesPerL)):
            return False
        if(Code.find(Code.passedCodesPerL[lenCodeString],codeString)):
            return True
        else:
            return False

if __name__ == "__main__":
    
    pass
