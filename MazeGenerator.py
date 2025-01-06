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
    
    def inGrid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.columns

    def checkSquare(self, row, col):
        return self.inGrid(row, col) and self.grid[row][col] != 1 and self.grid[row][col] != 2

    def deadEnd(self, row, col):
        dead_end = True
        if self.checkSquare(row+2, col):
            dead_end = False
        if self.checkSquare(row-2, col):
            dead_end = False
        if self.checkSquare(row, col+2):
            dead_end = False
        if self.checkSquare(row, col-2):
            dead_end = False
        return dead_end
    
    def checkNeighbours(self, row, col):
        options = []
        for option in [[row+2, col], [row-2, col], [row, col+2], [row, col-2]]:
            if self.checkSquare(option[0], option[1]):
                options.append(option)
        chosen = random.choice(options)
        return chosen[0], chosen[1]

    def generateMaze(self):
        self.generateBaseGrid()
        current = [1, 1]
        self.grid[current[0]][current[1]] = 2
        movements = [current]

        while movements:
            if self.deadEnd(current[0], current[1]):
                movements.pop()
                if movements:
                    current = movements[-1]
                continue
        
            next_row, next_col = self.checkNeighbours(current[0], current[1])
            movements.append([next_row, next_col])
            self.grid[next_row][next_col] = 2
            self.grid[(current[0]+next_row)//2][(current[1]+next_col)//2] = 2
            current = [next_row, next_col]
        return self.grid

if __name__ == "__main__":
    mazeGen = MazeGenerator()
    maze = mazeGen.generateMaze()
    print(mazeGen.displayMaze())


