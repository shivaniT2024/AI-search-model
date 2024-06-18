# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 17:10:32 2023

@author: shiva
"""

import random
from BaseAI import BaseAI
class IntelligentAgent(BaseAI):
    
    def getMove(self, grid):
        x = self.maximize(grid, -float('inf'), float('inf'), 3)
        return x[2]
  
    
    #def decision(self, state):
     #  child, _ = self.maximize(state, -float('inf'), float('inf'),3)
      # return child
       

    def terminaltest_min(self, state,depth):
    
        if depth ==0:
            return True
        if not state.canMove():
            return True
        return False
    
    def terminaltest_max(self,state,depth):
        
        if depth ==0:
            return True
        if state.getMaxTile() >= 2048:
            return True
        return False
        

    def minimize(self, state, alpha, beta, depth, which): #mini
       
        if self.terminaltest_min(state,depth):
            return (None, self.evaluate(state))

        minChild, minUtility = [None, float('inf')]

       
        for x in state.getAvailableCells(): #list of coordinates. list of tuples
            
            child = state.clone()
            child.insertTile(x, which)
            
            _, utility,v = self.maximize(child,alpha,beta,depth-1)
      
            if utility < minUtility:
                minChild, minUtility = child, utility
                
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility 

        return [minChild, minUtility]

    def maximize(self, state, alpha, beta,depth):
       
        if self.terminaltest_max(state,depth):
            return (None, self.evaluate(state),-1)

        maxChild, maxUtility = [None, -float('inf')]
        
        maxMove = 0

        for x in state.getAvailableMoves(): #each child is a tuple. we care about the grid
            child = x[1]
            move = x[0]
            
            if child == state:
                continue
            
            _, utility2 = self.minimize(child, alpha, beta, depth-1, 2 )
            _, utility4 = self.minimize(child, alpha, beta, depth-1,4 )
            
            utility = 0.9*utility2 + 0.1*utility4

            if utility > maxUtility:
                maxChild, maxUtility, maxMove = child, utility, move
                
            if maxUtility >= beta:
                break
            
            if maxUtility > alpha:
                alpha = maxUtility
        
        return [maxChild, maxUtility, maxMove]
    

    def evaluate(self, state):
        
        largest= state.getMaxTile()
        diff = abs(2040-largest)

        empty_cells = len(state.getAvailableCells())

        monotonicity = 0
        for i in range(3):
            for j in range(3):
                current_tile = state.map[i][j]
                if current_tile != 0:
                    if j < 3 and state.map[i][j + 1] >= current_tile:
                        monotonicity += 1
                    if i < 3 and state.map[i + 1][j] >= current_tile:
                        monotonicity += 1
    
        smoothness = 0
        for i in range(4):
            for j in range(3):
                current_tile = state.map[i][j]
                right_neighbor = state.map[i][j + 1]
                if right_neighbor >= current_tile:
                    smoothness += abs(right_neighbor - current_tile)
       
        # Check vertical smoothness
        for i in range(3):
            for j in range(3):
                current_tile = state.map[i][j]
                lower_neighbor = state.map[i + 1][j]
                if lower_neighbor >= current_tile:
                    smoothness += abs(lower_neighbor - current_tile)
                    
                   
       
        #score = 0.8*empty_cells+ 0.2*monotonicity
        score = 0.8*empty_cells + 0.3*(monotonicity/largest)
        #score = 0.9*empty_cells + 0.4*(1/diff)*10 + 0.2*(monotonicity/10)
        return score
    
        

   
