import pygame
pygame.font.init()
import random

# Window setup:

WIDTH, HEIGHT = 540, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts:
FONT_CUBE = pygame.font.SysFont('comicsans', 40)
FONT_GRID = pygame.font.SysFont('comicsans', 40)

def valid(board, num, pos):
    # check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(board):

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)

    return None


class Grid:

    board = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.model = None

    def draw(self):
        # draw grid lines
        gap = self.width // self.cols
        for i in range(self.rows + 1):
            line_thickness = 1
            # draw horizontal lines:
            pygame.draw.line(WIN, BLACK, (0, i * gap), (self.width, i *  gap), line_thickness)
            # draw vertical lines:
            pygame.draw.line(WIN, BLACK, (i * gap, 0), (i * gap, self.height), line_thickness)

        # draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw()

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def select(self, row, col):
        if self.selected:
            row_unselect, col_unselect = self.selected
            self.cubes[row_unselect][col_unselect].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def solve(self):
        
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True
                
                self.model[row][col] = 0

        return False

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False

        return True

    def solve_game(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_game():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

class Cube:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self):
        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = FONT_CUBE.render(str(self.temp), 1, GREY)
            WIN.blit(text, (x + 5, y + 5))
        elif not(self.value == 0):
            text = FONT_CUBE.render(str(self.value), 1, BLACK)
            WIN.blit(text, (x + (gap // 2 - text.get_width() // 2), y + (gap // 2 - text.get_height() // 2)))

        if self.selected:
            pygame.draw.rect(WIN, BLACK, (x, y, gap, gap), 6)

    def set_temp(self, val):
        self.temp = val

    def set(self, val):
        self.value = val

    def draw_change(self, win=True):
        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(WIN, WHITE, (x, y, gap, gap), 0)

        text = FONT_CUBE.render(str(self.value), 1, BLACK)
        WIN.blit(text, (x + (gap // 2 - text.get_width() // 2), y + (gap // 2 - text.get_height() // 2)))

        if win:
            pygame.draw.rect(WIN, GREEN, (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(WIN, RED, (x, y, gap, gap), 3)

def draw_window(board):
    WIN.fill(WHITE)

    board.draw()
    
def main():
    board = Grid(9, 9, 540, 540)
    key = None
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_game()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print('Success')
                        else:
                            print('Wrong')
                        key = None

                    if board.is_finished():
                        print('Game over')
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        draw_window(board)
        pygame.display.update()

if __name__ == '__main__':
    main()
pygame.quit()