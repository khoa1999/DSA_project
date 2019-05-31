import random
from copy import deepcopy
from typing import List

class BattleshipGame:
    # Initial boards
    # The parameter @ships = {'A': 4, 'B': 5, 'S': 3, 'D': 3, 'P': 2}
    def __init__(self, ships):
        self.__userBoard = []             # Private @field __userBoard
        self.userShips = dict(ships)      # Each user ship point to -> the length remained of its self
        self.__computerBoard = []         # Private @field __computerBoard
        self.computerShips = dict(ships)  # Each user ship point to -> the length remained of its self
        self.rounds = 0
        for i in range(10):
            self.__userBoard.append([' '] * 10)
            self.__computerBoard.append([' '] * 10)
        self.computerTargeting = False      # Computer's targeting phase initially is False.
        self.hits = 0                       # Tracks computer hits and is used to determine whether or not to continue the targeting phase.
        self.targetStack = []               # Target stack for computer in targeting mode, containing all possible and valid moves following a hit by the computer.
        self.parityDictionary = dict(ships) # Dictionary used to determine the lowest hit points of remained ships to adjust parity in computer hunting phase.
        self.userShotList = [[int, int]]    # Each item is a list of coordinate [int x, int y]
        self.computerShotList = [[int, int]]# Each item is a list of coordinate [int x, int y]
        self.userSunkShips = []             # List of user's ship names that been destroyed.
        self.computerSunkShips = []         # List of computer's ship names that been destroyed.
        self.userPlacedShips = {}           # Dictionary of user's ship and its position {'Ship_Name': [int x, int y, str: orientation], ...}
        self.__computerPlacedShips = {}     # Dictionary of user's ship and its position {'Ship_Name' : [int x, int y, str: orientation], ...}
        pass

    def drawBoard(self, hide):
        # Draw boards
        # Aircraft is A, Destroyer is D, Submarine is S, Patrol boat is P, Battleship is B
        # Rows are denoted by characters from A to J
        # Columns are denoted by numbers from 1 to 10
        stats = [['Nbr. of hits  :', self.getHits(True), self.getHits(False)],
                 ['Nbr. of misses:', self.getMisses(True), self.getMisses(False)],
                 ['Ships sunk    :', len(self.getEnemyFleet(True)[1]), len(self.getEnemyFleet(False)[1])]]
        shipsSunkByComputer = list(self.getEnemyFleet(True)[1])
        shipsSunkByPlayer = list(self.getEnemyFleet(False)[1])
        statsIndex = 0
        computerIndex = 0
        playerIndex = 0
        if hide:
            computerBoard = deepcopy(self.__computerBoard)
            for row in range(10):
                for cell in range(10):
                    if computerBoard[row][cell] in 'ABCDSP':
                        computerBoard[row][cell] = ' '
        else:
            computerBoard = self.__computerBoard
        columnNumbers = '1 2 3 4 5 6 7 8 9 10 '
        print('%20s %21s %18s %s' % ('Computer\'s board: ', 'User\'s board: ', 'at round: ', self.rounds))
        print('%24s %25s %33s %15s' % (columnNumbers, columnNumbers, 'Computer Status: ', 'User Status: '))
        count = 65        # ASCII code of A is 65
        for row in range(len(self.__userBoard)):
            letter = chr(count)  # chr will return a string of one character whose ASCII code is count(65-74)
            print('%2s|%s|%5s|%s|' % (letter, '|'.join(computerBoard[row]), letter, '|'.join(self.__userBoard[row])), end='')
            if statsIndex < len(stats):
                print('%17s %3.2d %19.2d' % (stats[statsIndex][0], stats[statsIndex][1], stats[statsIndex][2]))
                statsIndex += 1
            elif len(shipsSunkByComputer) or len(shipsSunkByPlayer):
                if playerIndex < len(shipsSunkByPlayer):
                    playerSunkShip = shipsSunkByPlayer[playerIndex]
                    playerIndex += 1
                else:
                    playerSunkShip = ''
                if computerIndex < len(shipsSunkByComputer):
                    computerSunkShip = shipsSunkByComputer[computerIndex]
                    computerIndex += 1
                else:
                    computerSunkShip = ''
                print('                   %-16s    %s' % (computerSunkShip, playerSunkShip))
            else:
                print('')
            count += 1

    def makeA_Move(self, computer, x, y):
        # Return {' '} if it's a miss and return {'A', 'D', 'S', 'P', 'B'} if it's a hit
        if computer:
            board = self.__userBoard
        else:
            board = self.__computerBoard
        if board[x][y] in '* #'.split():
            return board[x][y]      # Return '*' or '#'
        elif board[x][y] == ' ':
            miss = board[x][y]
            board[x][y] = '*'
            return miss             # Return ' '
        else:
            hit = board[x][y]
            board[x][y] = '#'
            return hit              # Return one of {'A', 'D', 'S', 'P', 'B'}

    def validatePlacement(self, computer, ship, size, x, y, orientation):
        # Use the computer's or user's board depending on whether or not True has been passed into the method.
        # With the appropriate board, check if the caller has provided x and y coordinates of an empty cell.
        # If the orientation is vertical, check whether the x coordinate + the size of the ship exceeds the bounds of
        # the game board, if so, return False.
        # Otherwise, check if each x and y coordinate of the ship would fill an empty
        # cell, if so, return True, otherwise return False.
        # This process is identical for checking valid horizontal placement except that
        # the size of the ship is added to the y coordinate instead of the x coordinate to check if the ship is
        # within the bounds of the game board.
        if computer:
            board = self.__computerBoard
        else:
            board = self.__userBoard

        if board[x][y] == ' ':
            if orientation == 'v':
                if x + size - 1 > 9:
                    return False
                else:
                    for i in range(size):
                        if board[x + i][y] != ' ':
                            return False
                    for i in range(size):
                        board[x + i][y] = ship
                    return True
            elif orientation == 'h':
                if y + size - 1 > 9:
                    return False
                else:
                    for i in range(size):
                        if board[x][y + i] != ' ':
                            return False
                    for i in range(size):
                        board[x][y + i] = ship
                    return True
        else:
            return False

    def getEnemyFleet(self, computer):
        # Create empty lists for the entire fleet of all ships sunk
        # If the computer is calling this method, iterate through the users's board, otherwise iterate through the computers's board
        # For each ship in the ship dictionary defined in the init, if the hit points of the ship are greater than zero,
        # call the what ship private method to get the full name of the ship, and then append it to the ships to sink list.
        # Otherwise, if the hit points of the ship is 0, get the full name
        # of the ship as previously using the what ship method, and append it to the ships sunk list.
        # Finally, append both lists to the fleet list and return it.
        shipsToSink = []
        shipsSunk = []
        if computer:
            ships = self.userShips
        else:
            ships = self.computerShips
        for ship in ships:
            if ships[ship] > 0:
                ship = self.whatShip(ship)
                shipsToSink.append(ship)
            else:
                ship = self.whatShip(ship)
                shipsSunk.append(ship)
        return [shipsToSink, shipsSunk]

    def whatShip(self, symbol):
        # Take the first letter (symbol of the ship and return the full name of the ship)
        shipNames = {'A': 'Aircraft Carrier',
                     'B': 'Battleship',
                     'S': 'Submarine',
                     'D': 'Destroyer',
                     'P': 'Patrol Boat'}
        fullName = shipNames[symbol]
        return fullName

    def checkWinning(self, computer):
        # Pass true or false depending on whether the user or computer is calling the method.
        # To determine if the computer or user has won, check the length of the ships to sink list
        # generated by the get enemy fleet method. If there are still ships on the board that have
        # not yet been sunk, return False, otherwise return True since all ships have been sunk.
        if computer:
            computer = True
        else:
            computer = False
        if len(self.getEnemyFleet(computer)[0]) == 0:
            return True
        else:
            return False

    def checkIfSunk(self, computer, ship):
        # Check if all parts of the ship is hit
        if computer:
            self.userShips[ship] -= 1
            if self.userShips[ship] == 0:
                print('Computer sunk your %s!' % (self.whatShip(ship)))
                self.userSunkShips.append(self.whatShip(ship))
                return True
            return False
        else:
            self.computerShips[ship] -= 1
            if self.computerShips[ship] == 0:
                print('You sunk Computer\'s %s!' % (self.whatShip(ship)))
                self.computerSunkShips.append(self.whatShip(ship))
                return True
            return False

    def incrementRounds(self):
        # increment the instance variable rounds by one after both the player and computer have shot
        self.rounds += 1

    def getHits(self, computer):
        # Pass true if returning hits for computer or false if checking hits for the player.
        # Iterate through the game board and check for hits ('#'), if a hit is encountered, increment
        # the variable hits by one. After iterating, return hits.
        hits = 0
        if computer:
            board = self.__userBoard
        else:
            board = self.__computerBoard
        for row in range(10):
            for cell in range(10):
                if board[row][cell] == '#':
                    hits += 1
        return hits

    def getMisses(self, computer):
        # Pass true if returning misses for computer or false if checking misses for the player.
        # Iterate through the game board and check for misses ('#'), if a miss is encountered, increment
        # the variable misses by one. After iterating, return misses.
        misses = 0
        if computer:
            board = self.__userBoard
        else:
            board = self.__computerBoard
        for row in range(10):
            for cell in range(10):
                if board[row][cell] == '*':
                    misses += 1
        return misses

    def userPlaceShips(self, ship, size):
        # While ship placement is not valid, prompt the user to enter in x and y coordinates for their shot.
        # After valid input has been accepted, ask the user for the orientation they would like to place their ship and only accept either v or h.
        # After all input is validated, call the validate placement method to check
        # if the ship can be placed on the board, if not, alert the user and prompt them to enter a new set of coordinates and orientation.
        # If the ship can be placed on the board, alert the player that they have placed a ship and the type of ship placed.
        valid = False
        while not valid:
            print('Placing %s of size %s' % (ship, size))
            x, y = userInput()
            orientation = None
            while orientation not in 'v h'.split():
                orientation = input('Is this ship vertical or horizontal (v,h)? ').lower()
            valid = self.validatePlacement(False, ship[0], size, x, y, orientation)
            print('You placed a %s' % ship)
            self.drawBoard(True)
            print()
            if not valid:
                print('Cannot place a %s there. Stern is out of the board or collides with another ship.' % ship)
                print('Please take a look at the board and try again.')

    def computerPlaceShips(self, ship, size):
        # While a valid placement for a particular ship has not been randomly generated by the computer,
        # generate random x and y coordinates between 0 and 9 and a random orientation (either v or h).
        # Continue generating random coordinates until the ship can be placed on the board.
        valid = False
        while not valid:
            x, y = random.randint(0, 9), random.randint(0, 9)
            orientation = random.choice(['v', 'h'])
            valid = self.validatePlacement(True, ship[0], size, x, y, orientation)
            if valid:
                # self.__computerPlacedShips.update({ship: [x, y, orientation]})
                self.__computerPlacedShips.update({ship: [chr(x + 65), y + 1, orientation]})
        print('Computer has placed a %s' % ship)

    def computerMakesMove(self):
        # Pass the battleShip game object, the size of the ships, and whether or not the computer is in targeting mode.
        # Initialize parity variable as the minimum ship size still in play. If the computer is in targeting mode,
        # pop a move from the targetStack and play that move. Otherwise, choose a random x (letter) coordinate between 0 and 9
        # set the range of possible y coordinates (numbers) to the result of the modulo of the x coordinate and the parity(min ship size).
        # Generate a random y coordinate in the defined range and then play the resulting move.
        # If the computer has fired a shot in the same location previously, generate new x and y coordinates.
        # Otherwise, print a message informing the user that the computer has missed their ship,
        # or if the computer has hit the user's ship, check if it has sunk by calling the check if sunk method.
        # If the ship has not been sunk, push to targetStack moves to the left, right, top, and bottom of the hit and return True(True is targeting mode).

        parity = min(self.parityDictionary.values())  # Get smallest ship size still remaining in play.
        while True:
            if self.computerTargeting:
                x, y = self.targetStack.pop()
            else:
                x = random.randrange(0, 10)
                yRange = x % parity
                y = random.randrange(yRange, 10, parity)
            computerMove = self.makeA_Move(True, x, y)
            if computerMove in '* #'.split():
                continue
            elif computerMove == ' ':
                self.computerShotList.append([x, y])
                print('Computer missed your ship at %s %s.' % (chr(x + 65), y + 1))
                if self.computerTargeting:
                    self.computerTargeting = True
                else:
                    self.computerTargeting = False
                return False
            else:
                self.hits += 1
                self.computerShotList.append([x, y])
                print('Computer hit your ship at %s %s!' % (chr(x + 65), y + 1))
                if self.checkIfSunk(True, computerMove):
                    self.hits -= self.parityDictionary[computerMove]  # If hits - length of ship sunk = 0, no hits were registered to a different ship.
                    del self.parityDictionary[computerMove]  # If the ship has sunk, delete it from the dictionary to allow a new minimum ship size.
                    if self.hits == 0:  # To make sure all hit shots are on the latest Sunk Ship, else at least 1 shot hit another ship that not been sunk yet.
                        self.targetStack = []  # Empty the stack before changing computer to hunting mode
                        self.computerTargeting = False
                    else:
                        self.computerTargeting = True
                else:
                    # Append x and y coordinates above, below, to the left, and to the right
                    # of the hit to targetStack list if they are within the bounds of the game board.
                    # This initiates the target phase. Checking if this cell has already been played
                    # is not needed because this case is handled above.
                    if y - 1 >= 0:
                        self.targetStack.append([x, y - 1])
                    if y + 1 <= 9:
                        self.targetStack.append([x, y + 1])
                    if x - 1 >= 0:
                        self.targetStack.append([x - 1, y])
                    if x + 1 <= 9:
                        self.targetStack.append([x + 1, y])
                    self.computerTargeting = True
                return True

    def userMakesMoveAtXY(self, x, y):
        userMove = self.makeA_Move(False, x, y)
        if userMove in '* #'.split():
            print('Sorry, %s %s was already played. Try again.' % (chr(x + 65), y + 1))
            a = 0
        elif userMove == ' ':
            self.userShotList.append([x, y])
            print('Your shot at %s %s missed.' % (chr(x + 65), y + 1))
            a = 1
        else:
            a = 2
            self.userShotList.append([x, y])
            print('You hit Computer\'s ship at %s %s!' % (chr(x + 65), y + 1))
            if self.checkIfSunk(False, userMove):
                raise ComputerShipSunkException
        return a

    def userMakesMove(self):
        # Until a valid move is played on the board, ask the user for coordinates for their shot.
        # If the a shot has already been taken at that location, alert the user and prompt them to enter another set of coordinates.
        # If the user has missed, print a message and return.
        # If the user has hit a ship, print a message indicating they hit a ship and then call the check if sunk method.
        while True:
            x, y = userInput()
            userMove = self.makeA_Move(False, x, y)
            if userMove in '* #'.split():
                print('Sorry, %s %s was already played. Try again.' % (chr(x + 65), y + 1))
            elif userMove == ' ':
                self.userShotList.append([x, y])
                print('Your shot at %s %s missed.' % (chr(x + 65), y + 1))
                return
            else:
                self.userShotList.append([x, y])
                print('You hit Computer\'s ship at %s %s!' % (chr(x + 65), y + 1))
                if self.checkIfSunk(False, userMove):
                    print("BOOM !")
                return

    def getLatestShot(self, isComputer):
        try:
            if isComputer:
                return self.computerShotList.__getitem__(self.computerShotList.__len__() - 1)
            else:
                return self.userShotList.__getitem__(self.userShotList.__len__() - 1)
        except IndexError:
            return None

    def getLatestSunkShipPosition(self, isComputer):
        try:
            if isComputer:
                return self.__computerPlacedShips.get(self.getLatestSunkShipName(True))
            else:
                return self.userPlacedShips.get(self.getLatestSunkShipName(False))
        except KeyError:
            return None

    def getLatestSunkShipName(self, isComputer):
        try:
            if isComputer:
                return self.computerSunkShips.__getitem__(self.computerSunkShips.__len__() - 1)
            else:
                return self.userSunkShips.__getitem__(self.userSunkShips.__len__() - 1)
        except IndexError:
            return None

    def getComputerPlacedShips(self):  # Get computer's ships name & position
        return self.__computerPlacedShips

    pass  # End BattleshipGame's constructor !


