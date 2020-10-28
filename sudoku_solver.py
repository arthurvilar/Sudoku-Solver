def draw_board(board):
    for r in range(len(board)):
        for c in range(len(board[r])):
            print(f'{board[r][c]} ', end='')
        print()


# check if number n can be placed on board[row][col]
def possible(row, col, n):
    global board

    # check row
    if n in board[row]:
        return False

    # check column
    for i in range(len(board)):
        if board[i][col] == n:
            return False

    # check square
    y = row//3 * 3
    x = col//3 * 3
    for i in range(3):
        for j in range(3):
            if board[i+y][j+x] == n:
                return False

    return True


# find a solution using backtracking
def solve():
    global board

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                for n in range(1, 10):
                    if possible(i, j, n):
                        board[i][j] = n
                        solve()
                        board[i][j] = 0 # backtrack
                return

    print('\n----SOLUTION:----\n')
    draw_board(board)


def main():

    global board
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

    print('\n-----PUZZLE:-----\n')
    draw_board(board)
    solve()


if __name__ == '__main__':
    main()
