#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:03:56 2019

@author: hodangphuongngoc

"""
import DSA_battleship as bs

"""input toa do chay tu 0"""


class Backend:
    # Call DSA_battleship class
    counter = 0  # Dummy variable for front-end without backend
    hits = 0
    targetStack = []
    computerTargeting = False
    playing = False
    fleetDictionary = {'Aircraft Carrier': 4,
                       'Battleship': 5,
                       'Submarine': 3,
                       'Destroyer': 3,
                       'Patrol Boat': 2}
    parityDictionary = None
    battleShip = None
    ships = None

    @staticmethod
    def start_game():
        # The dictionary key is first letter of ship and the associated values are ship hit points
        Backend.ships = {key[0]: Backend.fleetDictionary.get(key) for key in Backend.fleetDictionary}

        Backend.parityDictionary = dict(Backend.ships)
        Backend.battleShip = bs.BattleshipGame(Backend.ships)
        Backend.playing = True

        Backend.call_place_computer_ship()
        print('Welcome to Battleship! Please place your ships.')
        Backend.call_set_user_ship()
        Backend.play()
        pass

    @staticmethod
    def call_place_computer_ship():
        if Backend.battleShip is None:
            raise ValueError("The game has not yet been created !")

        """ Placing computer' ships into Backend.battleShip """
        for computerShip in Backend.fleetDictionary:
            bs.computerPlaceShips(Backend.battleShip, computerShip, Backend.fleetDictionary[computerShip])
        pass

    @staticmethod
    def call_set_user_ship():
        if Backend.battleShip is None:
            raise ValueError("The game has not yet been created !")

        allShipPlaced = {}  # Create new dictionary to add ships' properties
        """ Placing computer' ships into Backend.battleShip """
        for userShip in Backend.fleetDictionary:
            # shipProperty = Backend.userPlaceShips(Backend.battleShip, userShip, Backend.fleetDictionary[userShip])
            shipProperty = Backend.userAutoPlaceShips(Backend.battleShip, userShip, Backend.fleetDictionary[userShip])
            allShipPlaced.update({userShip[0]: shipProperty})

        """ Return list of dict{chữ cái đầu tên thuyền:value}
        for each value : list có ba giá trị  [x,y,v/h]
        index từ 0 """

        """ The returned value is a dictionary. Each key point to a list contains 3 main ships' properties.
            {"A": [0, 0, "v"],
            "B": [0, 1, "h"],
            "S": [1, 1, "v"],
            "D": [2, 4, "h"],
            "P": [3, 5, "v"]}
        """

        return allShipPlaced

    @staticmethod
    def check_win():
        """ Return Winner theo format [bool,bool]
        false,true : computer win
        true,false: user win 
        false, false : 
        """
        if Backend.battleShip.checkWinning(True):
            return [False, True]  # Computer win.
        elif Backend.battleShip.checkWinning(False):
            return [False, False]  # User win.
        else:
            return [False, False]  # Neither of both has yet win the game.

    @staticmethod
    def call_hit(x: int, y: int):

        """ tra ve cho backend vi tri thuyen bi bắn"""
        pass

   

    @staticmethod
    def userPlaceShips(battleShipGame, ship, size):
        valid = False
        x: str
        y: int
        orientation: str
        while not valid:
            print('Placing %s of size %s' % (ship, size))
            x, y = bs.userInput()
            orientation = None
            while orientation not in 'v h'.split():
                orientation = input('Is this ship vertical or horizontal (v,h)? ').lower()
            valid = battleShipGame.validatePlacement(False, ship[0], size, x, y, orientation)
            print('You placed a %s' % ship)
            battleShipGame.drawBoard(True)
            print()
            if not valid:
                print('Cannot place a %s there. Stern is out of the board or collides with another ship.'
                      '\nPlease take a look at the board and try again.' % ship)
        return [x, y, orientation]

    @staticmethod
    def userAutoPlaceShips(battleShipGame, ship, size):
        import random
        valid = False
        x: str
        y: int
        orientation: str
        while not valid:
            x, y = random.randint(0, 9), random.randint(0, 9)
            orientation = random.choice(['v', 'h'])
            valid = battleShipGame.validatePlacement(False, ship[0], size, x, y, orientation)
        battleShipGame.drawBoard(True)
        return [x, y, orientation]

    @staticmethod
    def play():
        while Backend.playing:
            bs.userMakesMove(Backend.battleShip)

            if Backend.battleShip.checkWinning(False):  # User win
                Backend.battleShip.drawBoard(True)
                print('Congratulations! You have won against the computer.')
                Backend.playing = False
                break
            Backend.computerTargeting = bs.computerMakesMove(Backend.battleShip, Backend.ships,
                                                             Backend.computerTargeting, Backend.hits,
                                                             Backend.targetStack, Backend.parityDictionary)

            if Backend.battleShip.checkWinning(True):  # Computer win
                print('Sorry! You have lost against the computer.')
                print('Remaining Computer Ships:')
                Backend.battleShip.drawBoard(False)
                Backend.playing = False
                input('Press any key to exit.')
                break
            Backend.battleShip.incrementRounds()
            Backend.battleShip.drawBoard(True)


Backend.start_game()
