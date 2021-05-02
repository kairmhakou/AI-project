# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:03:22 2021

@author: Loic Dehan
"""
from State import State

class Tabu:
    tabuList = set()
    
    #Convert all decisions to array of chars:
    #   for each reservation: to which car it is assigned or 'x' if not assigned
    #   for each car: in which zone it is placed
    def formCode():       
        rcode = [r.carID if r.carID!=-1 else 'x' for r in State.rlist]
        ccode = [c.zone for c in State.cars]
        return [rcode,ccode]
        
    #Convert array of chars to string to be placed in tabuList sets
    def _codeToStr(code):
        return ''.join(map(str,code[0])) + ''.join(map(str,code[1]))
       
    #Add state to tabuList 
    def add(code):
        c = ''.join(map(str,code[0])) + ''.join(map(str,code[1]))
        Tabu.tabuList.add(c)
        return 1
        
    #Check if state is already in tabuList
    def inMemory(code):
        codeString = ''.join(map(str,code[0])) + ''.join(map(str,code[1]))
        return codeString in Tabu.tabuList

if __name__ == "__main__":
    pass
