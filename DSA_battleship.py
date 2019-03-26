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
        shipsSunkByComputer = list(self.getEnemyFleet(True)[1])
        shipsSunkByPlayer = list(self.getEnemyFleet(False)[1])
        statsIndex = 0
        computerIndex = 0
        playerIndex = 0
        if hide:
            computerBoard = deepcopy(self.computerBoard)
            for row in range(10):
                for cell in range(10):
                    if computerBoard[row][cell] in 'ABCDSP':
                        computerBoard[row][cell] = ' '
        else:
            computerBoard = self.computerBoard
        columnNumbers = ('1 2 3 4 5 6 7 8 9 10 ')
        print('%20s %21s %18s %s' % ('Computer\'s board:', 'User\'s board:', 'at round:', self.rounds))
        print('%24s %25s %33s %15s' % (columnNumbers, columnNumbers, 'Computer Status:', 'User Status:'))
        count = 65  # ASCII code of A is 65
        for row in range(len(self.userBoard)):
            letter = chr(count)  # chr will return a string of one character whose ASCII code is count(65-74)
            print('%2s|%s|%5s|%s|' % (letter, '|'.join(computerBoard[row]), letter, '|'.join(self.userBoard[row])),
                  end='')
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
        # Return * if it's a miss and return # if it's a hit
        if computer:
            board = self.userBoard
        else:
            board = self.computerBoard
        if board[x][y] in '* #'.split():
            return board[x][y]
        elif board[x][y] == ' ':
            miss = board[x][y]
            board[x][y] = '*'
            return miss
        else:
            hit = board[x][y]
            board[x][y] = '#'
            return hit

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
            board = self.computerBoard
        else:
            board = self.userBoard

        if board[x][y] == ' ':
            if orientation == 'v':
                if x + size > 9:
                    return False
                else:
                    for i in range(size):
                        if board[x + i][y] != ' ':
                            return False
                    for i in range(size):
                        board[x + i][y] = ship
                    return True
            elif orientation == 'h':
                if y + size > 9:
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
        # For each ship in the ship dictionary defined in the init, if the hitpoints of the ship are greater than zero,
        # call the what ship private method to get the full name of the ship, and then append it to the ships to sink list.
        # Otherwise, if the hitpoints of the ship is 0, get the full name
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
                return True
            return False
        else:
            self.computerShips[ship] -= 1
            if self.computerShips[ship] == 0:
                print('You sunk Computer\'s %s!' % (self.whatShip(ship)))
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
            board = self.userBoard
        else:
            board = self.computerBoard
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
            board = self.userBoard
        else:
            board = self.computerBoard
        for row in range(10):
            for cell in range(10):
                if board[row][cell] == '*':
                    misses += 1
        return misses


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
            move[1] = int(move[1])
            if 'a' <= move[0] <= 'j':
                move[0] = ord(move[0]) - 97
            if 1 <= move[1] <= 10:
                move[1] = move[1] - 1
                x = move[0]
                y = move[1]
                return x, y
            else:
                continue
        else:
            continue


def userPlaceShips(battleShip, ship, size):
    # While ship placement is not valid, prompt the user to enter in x and y coordinates for their shot.
    # After valid input has been acceped, ask the user for the orientation they would like to place their ship and only accept either v or h.
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
        valid = battleShip.validatePlacement(False, ship[0], size, x, y, orientation)
        print('You placed a %s' % (ship))
        battleShip.drawBoard(True)
        print()
        if not valid:
            print(
                'Cannot place a %s there. Stern is out of the board or collides with another ship.\nPlease take a look at the board and try again.' % (
                    ship))


def computerPlaceShips(battleShip, ship, size):
    # While a valid placement for a particular ship has not been randomly generated by the computer,
    # generate random x and y coordinates between 0 and 9 and a random orientation (either v or h).
    # Continue generating random coordinates until the ship can be placed on the board.
    valid = False
    while not valid:
        x, y = random.randint(0, 9), random.randint(0, 9)
        orientation = random.choice(['v', 'h'])
        valid = battleShip.validatePlacement(True, ship[0], size, x, y, orientation)
    print('Computer has placed a %s' % (ship))


