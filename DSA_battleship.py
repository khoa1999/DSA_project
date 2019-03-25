import random
from copy import deepcopy


class BattleshipGame():
    #Initial boards, ships
    def __init__(self, ships):
        self.userBoard = []
        self.userShips = dict(ships)
        self.computerBoard = []
        self.computerShips = dict(ships)
        self.rounds = 0
        for i in range(10):
            self.userBoard.append([' '] * 10)
            self.computerBoard.append([' '] * 10)
    def drawBoard(self, hide):
        # Draw boards
        # Aircraft is A, Destroyer is D, Submarine is S, Patrol boat is P, Battleship is B
        # Rows are denoted from A to J
        # Columns are denoted from 1 to 10    
        stats = [['Nbr. of hits  :', self.getHits(True), self.getHits(False)], \
                 ['Nbr. of misses:', self.getMisses(True), self.getMisses(False)], \
                 ['Ships sunk    :', len(self.getEnemyFleet(True)[1]), len(self.getEnemyFleet(False)[1])]]
        
        
        
        
      