class UserShipSunkException(Exception):
    """ Raised when a new ship of user been sunk !"""
    pass  # End UserShipSunkException constructor !


class ComputerShipSunkException(Exception):
    """ Raised when a new ship of computer been sunk !"""
    pass  # End ComputerShipSunkException constructor !


def userInput():
    # Until the user enters in valid input, prompt them to enter a letter and number for the x and y coordinate respectively.
    # To do this, check if the user's input consists of two elements separated by a space,
    # if so check if the x coordinate consists of a letter and the y coordinate consists of a number.
    # Next convert the y coordinate to an integer and check if it is within 1 and 10.
    # Next check if the x coordinate is between the letters a and j.
    # Finally return the x and y coordinates as integers between 0 and 9.
    while True:
        move = input('Enter coordinates x y (x in [A..J]) and y in [1..10]): ').lower()
        move = move.split()
        if len(move) != 2:
            continue
        if move[0].isalpha() and move[1].isnumeric():
            if len(move[0]) > 1:
                continue
            if 'a' <= move[0] <= 'j' and 1 <= int(move[1]) <= 10:
                return int(ord(move[0]) - 97), int(int(move[1]) - 1)
            else:
                continue
        else:
            continue


def main():
    playing = True
    fleetDictionary = {'Aircraft Carrier': 4,
                       'Battleship': 5,
                       'Submarine': 3,
                       'Destroyer': 3,
                       'Patrol Boat': 2}
    ships = {key[0]: fleetDictionary.get(key) for key in fleetDictionary}  # The dictionary key is 1st letter of ship and associated values are ship hit points.
    battleShip = BattleshipGame(ships)
    for computerShip in fleetDictionary:
        battleShip.computerPlaceShips(computerShip, fleetDictionary[computerShip])
    battleShip.drawBoard(True)
    print('Welcome to Battleship! Please place your ships.')
    for userShip in fleetDictionary:
        battleShip.userPlaceShips(userShip, fleetDictionary[userShip])
    battleShip.incrementRounds()
    battleShip.drawBoard(True)
    input('You have placed all of your ships. Please press ENTER to continue.')
    print('Fire at the enemy fleet...')
    while playing:
        battleShip.userMakesMove()
        userWin = battleShip.checkWinning(False)
        if userWin:
            battleShip.drawBoard(True)
            print('Congratulations! You have won against the computer.')
            playing = False
            break
        battleShip.computerMakesMove()
        computerWin = battleShip.checkWinning(True)
        if computerWin:
            print('Sorry! You have lost against the computer.')
            print('Remaining Computer Ships:')
            battleShip.drawBoard(False)
            playing = False
            input('Press any key to exit.')
            break
        battleShip.incrementRounds()
        battleShip.drawBoard(True)


if __name__ == "__main__":
    main()
