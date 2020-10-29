import pygame
pygame.font.init()


class Grid:
    board = [
        [5, 0, 1, 0, 7, 2, 0, 0, 0],
        [6, 0, 9, 0, 0, 0, 0, 0, 0],
        [8, 0, 7, 5, 4, 0, 6, 0, 3],
        [4, 9, 6, 0, 0, 7, 8, 0, 0],
        [0, 0, 3, 0, 0, 4, 0, 0, 6],
        [2, 1, 0, 0, 9, 0, 0, 4, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 5, 0, 6, 3, 4, 2, 9],
        [0, 0, 4, 0, 2, 8, 5, 6, 1]
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
        for i in range(self.rows):
            for j in range(self.cols):
                self.model = self.cubes[i][j].value

    def draw(self):
        # Draw grid lines
        gap = self.width // 9

        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)   # horizontal lines
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)  # vertical lines

        # Draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, col, row):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = row, col

    def click(self, pos):
        i, j = pos

        if i < self.width and j < self.height:
            gap = self.width // 9
            x = i // gap
            y = j // gap
            return x, y
        else:
            return None


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
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        if self.value == 0:
            # text = font.render(str(self.temp), 1, (128, 128, 128))
            # win.blit(text, (x + 5, y + 5))
            pass
        else:
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap//2 - text.get_width()//2), y + (gap//2 - text.get_height()//2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


def redraw_window(win, board):
    win.fill((255, 255, 255))
    board.draw()


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('Sudoku')
    board = Grid(9, 9, 540, 540, win)
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])

        redraw_window(win, board)
        pygame.display.update()


main()
pygame.quit()
