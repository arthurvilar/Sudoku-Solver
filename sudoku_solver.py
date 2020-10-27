def draw_board(board):
    for r in range(len(board)):
        for c in range(len(board[r])):
            print(f'{board[r][c]} ', end='')
        print()


def main():

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

    draw_board(board)


if __name__ == '__main__':
    main()
