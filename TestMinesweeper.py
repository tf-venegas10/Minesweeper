# This solution was build using python 2.7
# Author: Tomas F. Venegas Bernal tf.venegas10@uniandes.edu.co
# Tests file
import unittest
from Minesweeper import *
from random import randint
class TestMethods(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.width = randint(2, 100)
        self.height = randint(2, 100)
        self.nMines = randint(min(self.width,self.height), self.width*self.height)
        self.realBoard, self.shownBoard, self.tempMines = buildGame(self.height, self.width, self.nMines)

        #define global parameters
        self.gameOver = False
        self.victory = False
        self.missingMines = self.nMines
        self.setMines = 0

    #tests build specified parameters
    def test_build(self):
        #test that all mines are correctly set up
        for (i,j) in self.tempMines:
            self.assertEqual(self.realBoard[i][j],-1)

        #test that the number of mines selected is the actual number used
        self.assertEqual(len(self.tempMines), self.nMines)

        self.assertEqual(len(self.realBoard), self.height)

        self.assertEqual(len(self.realBoard[0]), self.width)

    def test_uncover_mine(self):
        #uncover mine
        self.gameOver=uncover(self.tempMines[0][0], self.tempMines[0][1],self.realBoard,self.shownBoard,self.tempMines)
        for (i,j) in self.tempMines:
            self.assertEqual(self.shownBoard.matrix[i][j],"*")
        self.assertEqual(self.gameOver,True)

    def test_uncover_other(self):
        for i in xrange (self.height):
            for j in xrange(self.width):
                if (i,j) not in self.tempMines:
                    self.gameOver=uncover(i,j,self.realBoard,self.shownBoard,self.tempMines)
                    self.assertEqual(self.gameOver,False)

    def test_doAction(self):
        doAction(0,0,"M",self.realBoard,self.shownBoard,self.missingMines,self.setMines, self.tempMines, self.nMines)
        self.assertEqual(self.shownBoard.matrix[0][0],"P")
        doAction(0,1,"U",self.realBoard,self.shownBoard,self.missingMines,self.setMines, self.tempMines, self.nMines)
        self.assertNotEqual(self.shownBoard.matrix[0][1],".")

    def test_win(self):
        for (i, j) in self.tempMines:
            self.gameOver, self.victory, self.missingMines, self.setMines=doAction(i,j,"M",self.realBoard,self.shownBoard,self.missingMines,self.setMines, self.tempMines, self.nMines)
        self.assertEqual(self.victory,True)
        self.assertEqual(self.gameOver,True)

    @classmethod
    def tearDown(self):
        self.gameOver=False
        self.victory=False
if __name__ == '__main__':
    unittest.main()
