import math


def handle_move_part_1(move, h_loc, t_loc, visited):
    # move head
    if move == 'R':
        h_loc = (h_loc[0] + 1, h_loc[1])
    elif move == 'L':
        h_loc = (h_loc[0] - 1, h_loc[1])
    elif move == 'U':
        h_loc = (h_loc[0], h_loc[1] + 1)
    elif move == 'D':
        h_loc = (h_loc[0], h_loc[1] - 1)

    # move tail
    if h_loc == t_loc:
        print(f'No tail move, both at {h_loc}')
    else:
        col_diff = h_loc[1] - t_loc[1]
        row_diff = h_loc[0] - t_loc[0]

        if abs(col_diff) + abs(row_diff) == 3:
        # diag special case
        t_loc = (t_loc[0] + math.copysign(1, row_diff),
                t_loc[1] + math.copysign(1, col_diff))
        else:
        col_move = 0 if abs(col_diff) < 2 else (col_diff -
                                                math.copysign(1, col_diff))
        row_move = 0 if abs(row_diff) < 2 else (row_diff -
                                                math.copysign(1, row_diff))
        t_loc = (t_loc[0] + row_move, t_loc[1] + col_move)

    # update visited set
    visited.add(t_loc)

    return (h_loc, t_loc, visited)


def expand_moves(input):
    new_input = []
    for move in input:
        direction, magnitude = move.split(' ')
        magnitude = int(magnitude)
        new_input += [direction] * magnitude
    return new_input


def get_subtail_loc(h_loc, old_t_loc):
    if h_loc == old_t_loc:
        # No tail move, both at same location
        return old_t_loc

    col_diff = h_loc[1] - old_t_loc[1]
    row_diff = h_loc[0] - old_t_loc[0]

    if abs(col_diff) + abs(row_diff) == 3:
        return (old_t_loc[0] + math.copysign(1, row_diff),
                old_t_loc[1] + math.copysign(1, col_diff))

    col_move = 0 if abs(col_diff) < 2 else (col_diff -
                                            math.copysign(1, col_diff))
    row_move = 0 if abs(row_diff) < 2 else (row_diff -
                                            math.copysign(1, row_diff))

    return (old_t_loc[0] + row_move, old_t_loc[1] + col_move)


def handle_move_part_2(locs, visited):

    for i in range(len(locs)):
        h_loc = locs[i]

        if i == (len(locs) - 1):
            # final tail, update visited
            visited.add(h_loc)
            break

        # update sub-tail loc
        locs[i + 1] = get_subtail_loc(h_loc, locs[i + 1])

    return locs, visited


with open('input.txt') as f:
    input = f.read().strip().split("\n")
    print(input)

    # Part 1
    # h_loc, t_loc, visited = (0, 0), (0, 0), set()

    # initialize state
    locs = [(0, 0)] * 10
    visited = set()
    visited.add((0, 0))

    # flatten moves to single steps
    input = expand_moves(input)

    for move in input:
      # part 1
      # h_loc, t_loc, visited = handle_move_part_1(move, h_loc, t_loc, visited)

      # part 2
      # move ultimate head
      if move == 'R':
        locs[0] = (locs[0][0] + 1, locs[0][1])
      elif move == 'L':
        locs[0] = (locs[0][0] - 1, locs[0][1])
      elif move == 'U':
        locs[0] = (locs[0][0], locs[0][1] + 1)
      elif move == 'D':
        locs[0] = (locs[0][0], locs[0][1] - 1)

      # update rest of list
      locs, visited = handle_move_part_2(locs, visited)

    print("-------")
    print(len(visited))
