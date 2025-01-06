import pygame
from Constants import BLACK, BLUE, GREEN, RED, WHITE, ROWS, COLUMNS, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT

class MapRenderer:
    def __init__(self, screen):
        self.screen = screen 

    def drawGrid(self):
        for i in range(0, GRID_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, WHITE, (i, 0), (i, GRID_HEIGHT))  # Vertical lines
        for j in range(0, GRID_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, WHITE, (0, j), (GRID_WIDTH, j))  # Horizontal lines

    def drawMap(self, grid):
        self.screen.fill(BLACK)
        for i in range(ROWS):
            for j in range(COLUMNS):
                colour = None
                if grid[i][j] == 0:
                    colour = GREEN
                elif grid[i][j] == 1:
                    colour = BLACK
                elif grid[i][j] == 2:
                    colour = WHITE
                elif grid[i][j] == 3:
                    colour = BLUE
                elif grid[i][j] == 4:
                    colour = RED

                if colour is not None:
                    pygame.draw.rect(
                        self.screen,
                        colour,
                        (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
        self.drawGrid()
