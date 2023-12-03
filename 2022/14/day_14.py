import math
import numpy as np

START = 2
ROCK = 1
EMPTY = 0
SAND = 4

def get_grid(rock_pts, max_x, min_x, max_y, min_y):
    grid = np.zeros((max_y + 1 - min_y, max_x + 1 - min_x), dtype=int)

    for pt in rock_pts:
        grid[pt[1]-min_y, pt[0]-min_x] = ROCK

    grid[0-min_y, 500-min_x] = START

    return grid


def get_path(p1, p2):
    """
    return full list of (x, y) pairs between p1 and p2 (inclusive)
    e.g. (498,4), (498,6) ==> [(498,4), (498,5), (498,6)]
    """
    assert len(p1) == len(p2) and len(p2) == 2, "Bad pt input"
    assert p1[1] != p2[1] or p1[0] != p2[0], "Error! can't find diaganal paths"

    if p1[0] != p2[0]:
        step = int(math.copysign(1, p2[0] - p1[0]))
        for x in range(p1[0], p2[0] + step, step):
            yield [x, p1[1]]

    if p1[1] != p2[1]:
        step = int(math.copysign(1, p2[1] - p1[1]))
        for y in range(p1[1], p2[1] + step, step):
            yield [p1[0], y]


def is_off_grid(idx, grid):
    if idx[0] >= grid.shape[0] or idx[1] >= grid.shape[1]:
        return True

    if idx[0] < 0 or idx[1] < 0:
        return True

    return False


def is_open(idx, grid):
    val = grid[idx[0]][idx[1]]
    return (val == EMPTY)


def drop_sand(grid):
    init_sand_idx = list(zip(*np.where(grid == START)))[0]
    new_sand_idx = init_sand_idx

    while True:
        # try down
        down_idx = (new_sand_idx[0] + 1, new_sand_idx[1])
        if is_off_grid(down_idx, grid):
            return None
        if is_open(down_idx, grid):
            new_sand_idx = down_idx
            continue

        # try down left
        down_left_idx = (new_sand_idx[0] + 1, new_sand_idx[1] - 1)
        if is_off_grid(down_left_idx, grid):
            return None
        if is_open(down_left_idx, grid):
            new_sand_idx = down_left_idx
            continue

        down_right_idx = (new_sand_idx[0] + 1, new_sand_idx[1] + 1)
        if is_off_grid(down_right_idx, grid):
            return None
        if is_open(down_right_idx, grid):
            new_sand_idx = down_right_idx
            continue

        break

    if new_sand_idx == init_sand_idx:
        return None

    return new_sand_idx


def run():
    with open('input.txt') as f:
        # parse inputs
        input = [l.split(' -> ') for l in f.read().split('\n')]
        input = [[[int(i) for i in t.split(',')] for t in l] for l in input]

        # generate grid with rock pts
        rock_pts = set()
        for line in input:
            for p1, p2 in zip(line, line[1:]):
                for pt in get_path(p1, p2):
                    rock_pts.add(tuple(pt))

        max_x = max(rock_pts, key=lambda x: x[0])[0]
        min_x = min(rock_pts, key=lambda x: x[0])[0]
        max_y = max(rock_pts, key=lambda x: x[1])[1]
        min_y = min(0, min(rock_pts, key=lambda x: x[1])[1])
        grid = get_grid(rock_pts, max_x, min_x, max_y, min_y)

        # Part 2
        grid = np.pad(grid, [(1,2),(50000,50000)], 'minimum')
        grid[len(grid)-1] = ROCK

        # file up with sand
        num_sand_placed = 0
        print('start')
        while ( sand_idx := drop_sand(grid) ) is not None:
            grid[sand_idx[0], sand_idx[1]] = SAND
            num_sand_placed += 1
            print(num_sand_placed)

        print(num_sand_placed + 1)


if __name__ == '__main__':
    run()