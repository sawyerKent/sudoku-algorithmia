import pygame

from utils import utils

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
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if utils.valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, utils.SAILOR_BLUE, (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, utils.SAILOR_BLUE, (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def backtrace(self):
        self.update_model()
        find = utils.find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if utils.valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.backtrace():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False
    
    def constraint_propagation(self):
        self.update_model()

        # Using constraint propagation
        domains, unassigned = self.initialize_domains()
        queue = [((row, col), neighbor) for row in range(self.rows) for col in range(self.cols) if self.model[row][col] == 0 for neighbor in self.neighbors((row, col))]

        if not self.ac3(queue, domains):
            return False

        # If any domain is empty, there's no solution
        for domain in domains.values():
            if not domain:
                return False

        # Backtracking with constraint propagation
        return self.backtracking_search(domains, unassigned)


    def initialize_domains(self):
        domains = {}
        unassigned = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.model[row][col] == 0:
                    domains[(row, col)] = {i for i in range(1, 10)}
                    unassigned.append((row, col))
                else:
                    domains[(row, col)] = {self.model[row][col]}
        return domains, unassigned

    def revise(self, xi, xj, domains):
        revised = False
        values_xi = domains[xi].copy()
        for x in values_xi:
            if all(not utils.valid(self.model, x, xi) for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised

    def ac3(self, queue, domains):
        while queue:
            xi, xj = queue.pop(0)
            if self.revise(xi, xj, domains):
                if not domains[xi]:
                    return False
                for neighbor in self.neighbors(xi):
                    queue.append((neighbor, xi))
        return True

    def neighbors(self, xi):
        neighbors = set()
        row, col = xi
        # Row constraints
        for i in range(9):
            if i != col:
                neighbors.add((row, i))
        # Column constraints
        for i in range(9):
            if i != row:
                neighbors.add((i, col))
        # Subgrid constraints
        subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(subgrid_row, subgrid_row + 3):
            for j in range(subgrid_col, subgrid_col + 3):
                if (i, j) != (row, col):
                    neighbors.add((i, j))
        return neighbors


    def backtracking_search(self, domains, unassigned):
        if not unassigned:
            return True

        var = min(unassigned, key=lambda x: len(domains[x]))
        unassigned.remove(var)
        row, col = var

        for value in domains[var]:
            if utils.valid(self.model, value, var):
                self.model[row][col] = value
                self.cubes[row][col].set(value)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.backtracking_search(domains, unassigned):
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        unassigned.append(var)
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
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, utils.WHITE)
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, utils.SAILOR_BLUE)
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, utils.WHITE, (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, utils.MINT, (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, utils.SAILOR_BLUE)
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, utils.SAILOR_BLUE, (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, utils.WHITE, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val