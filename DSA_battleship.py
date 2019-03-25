import random
from copy import deepcopy


class BattleshipGame():
    #Initial boards
    def __init__(self, ships):
        self.userBoard = []
        self.userShips = dict(ships)
        self.computerBoard = []
        self.computerShips = dict(ships)
        self.rounds = 0
        for i in range(10):
            self.userBoard.append([' '] * 10)
            self.computerBoard.append([' '] * 10)
