#! /usr/bin/python3
import sys

v_to_flow = {}
v_to_next = {}
best_so_far = {} # {NODE__TIME: score}

with open('input.txt', 'r', encoding="utf8") as f:
    lines = [l.split(' ') for l in f.read().split('\n')]

    for l in lines:
        valve = l[1]
        flow = int(l[4][:-1].split('=')[1])
        next_valve = [n.replace(',', '').strip() for n in l[9:]]
        v_to_flow[valve] = flow
        v_to_next[valve] = next_valve


# def opt_path_score_part_1(node, time_remaining, total_rate, total_release, path, open_valves):
#     # print(node, time_remaining, total_rate, total_release)

#     if time_remaining == 0:
#         # if total_release > 1730:
#         #     print(open_valves, path)
#         return total_release

#     total_release += total_rate

#     key = f'{node}__{time_remaining}'
#     if key in best_so_far and best_so_far[key] >= total_release:
#         return -1
#     else:
#         best_so_far[key] = total_release


#     stay_and_open = -1
#     if node not in open_valves:
#         stay_and_open = opt_path_score_part_1(
#             node,
#             time_remaining - 1,
#             total_rate + v_to_flow[node],
#             total_release,
#             path,
#             open_valves + [node])

#     return max(
#         stay_and_open,

#         # stay and do nothing
#         opt_path_score_part_1(
#             node,
#             time_remaining - 1,
#             total_rate,
#             total_release,
#             path,
#             open_valves),

#         # follow each pipe
#         max([
#             opt_path_score_part_1(
#                 next_node,
#                 time_remaining - 1,
#                 total_rate,
#                 total_release,
#                 path + [next_node],
#                 open_valves)
#             for next_node in v_to_next[node]
#         ])
#     )

# print(opt_path_score_part_1('AA', 30, 0, 0, ['AA'], []))
MAX_FLOW = 313
def opt_path_score_part_2(my_node, el_node, time_remaining, total_rate,
    total_release, path, open_valves):

    if time_remaining == 0:
        return total_release

    if time_remaining * MAX_FLOW < 2502:
        # NGMI
        return -1

    if total_release > 2500 and total_release % 1000 == 0:
        print(total_release)

    total_release += total_rate

    # trim paths
    # key = f'{my_node}__{el_node}__{time_remaining}'
    # if key in best_so_far and best_so_far[key] >= total_release:
    #     return -1
    # else:
    #     best_so_far[key] = total_release

    my_next_moves = v_to_next[my_node] + ['open']
    el_next_moves = v_to_next[el_node] + ['open']

    best_move_score = -1
    for my_move in my_next_moves:
        for el_move in el_next_moves:
            open_valves_add = []
            rate_add = 0

            if my_move == 'open':
                if v_to_flow[my_node] == 0:
                    continue
                if my_node not in open_valves and my_node not in open_valves_add:
                    open_valves_add += [my_node]
                    rate_add += v_to_flow[my_node]
            if el_move == 'open':
                if v_to_flow[el_node] == 0:
                    continue
                if el_node not in open_valves and el_node not in open_valves_add:
                    open_valves_add += [el_node]
                    rate_add += v_to_flow[el_node]

            best_move_score = max(best_move_score,
                opt_path_score_part_2(
                    my_move if my_move != 'open' else my_node,
                    el_move if el_move != 'open' else el_node,
                    time_remaining - 1,
                    total_rate + rate_add,
                    total_release,
                    path + [(my_move, el_move)],
                    open_valves + open_valves_add)
            )

    return best_move_score

# 2502 is too low, 5k too high
print(opt_path_score_part_2('AA', 'AA', 26, 0, 0, [('AA', 'AA')], []))
