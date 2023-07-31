import pygame

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
    win.blit(text, (540 - 160, 560))
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