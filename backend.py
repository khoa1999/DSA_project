#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:03:56 2019

@author: Ho Dang Phuong Ngoc

"""
import DSA_battleship as bs


class Backend:
    # Call DSA_battleship class.
    fleetDictionary = {'Aircraft Carrier': 4,
                       'Battleship': 5,
                       'Submarine': 3,
                       'Destroyer': 3,
                       'Patrol Boat': 2}
    battleShipGame = None
    playing = False
    ships = None
    player_hits = {}
    computer_hits = {}
    flag = None
    
    @staticmethod
    def start_game():
        # The dictionary @{ships}'s key is the 1st letter of ship's name and the associated values are ship's length
        Backend.ships = {key[0]: Backend.fleetDictionary.get(key) for key in Backend.fleetDictionary}
        Backend.battleShipGame = bs.BattleshipGame(Backend.ships)
        Backend.playing = True
        Backend.flag = False
        Backend.player_hits = {}
        Backend.computer_hits = {}
        #Backend.set_computer_ship()
        print('Welcome to Battleship! Please place your ships.')
        pass

    @staticmethod
    def set_computer_ship():
        if Backend.battleShipGame is None:
            raise ValueError("The game has not yet been created !")

        """ Placing computer' ships into Backend.battleShip """
        for computerShip in Backend.fleetDictionary:
            Backend.battleShipGame.computerPlaceShips(
                    computerShip, Backend.fleetDictionary[computerShip])
        pass

    @staticmethod
    def set_user_ship(ships: dict):
        """ The @parameter ships is a dictionary. Each key point to a list contains 3 main ships' properties.
            {"Aircraft Carrier": [0, 0, "v"],
            "Battleship": [0, 1, "h"],
            "Submarine": [1, 1, "v"],
            "Destroyer": [2, 4, "h"],
            "Patrol Boat": [3, 5, "v"]}
        """
        for key, value in ships.items():
            size = Backend.fleetDictionary.get(key)
            """if not Backend.battleShipGame.validatePlacement(False, key[0], size, value[0], value[1], value[2]):
                return False
        Backend.battleShipGame.userPlacedShips = dict(ships)  # If no error. Update user's ship position to Core Game !

        return True  # Successfully placing all ships"""
        
            if (Backend.battleShipGame.validatePlacement(False, key[0], size, value[0], value[1], value[2])==False):
                return False
        Backend.battleShipGame.userPlacedShips = dict(ships)  # If no error. Update user's ship position to Core Game !

        return True  # Successfully placing all ships
            

    @staticmethod
    def check_win():
        """ Return Winner in format [bool, bool]
        false, true : Computer Win
        true, false : User Win
        false, false : Neither Win
        """
        if Backend.battleShipGame.checkWinning(True):
            return [False, True]  # Computer win.
        elif Backend.battleShipGame.checkWinning(False):
            return [True, False]  # User win.
        else:
            return [False, False]  # Neither of both has yet win the game.

    @staticmethod
    def user_hit_at(x: int, y: int):
        """ Return User's shot, True if hit, False if miss or already shoot at [x, y] !"""
        if Backend.battleShipGame is None:
            raise ValueError("The game has not yet been created !")
        """ Raise ComputerShipSunkException if the latest move sink the enemy ship !"""
        if((x,y) in Backend.player_hits.keys()):
            return Backend.player_hits[(x,y)]
        try:
            a = Backend.battleShipGame.userMakesMoveAtXY(x, y)
        except Exception:
            a = 2
            Backend.flag = True
        if(a == 1):
            Backend.player_hits[(x,y)] = False
        elif(a == 2):
            Backend.player_hits[(x,y)] = True
        return Backend.player_hits[(x,y)]

    @staticmethod
    def computer_hit_at():
        """ Return computer's shot position at [x, y] !"""
        Backend.computer_hits[(Backend.battleShipGame.getLatestShot(True)[0],
                               Backend.battleShipGame.getLatestShot(True)[1])] = Backend.battleShipGame.computerMakesMove()
        return Backend.battleShipGame.getLatestShot(True)  # Latest shot of computer [x: int, y: int]
    
    @staticmethod
    def end_game():
        Backend.battleShipGame = None
        Backend.playing = False
        Backend.ships = None
        pass
    @staticmethod
    def get_score():
        return [Backend.battleShipGame.getHits(True),
                Backend.battleShipGame.getHits(False)]
    @staticmethod
    def check():
        if(Backend.flag):
            Backend.flag = False
            a = Backend.battleShipGame.getLatestSunkShipPosition(True)
            b = None
            if(a[0] == 'A'):
                b = 0
            elif(a[0] == 'B'):
                b = 1
            elif(a[0] == 'C'):
                b = 2
            elif(a[0] == 'D'):
                b = 3
            elif(a[0] == 'E'):
                b = 4
            elif(a[0] == 'F'):
                b = 5
            elif(a[0] == 'G'):
                b = 6
            elif(a[0] == 'H'):
                b = 7
            elif(a[0] == "I"):
                b = 8
            elif(a[0] == 'J'):
                b = 9
            return [Backend.battleShipGame.getLatestSunkShipName(True),
                [a[1] - 1,b,a[2]]]
        return None
    @staticmethod
    def get_health(name:str):
        return Backend.fleetDictionary[name]
    
    
    
    
    
        
    
    
        
    
        
        
        
        
        
        
        
    
    
