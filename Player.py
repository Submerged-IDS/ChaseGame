import pygame

from Constants import ROWS, COLUMNS, BLUE, RED

"""
# up    = 1 #
# right = 2 #
# down  = 3 #
# left  = 4 #
"""


class Player:
    def __init__(self, player_id, x, y, colour, grid):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.colour = colour
        self.is_it = False
        self.grid = grid

        self.grid[self.y][self.x] = player_id


    def isInGrid(self, row, col):
        return 0 <= row < ROWS and 0 <= col < COLUMNS

    def move(self, direction):

        new_x, new_y = self.x, self.y
        if direction == 1:
            new_y -= 1
        elif direction == 2:
            new_x += 1
        elif direction == 3:
            new_y += 1
        elif direction == 4:
            new_x -= 1
        
        if self.isInGrid(row=new_y, col=new_x) and self.grid[new_y][new_x] != 1:
            self.grid[self.y][self.x] = 2
            self.x, self.y = new_x, new_y
            self.grid[self.y][self.x] = self.player_id
