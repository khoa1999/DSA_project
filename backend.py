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

    @staticmethod
    def start_game():
        # The dictionary @{ships}'s key is the 1st letter of ship's name and the associated values are ship's length
        Backend.ships = {key[0]: Backend.fleetDictionary.get(key) for key in Backend.fleetDictionary}
        Backend.battleShipGame = bs.BattleshipGame(Backend.ships)
        Backend.playing = True
        Backend.set_computer_ship()
        print('Welcome to Battleship! Please place your ships.')
        pass

    @staticmethod
    def set_computer_ship():
        if Backend.battleShipGame is None:
            raise ValueError("The game has not yet been created !")

        """ Placing computer' ships into Backend.battleShip """
        for computerShip in Backend.fleetDictionary:
            Backend.battleShipGame.computerPlaceShips(computerShip, Backend.fleetDictionary[computerShip])
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
            if not Backend.battleShipGame.validatePlacement(False, key[0], size, value[0], value[1], value[2]):
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
        return Backend.battleShipGame.userMakesMoveAtXY(x, y)

    @staticmethod
    def computer_hit_at():
        """ Return computer's shot position at [x, y] !"""
        Backend.battleShipGame.computerMakesMove()
        return Backend.battleShipGame.getLatestShot(True)  # Latest shot of computer [x: int, y: int]

    @staticmethod
    def end_game():
        Backend.battleShipGame = None
        Backend.playing = False
        Backend.ships = None
        pass

    
    
    
    
        
    
    
        
    
        
        
        
        
        
        
        
    
    
