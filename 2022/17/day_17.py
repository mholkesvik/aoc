#! /usr/bin/python3

SHAPES = [
    ['|..@@@@.|'],

    ['|...@...|',
     '|..@@@..|',
     '|...@...|'],

     ['|....@..|',
      '|....@..|',
      '|..@@@..|'
     ],

     ['|..@....|',
      '|..@....|',
      '|..@....|',
      '|..@....|'],

     ['|..@@...|',
      '|..@@...|'],
]

BOTTOM = '+-------+'
EMPTY = '|.......|'

BOARD = [
    BOTTOM
]


def add_shape(shape, board):
    # exactly 3 blank lines
    num_empty = 0
    for row in board:
        if ('-' not in row) and ('#' not in row) and ('@' not in row):
            num_empty += 1

    if num_empty < 3:
        board = [EMPTY] * (3-num_empty) + board
    elif num_empty > 3:
        board = board[num_empty-3:]

    for row in shape[::-1]:
        board = [row] + board

    return board


def print_board(board):
    for line in board:
        print(line)


def get_shape_idxs(board):
    for i, row in enumerate(board):
        for j, c in enumerate(row):
            if c == '@':
                yield (i, j)


def is_shape_at_rest(board):
    for idx in get_shape_idxs(board):
        if board[idx[0]+1][idx[1]] not in ['.','@']:
            return True
    return False


def can_shift(board, shift_dir):
    for idx in get_shape_idxs(board):
        shift_col_idx = idx[1]-1 if shift_dir == '<' else idx[1]+1
        if board[idx[0]][shift_col_idx] in ['|','#']:
            return False
    return True

def shift(board, shift_dir):
    shift_move = -1 if shift_dir == '<' else 1
    shift_idx = [(idx[0], idx[1] + shift_move) \
        for idx in get_shape_idxs(board)]
    new_board = grid_replace(board, '@', '.')
    for new_idx in shift_idx:
        row = new_board[new_idx[0]][:]
        new_board[new_idx[0]] = row[:new_idx[1]] + '@' + row[new_idx[1] + 1:]

    return new_board


def grid_replace(board, a, b):
    new_board = []
    for row in board:
        new_board.append(row.replace(a, b))
    return new_board


def fall(board):
    fall_idxs = [(i[0]+1, i[1]) for i in get_shape_idxs(board)]
    new_board = grid_replace(board, '@', '.')

    for new_idx in fall_idxs:
        row = new_board[new_idx[0]][:]
        new_board[new_idx[0]] = row[:new_idx[1]] + '@' + row[new_idx[1] + 1:]

    return new_board


ROCK_COUNT_MAX = 2022
from itertools import cycle

with open('input.txt', 'r', encoding="utf8") as f:
    jets = cycle(f.read())
    b = BOARD
    for rock_ct, s in enumerate(cycle(SHAPES), 0):
        if rock_ct >= ROCK_COUNT_MAX:
            break

        b = add_shape(s, b)
        jet = next(jets)
        # print_board(b)

        if can_shift(b, jet):
            b = shift(b, jet)
        while not is_shape_at_rest(b):
            jet = next(jets)
            b = fall(b)
            if can_shift(b, jet):
                b = shift(b, jet)

        b = grid_replace(b, '@', '#')


    # count height
    print(len([l for l in b if l not in [EMPTY, BOTTOM]]))
    # print_board(b)

