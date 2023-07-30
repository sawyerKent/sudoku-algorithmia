# sodoku-algorithmia

import pygame
import time
pygame.font.init()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
GREY = (128, 128, 128)
RED = (255, 0, 0)
SAILOR_BLUE = (0, 32, 63)
MINT = (173, 239, 209)

"""
    colors needed for: Grid::draw(), Cube::draw(), 
    Cube::draw_change(), Cube::redraw_window()
"""

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        # TODO: add logic to update the model
        return

    def place(self, val):
        # TODO: add logic
        return

    def sketch(self, val):
        # TODO: add sketch logic
        return

    def draw(self):
        # TODO: add logic
        return

    def select(self, row, col):
        # TODO: add logic
        return

    def clear(self):
        # TODO: add logic
        return

    def click(self, pos):
        # TODO: add logic
        return

    def is_finished(self):
        # TODO: add logic
        return

    def solve(self):
        # TODO: Add logic for solving the puzzle

        return False

    def solve_gui(self):
        # TODO: Add logic for solving the gui puzzle
        
        return False
    
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        # TODO: add logic
        return

    def draw_change(self, win, g=True):
        # TODO: add logic
        return

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val