def computerMakesMove(battleShip, shipSizes, computerTargeting):
    # Pass the battleShip game object, the size of the ships, and whether or not the computer is in targetting mode.
    # Initialize parity variable as the minimum ship size still in play. If the computer is in targetting mode,
    # pop a move from the targetStack and play that move. Otherwise, choose a random x (letter) coordinate between 0 and 9
    # set the range of possible y coordinates (numbers) to the result of the modulo of the x coordinate and the parity(min ship size).
    # Generate a random y coordinate in the defined range and then play the resulting move.
    # If the computer has fired a shot in the same location previously, generate new x and y coordinates.
    # Otherwise, print a message informng the user that the computer has missed their ship,
    # or if the computer has hit the user's ship, check if it has sunk by calling the check if sunk method.
    # If the ship has not been sunk, push to targetStack moves to the left, right, top, and bottom of the hit and return True(True is targetting mode).

    global targetStack  # These three global variables are initialized in the main function below
    global hits
    global parityDictionary
    parity = min(parityDictionary.values())  # Get smallest ship size still remaining in play.
    while True:
        if computerTargeting:
            x, y = targetStack.pop()
        else:
            x = random.randrange(0, 10)
            yRange = x % parity
            y = random.randrange(yRange, 10, parity)
        computerMove = battleShip.makeA_Move(True, x, y)
        if computerMove in '* #'.split():
            continue
        elif computerMove == ' ':
            print('Computer missed your ship at %s %s.' % (chr(x + 65), y + 1))
            if computerTargeting:
                return True
            else:
                return False
        else:
            hits += 1
            print('Computer hit your ship at %s %s!' % (chr(x + 65), y + 1))
            if battleShip.checkIfSunk(True, computerMove):
                del parityDictionary[
                    computerMove]  # If the ship has sunk, delete it from the dictionary to allow a new minimum ship size.
                hits -= shipSizes[
                    computerMove]  # if hits - length of ship sunk = 0, no hits were registered to a different ship
                if hits == 0:
                    targetStack = []
                    return False  # Computer will be in hunting mode
                else:
                    return True  # Computer remains in targetting mode
            else:
                # Append x and y coordinates above, below, to the left, and to the right
                # of the hit to targetStack list if they are within the bounds of the game board.
                # This initiates the target phase. Checking if this cell has already been played
                # is not needed because this case is handled above.
                if y - 1 >= 0:
                    targetStack.append([x, y - 1])
                if y + 1 <= 9:
                    targetStack.append([x, y + 1])
                if x - 1 >= 0:
                    targetStack.append([x - 1, y])
                if x + 1 <= 9:
                    targetStack.append([x + 1, y])
                return True  # Computer will be in targetting mode.


def userMakesMove(battleShip):
    # Until a valid move is plyed on the board, ask the user for coordinates for their shot.
    # If the a shot has already been taken at that location, alert the user and prompt them to enter another set of coordinates.
    # If the user has missed, print a message and return.
    # If the user has hit a ship, print a message indicating they hit a ship and then call the check if sunk method.
    while True:
        x, y = userInput()
        userMove = battleShip.makeA_Move(False, x, y)
        if userMove in '* #'.split():
            print('Sorry, %s %s was already played. Try again.' % (chr(x + 65), y + 1))
        elif userMove == ' ':
            print('Your shot at %s %s missed.' % (chr(x + 65), y + 1))
            return
        else:
            print('You hit Computer\'s ship at %s %s!' % (chr(x + 65), y + 1))
            battleShip.checkIfSunk(False, userMove)
            return


def main():
    global hits  # Tracks computer hits and is used to determine whether or not to continue the targeting phase
    global targetStack  # List containing all possible, valid moves following a hit by the computer
    global parityDictionary  # Dictionary used to determine the lowest hitpoint ship remaining to adjust parity in computer hunting phase.
    hits = 0
    targetStack = []
    computerTargeting = False
    playing = True
    fleetDictionary = {'Aircraft Carrier': 5,
                       'Battleship': 4,
                       'Submarine': 3,
                       'Destroyer': 3,
                       'Patrol Boat': 2}
    ships = {key[0]: fleetDictionary.get(key) for key in
             fleetDictionary}  # The dictionary key is first letter of ship and the associated values are ship hitpoints
    parityDictionary = dict(ships)
    battleShip = BattleshipGame(ships)
    for computerShip in fleetDictionary:
        computerPlaceShips(battleShip, computerShip, fleetDictionary[computerShip])
    battleShip.drawBoard(True)
    print('Welcome to Battleship! Please place your ships.')
    for userShip in fleetDictionary:
        userPlaceShips(battleShip, userShip, fleetDictionary[userShip])
    battleShip.incrementRounds()
    battleShip.drawBoard(True)
    input('You have placed all of your ships. Please press ENTER to continue.')
    print('Fire at the enemy fleet...')
    while playing:
        userMakesMove(battleShip)
        userWin = battleShip.checkWinning(False)
        if userWin:
            battleShip.drawBoard(True)
            print('Congratulations! You have won against the computer.')
            playing = False
            break
        computerTargeting = computerMakesMove(battleShip, ships, computerTargeting)
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
