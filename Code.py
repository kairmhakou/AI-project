# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: dehan
"""

class Code:
    passedCodes = []
    
    position = 0
    def formCode(rlist,cars,cost=0):
        ccode = []
        rcode = []
        for r in rlist:
            rcode.append(r.code())
        for c in cars:
            ccode.append(c.code())
        return [rcode,ccode,cost]
    def add(ncode):
        Code.passedCodes.append(ncode)
    def setMemory(code):
        
        Code.passedCodes.append(code)
        
    def inMemory(code):        
        for cd in Code.passedCodes:
            equals = True
            for r in range(len(cd[0])):
                if(cd[0][r]!=code[0][r]):
                    equals = False
            for c in range(len(cd[1])):
                if(cd[1][c]!=code[1][c]):
                    equals = False
            if(equals == True):
                return True
        return False
                