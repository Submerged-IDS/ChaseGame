import pygame
import time
import random

ROWS = 11
COLUMNS = 11
CELL_SIZE = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

"""
Create a 2D array
# 0 - unvisited #
# 1 - walls     #
# 2 - visited   #
"""

class MazeGenerator:
    def __init__(self):
        self.rows = ROWS
        self.columns = COLUMNS
        self.grid = [[0 for _ in range(self.columns)]for _ in range(self.rows)]

    def generateBaseGrid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if i % 2 == 0 or j % 2 == 0:
                    self.grid[i][j] = 1
    
    def displayMaze(self):
        return '\n'.join([''.join(map(str, row)) for row in self.grid])

        

if __name__ == "__main__":
    mazeGen = MazeGenerator()
    maze = mazeGen.generateBaseGrid()
    print(mazeGen.displayMaze())


