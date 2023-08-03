import pygame
import random

"""
    colors needed for: Grid::draw(), Cube::draw(), 
    Cube::draw_change(), Cube::redraw_window()
"""

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
GREY = (128, 128, 128)
RED = (255, 0, 0)
SAILOR_BLUE = (0, 32, 63)
MINT = (173, 239, 209)

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i,j)  # row, col

    return None

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def redraw_window(win, board, time, strikes):
    win.fill(MINT)
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, SAILOR_BLUE)
    win.blit(text, (340, 540))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, RED)
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
        if board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_board(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i
            if solve_board(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def create_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill the diagonal sub-grids
    for i in range(0, 9, 3):
        fill_diagonal(board, i, i)

    # Solve the rest of the board
    solve_board(board)

    # Remove symmetric pairs to create the puzzle
    remove_symmetric_pairs(board)
    
    return board

def fill_diagonal(board, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

def remove_symmetric_pairs(board):
    pairs_to_remove = (81 - random.randint(20, 40)) // 2
    for _ in range(pairs_to_remove):
        row, col = random.randint(0, 4), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 4), random.randint(0, 8)
        board[row][col] = 0
        board[8 - row][8 - col] = 0

def sudoku_to_exact_cover(grid):
    N = 9
    M = N * N
    matrix = [[0] * 324 for _ in range(729)]

    # Filling constraints
    for i in range(N):
        for j in range(N):
            for n in range(N):
                k = i * N + j
                row_num = k * N + n

                # Cell constraint
                matrix[row_num][k] = 1

                # Row constraint
                matrix[row_num][M + i * N + n] = 1

                # Column constraint
                matrix[row_num][2 * M + j * N + n] = 1

                # Box constraint
                box_num = (i // 3) * 3 + (j // 3)
                matrix[row_num][3 * M + box_num * N + n] = 1

                # If the cell is already filled in the grid, reduce it to a single possibility
                if grid[i][j] != 0:
                    for num in range(N):
                        if num != grid[i][j] - 1:
                            matrix[k * N + num] = [0] * 324

    return matrix