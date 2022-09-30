import pygame
pygame.font.init()
import queue

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='C:/Users/andra/OneDrive/Desktop/python/Shortest Path Finder/path_main.log', level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(name)s: #%(lineno)d: %(message)s')

# Window setup:

WIDTH, HEIGHT = 540, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shortest Path Finder')

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts:
FONT_CUBE = pygame.font.SysFont('serif', 40)
FONT_GRID = pygame.font.SysFont('serif', 40)

# -------------------

def find_start(board, start):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None

def find_end(board, end):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == end:
                return i, j

    return None

def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors

def draw_game_over(text):
    draw_text = FONT_GRID.render(text, 1, RED)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

# -------------------------------------------------

class Grid:

    board = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", "#", " ", " ", "#", " ", "#"],
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

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def solve_game(self):
        self.update_model()
        logger.info(self.model)
        start = 'O'
        end = 'X'
        start_pos = find_start(self.model, start)
        end_pos = find_start(self.model, end)

        q = queue.Queue()
        q.put((start_pos, [start_pos]))

        visited = set()

        while not q.empty():
            current_pos, path = q.get()
            row, col = current_pos

            for r, ro in enumerate(self.model):
                for c, co in enumerate(ro):
                    if (r, c) in path:
                        self.cubes[r][c].draw_change('yellow')
                        self.update_model()

            pygame.display.update()
            pygame.time.delay(300)
     
            if current_pos == end_pos:
                self.draw_shortest_path('Shortest path', path)
                return

            neighbors = find_neighbors(self.model, row, col)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                r, c = neighbor
                if self.model[r][c] == '#':
                    continue

                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)

        draw_game_over('Unsolvable')

    def draw_shortest_path(self, text, path):
        for r, ro in enumerate(self.model):
                    for c, co in enumerate(ro):
                        if (r, c) in path:
                            self.cubes[r][c].draw_change('green')
                            self.update_model()

        draw_text = FONT_GRID.render(text, 1, RED)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)


class Cube:

    def __init__(self, value, row, col, width, height):
        self.value = value
        # self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self):
        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        text = FONT_CUBE.render(str(self.value), 1, BLACK)
        WIN.blit(text, (x + (gap // 2 - text.get_width() // 2), y + (gap // 2 - text.get_height() // 2)))

        if self.selected:
            pygame.draw.rect(WIN, BLACK, (x, y, gap, gap), 6)

    def set(self, val):
        self.value = val

    def draw_change(self, color='white'):
        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        if color == 'green':
            pygame.draw.rect(WIN, GREEN, (x, y, gap, gap), 0)
        elif color == 'yellow':
            pygame.draw.rect(WIN, YELLOW, (x, y, gap, gap), 0)
        else:
            pygame.draw.rect(WIN, WHITE, (x, y, gap, gap), 0)

        text = FONT_CUBE.render(str(self.value), 1, BLACK)
        WIN.blit(text, (x + (gap // 2 - text.get_width() // 2), y + (gap // 2 - text.get_height() // 2)))

def draw_window(board):
    WIN.fill(WHITE)

    board.draw()
    
def main():
    rows = 9
    cols = 9
    width = 540
    height = 540
    board = Grid(rows, cols, width, height)
    key = None
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    board.solve_game()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].value == '#':
                        board.cubes[i][j].value = ' '
                    elif board.cubes[i][j].value == ' ':
                        board.cubes[i][j].value = '#'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        draw_window(board)
        pygame.display.update()

if __name__ == '__main__':
    main()
pygame.quit()