# This solution was build using python 2.7
# Author: Tomas F. Venegas Bernal tf.venegas10@uniandes.edu.co

import random
import numpy as np


# This is a simple class that builds the Board that will be shown to the user.
class Board:
    def __init__(self, height, width):
        self.matrix = np.chararray((height, width))
        self.matrix[:] = "."

    # This method allows us to pass from the matrix to the console representation
    def toString(self):
        sttr = "   "
        for i in xrange(width):
            sttr += "  " + str(i) + " "
            if i < 10:
                sttr += " "
        sttr += "\n\n"
        for i in xrange(len(self.matrix)):
            sttr += str(i) + " |"
            for j in range(len(self.matrix[0])):
                sttr += "  " + self.matrix[i][j] + "  "
            sttr += "|\n"
        return sttr


# This function is charged of building the game: the initial board with the specified dimensions
# and the random mines on it.
def buildGame(height, width, nMines):
    # real board - with hidden values
    realBoard = np.zeros((height, width))

    # shown board - with specified caracters
    shownBoard = Board(height, width)

    tempMines = []
    i, j = 0, 0
    # First of all we are going to build randomly the set of nMines mines as a set of coordinates
    while len(tempMines) != nMines:
        i = random.randint(0, height - 1)
        j = random.randint(0, width - 1)
        if (i, j) not in tempMines:
            tempMines.append((i, j))

    # Now we are going to go through the set modifing only the boxes with the coordinates of a mine
    # we'll set the value to -1 and we'll add 1 to each adjacent box
    # we won't check if it already is a mine beacause we will reset all the mines to -1 at the end (to optimize)

    for (i, j) in tempMines:
        # we will set this at the end realBoard[i][j]=-1
        # modify lower boxes
        if i + 1 < height:
            realBoard[i + 1][j] += 1
            if j + 1 < width:
                realBoard[i + 1][j + 1] += 1
            if j - 1 >= 0:
                realBoard[i + 1][j - 1] += 1
        # modify upper boxes
        if i - 1 >= 0:
            realBoard[i - 1][j] += 1
            if j + 1 < width:
                realBoard[i - 1][j + 1] += 1
            if j - 1 >= 0:
                realBoard[i - 1][j - 1] += 1
        # modify the right box
        if j + 1 < width:
            realBoard[i][j + 1] += 1
        # modify the left box
        if j - 1 >= 0:
            realBoard[i][j - 1] += 1

    for (i, j) in tempMines:
        realBoard[i][j] = -1

    return realBoard, shownBoard, tempMines


# This function defines the procedure to follow when the user decides to uncover cell (i,j)
# (it's a recursive function)
def uncover(i, j, realBoard, shownBoard, tempMines):
    if i < 0 or j < 0 or i >= len(realBoard) or j >= len(realBoard[0]) or shownBoard.matrix[i][j] not in [".", "P"]:
        return False
    if realBoard[i][j] == -1:
        for (l, c) in tempMines:
            shownBoard.matrix[l][c] = "*"
        return True
    if realBoard[i][j] > 0:
        shownBoard.matrix[i][j] = str(realBoard[i][j])
        return False
    else:
        shownBoard.matrix[i][j] = "-"
# recursive calls
        uncover(i + 1, j, realBoard, shownBoard, tempMines)
        uncover(i + 1, j - 1, realBoard, shownBoard, tempMines)
        uncover(i + 1, j + 1, realBoard, shownBoard, tempMines)
        uncover(i - 1, j, realBoard, shownBoard, tempMines)
        uncover(i - 1, j - 1, realBoard, shownBoard, tempMines)
        uncover(i - 1, j + 1, realBoard, shownBoard, tempMines)
        uncover(i, j + 1, realBoard, shownBoard, tempMines)
        uncover(i, j - 1, realBoard, shownBoard, tempMines)
        return False

#This method is charged of doing the two possible actions
def doAction(line, column, action, realBoard, shownBoard, missingMines, setMines, tempMines, nMines):
    #Mark case
    if action == "M":
        if shownBoard.matrix[line][column] == "P":
            shownBoard.matrix[line][column] = "."
            if realBoard[line][column] == -1:
                missingMines += 1
                setMines -= 1
        elif shownBoard.matrix[line][column] == ".":
            shownBoard.matrix[line][column] = "P"
            if realBoard[line][column] == -1:
                missingMines -= 1
                setMines += 1
                if missingMines == 0 and setMines == nMines:
                    return (True, True, missingMines, setMines)
    #Uncover case
    else:
        return (uncover(line, column, realBoard, shownBoard, tempMines), False, missingMines, setMines)
    return (False, False, missingMines, setMines)


if __name__ == '__main__':

    # variable to make the game re-playable
    again = True
    while (again):
        # Initialize with impossible values
        height, width, nMines = -1, -1, -1

        # loop to read the initial game values
        while height <= 0 or width <= 0 or nMines <= 0 or nMines > height * width:
            print("We are going to play Minesweeper.")
            # Request initial input
            print(
                "Please enter the board s height, width, and number of mines you want separated by spaces (ex:'10 20 10')")
            # read input
            line = raw_input()
            tempArr = line.split(" ")
            # constants instantiation
            try:
                height, width, nMines = int(tempArr[0]), int(tempArr[1]), int(tempArr[2])
            except:
                pass

        # game crated
        realBoard, shownBoard, tempMines = buildGame(height, width, nMines)

        # These global parameters need to be defined!

        # boolean for when to stop
        gameOver = False
        # boolean for when the player was victorious
        victory = False

        # number of missing mines to be found by the player (to win the game)
        # a mine is considered found when the player places a flag on it.
        missingMines = nMines
        # number of flags set by the user
        setMines = 0

        while not gameOver:
            # print board
            print(shownBoard.toString())
            line, column, action = -1, -1, "O"

            # variable to evaluate if the user made a mistake on the input
            entries = 0

            # read input loop
            while line < 0 or line >= height or column < 0 or column >= width or action not in ["U", "M"]:
                if entries > 0:
                    print(
                        "You entered an INCORRECT value, this game is not that sophisticated please follow the guideline.")
                entries += 1
                print(
                    "Please enter the cell you want to modify separated by spaces in the form <line> <column> <action>")
                print("The possible actions are: M : mark or un-mark a cell, U : uncover a cell marked as '.' ")
                inp = raw_input()
                try:
                    tempArr = inp.split(" ")
                    line, column, action = int(tempArr[0]), int(tempArr[1]), tempArr[2]
                except:
                    pass

            gameOver, victory, missingMines, setMines = doAction(line, column, action, realBoard, shownBoard,
                                                                 missingMines, setMines, tempMines, nMines)

        if victory:
            print(shownBoard.toString())
            print("Congratulations! You have won :)")
        else:
            print(shownBoard.toString())
            print("Sorry! You have lost. Better chance next time.")

        print("Do you want to play again?")
        print("Mark 'YES' or 'yes' or 'y' or 'Y' for YES.")
        print("Other input for NO")
        inp = raw_input()
        try:
            if inp not in ["yes", "YES", "Y", "y"]:
                again = False
        except:
            again = False
