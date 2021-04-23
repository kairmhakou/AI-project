# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: Loic Dehan
"""
from State import State

class Tabu:
    tabuList = set()
   
    def formCode():       
        rcode = [r.carID if r.carID!=-1 else 'x' for r in State.rlist]
        ccode = [c.zone for c in State.cars]
        return [rcode,ccode]
           
    def _codeToStr(code):
        return ''.join(map(str,code[0])) + ''.join(map(str,code[1]))
        
    def add(code):
        c = ''.join(map(str,code[0])) + ''.join(map(str,code[1]))
        Tabu.tabuList.add(c)
        return 1

    def inMemory(code):
        codeString = ''.join(map(str,code[0])) + ''.join(map(str,code[1]))
        return codeString in Tabu.tabuList

if __name__ == "__main__":
    pass
