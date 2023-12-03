import numpy as np
import heapq

MOVES = {
    '∨': (1,0),
    '^': (-1,0),
    '>': (0,1),
    '<': (0,-1)
}


def heuristic(pos, end):
    # cityblock dist to end
    return (abs(pos[0] - end[0]) + abs(pos[1] - end[1]))


def gen_possible_moves(grid, cur_pos):
    cur_height = grid[cur_pos]
    for move_char, lr_ud in MOVES.items():
        lr, ud = lr_ud
        pos_index = ((cur_pos[0] + lr), (cur_pos[1] + ud))
        if pos_index[0] < 0 or pos_index[1] < 0:
            # NO! {pos_index} is off the grid (negative)
            continue
        if pos_index[0] >= grid.shape[0] or pos_index[1] >= grid.shape[1]:
            # NO! {pos_index} is off the grid (overflow)
            continue

        dest_height = ord(grid[pos_index]) if grid[pos_index] != 'E' else ord('z')
        cur_height = ord(grid[cur_pos])
        step_size = dest_height - cur_height
        if step_size > 1:
            # NO! {pos_index} ({grid[pos_index]}) is too high
            continue

        yield (move_char, pos_index)


def run():
    with open('input.txt') as f:
        lines = [' '.join(l) for l in f.read().split('\n') if l]
        grid = np.genfromtxt(lines, dtype=str)
        start = list(zip(*np.where(grid == 'S')))[0]
        end = list(zip(*np.where(grid == 'E')))[0]

        frontier = [] # A* search pri queue
        visited = set()
        distance = dict()
        distance[start] = 0
        came_from = dict()
        heapq.heappush(frontier, (heuristic(start, end), start))

        # Part 2
        additional_starts = list(zip(*np.where(grid == 'a')))
        for a_start_idx in additional_starts:
            heapq.heappush(frontier, (heuristic(a_start_idx, end), a_start_idx))
            distance[a_start_idx] = 0

        while len(frontier) > 0:
            __, node = heapq.heappop(frontier)
            if node in visited:
                continue
            if grid[node] == 'E':
                print('found end!')
                result_path = reconstruct_path(came_from, [start] + additional_starts, node)
                print(len(result_path) - 1)

            visited.add(node)

            for (__, successor) in gen_possible_moves(grid, node):
                heapq.heappush(frontier,
                    (distance[node] + 1 + heuristic(successor, end), successor))

                if (successor not in distance
                    or distance[node] + 1 < distance[successor]):
                    distance[successor] = distance[node] + 1
                    came_from[successor] = node

        return None


def reconstruct_path(came_from, starts, end):
    reverse_path = [end]
    while end not in starts:
        end = came_from[end]
        reverse_path.append(end)
    return list(reversed(reverse_path))


if __name__ == '__main__':
    run()