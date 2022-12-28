#! /usr/bin/python3

import numpy as np
from functools import reduce


def view_len(arr, h):
    dist = 0
    for l in arr:
        if h > l:
            dist += 1
        if h <=l:
            dist += 1
            break
    return dist


def is_visible(arr, row, col):
    if row in [0, len(arr[0])-1] or col in [0, len(arr)-1]:
        # Edge tree: visible
        return True

    val = arr[row][col]
    l = arr[row][:col]
    r = arr[row][col+1:]
    u = arr[:row, col]
    d = arr[row+1:, col]
    max_vals = map(max, [l, r, u, d])

    return not all([val <= x for x in max_vals])


def scenic_score(forest_arr, row, col):
    val = forest_arr[row][col]
    l = forest_arr[row][:col][::-1] # reverse for view order
    r = forest_arr[row][col+1:]
    u = forest_arr[:row, col][::-1] # reverse for view order
    d = forest_arr[row+1:, col]

    view_lens = [view_len(view_arr, val) for view_arr in [l, r, u, d]]

    return reduce(lambda x, y: x*y, view_lens)


def apply(arr, func):
    # TODO: gotta be a cleaner way to vectorize here...
    new_arr = np.array(
        [func(arr, ix, iy) for (ix, iy) in np.ndindex(arr.shape)])
    new_arr = new_arr.reshape(arr.shape)
    return new_arr


with open('input.txt') as f:
    input = f.read().strip().split("\n")
    input = [' '.join(w) for w in input]
    input = np.genfromtxt(input)

    # part 1
    is_visible_arr = apply(input, is_visible)
    print(f'Part 1: {np.sum(is_visible_arr)}')

    # part 2
    scenic_arr = apply(input, scenic_score)
    print(f'Part 2: {np.max(scenic_arr)}')
