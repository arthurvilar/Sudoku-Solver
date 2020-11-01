import pygame
import time
import tkinter as tk
from tkinter import messagebox
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
        self.model = None       # board without the temp values
        self.update_model()
        self.selected = None    # position (row and column) of the selected cube
        self.win = win

    # generates a board without the temp values to check for a solution
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # check if it's possible to place the value val in the selected cube and places it
    def place(self, val):
        i, j = self.selected
        if self.cubes[i][j].value == 0:
            self.cubes[i][j].set(val)
            self.update_model()

            if possible(self.model, val, (i, j)) and self.solve():
                return True
            else:
                self.cubes[i][j].set(0)
                self.update_model()
                return False

    # draw the grid lines and the cubes
    def draw(self):
        # draw grid lines
        gap = self.width // 9   # size of each row and column

        for i in range(self.rows + 1):
            if i % 3 == 0:
                thick = 3
                # horizontal lines and vertical lines
                pygame.draw.line(self.win, (0, 0, 0), (0, i * gap + 1), (self.width + 2, i * gap + 1), thick)
                pygame.draw.line(self.win, (0, 0, 0), (i * gap + 1, 0), (i * gap + 1, self.height), thick)
            else:
                thick = 1
                pygame.draw.line(self.win, (0, 0, 0), (3, i * gap + 1), (self.width, i * gap + 1), thick)
                pygame.draw.line(self.win, (0, 0, 0), (i * gap + 1, 3), (i * gap + 1, self.height), thick)

        # draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    # select the cube that was clicked
    def select(self, col, row):
        # reset every cube
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        # select the specified cube
        self.cubes[row][col].selected = True
        self.selected = row, col

    # find the row and column of the clicked cube and returns it,if the click was outside the board return none
    def click(self, pos):
        i, j = pos
        # check if the click was inside the board
        if i < self.width and j < self.height:
            gap = self.width // 9
            x = i // gap
            y = j // gap
            return int(x), int(y)
        else:
            return None

    # check if the board is complete
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    # solve the model board, but don't change the cubes values, to see if it's a valid solution
    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            i, j = find

        # try every number until it finds one that fits
        for n in range(1, 10):
            if possible(self.model, n, (i, j)):
                self.model[i][j] = n
                if self.solve():
                    return True
                self.model[i][j] = 0  # backtrack
        return False

    # solve the board with a simple animation to show the backtracking working
    def auto_solve(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            i, j = find

        # try every number until it finds one that fits
        for n in range(1, 10):
            if possible(self.model, n, (i, j)):
                self.model[i][j] = n
                self.cubes[i][j].set(n)
                self.cubes[i][j].draw_change(self.win, True)    # green rectangle
                self.update_model()
                pygame.display.update()
                pygame.time.delay(5)

                if self.auto_solve():
                    return True

                self.model[i][j] = 0    # backtrack
                self.cubes[i][j].set(0)
                self.cubes[i][j].draw_change(self.win, False)   # red rectangle
                self.update_model()
                pygame.display.update()
                pygame.time.delay(5)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    # draw the number inside the cube
    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width // 9   # size of each row and column
        x = self.col * gap      # start position of the column and row
        y = self.row * gap

        # print the temporary numbers
        '''if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))'''

        # print the official values
        if self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (1 + x + (gap//2 - text.get_width()//2), 3 + y + (gap//2 - text.get_height()//2)))

        # print a red rectangle around the selected cube
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x + 1, y + 1, gap, gap), 3)

    # draw the animation of the auto solve
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width // 9  # size of each row and column
        x = self.col * gap     # start position of the column and row
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x + 1, y + 1, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (1 + x + (gap//2 - text.get_width()//2), 3 + y + (gap//2 - text.get_height()//2)))

        if g:
            pygame.draw.rect(win, (0, 255, 0), (x + 1, y + 1, gap, gap), 3)     # green rectangle
        else:
            pygame.draw.rect(win, (255, 0, 0), (x + 1, y + 1, gap, gap), 3)     # red rectangle

    # set cube's value to val
    def set(self, val):
        self.value = val


# find an empty position and return the row, column
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i, j

    return None


# check if number n can be placed on board[row][col]
def possible(board, n, pos):
    row, col = pos

    # check row
    for i in range(len(board[row])):
        if board[row][i] == n and col != i:
            return False

    # check column
    for i in range(len(board)):
        if board[i][col] == n and row != i:
            return False

    # check box
    y = row//3 * 3
    x = col//3 * 3
    for i in range(y, y+3):
        for j in range(x, x+3):
            if board[i][j] == n and (i, j) != pos:
                return False

    return True


# refresh the window
def redraw_window(win, board, t, strikes, pencil):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 35)

    # draw strikes
    text = fnt.render(f"Errors: {strikes}/5 ", 1, (255, 0, 0))
    win.blit(text, (15, 560))

    # draw time
    text = fnt.render("Time: " + format_time(t), 1, (0, 0, 0))
    win.blit(text, (540 - 135, 560))

    # draw pencil mode
    if pencil:
        text = fnt.render("Pencil: ON", 1, (0, 0, 0))
    else:
        text = fnt.render("Pencil: OFF", 1, (0, 0, 0))
    win.blit(text, (200, 560))

    # draw board and numbers
    board.draw()


# convert the time in seconds to minutes:seconds
def format_time(secs):
    sec = secs % 60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


# display a message box if you lost the game
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    win = pygame.display.set_mode((543, 600))   # set the display
    pygame.display.set_caption('Sudoku')        # name of the window
    board = Grid(9, 9, 540, 540, win)           # set the board
    start = time.time()
    strikes = 0
    pencil = False
    run = True
    key = None

    while run and strikes < 5 and not board.is_finished():

        play_time = round(time.time() - start)

        for event in pygame.event.get():        # get events
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # Numbers
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

                # Auto solve
                if event.key == pygame.K_SPACE:
                    board.auto_solve()

                # Pencil
                if event.key == pygame.K_p:
                    if pencil:
                        pencil = False
                    else:
                        pencil = True

                # Select with arrow keys
                if event.key == pygame.K_UP and board.selected:
                    i, j = board.selected
                    if i >= 1:
                        board.select(j, i - 1)
                if event.key == pygame.K_DOWN and board.selected:
                    i, j = board.selected
                    if i <= 7:
                        board.select(j, i + 1)
                if event.key == pygame.K_RIGHT and board.selected:
                    i, j = board.selected
                    if j <= 7:
                        board.select(j + 1, i)
                if event.key == pygame.K_LEFT and board.selected:
                    i, j = board.selected
                    if j >= 1:
                        board.select(j - 1, i)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()    # get the mouse cursor position
                clicked = board.click(pos)      # get the row and column of pos
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            '''
            if pencil:
                board.sketch(key)
            else:
                do the real stuff
            if board.is_finished():
                game over you won
            '''
            if board.place(key):
                print('success')
            else:
                print('wrong')
                strikes += 1

            key = None

            if strikes >= 5:
                message_box('You Lost!', None)

        pygame.display.update()
        redraw_window(win, board, play_time, strikes, pencil)

    if board.is_finished():
        play_time = round(time.time() - start)
        message_box('You won!', f'Time: {format_time(play_time)}')


main()
pygame.quit()
