#! /usr/bin/python3

DECRYPT_KEY = 811589153
ROUNDS = 10


def print_state():
    assert len(original_idx_to_cur_index) == len(set(original_idx_to_cur_index.values())), \
        'Locations doubled up!'
    state = []
    for pos in range(0, len(original_idx_to_cur_index)):
        for i, j in original_idx_to_cur_index.items():
            if j == pos:
                state.append(original_idx_to_value[i])
    print(state)


with open('input.txt', 'r', encoding="utf8") as f:
    original_idx_to_cur_index = {}
    original_idx_to_value = {}
    original_zero_index = None

    # read in initial values
    for i, n in enumerate(f.readlines()):
        original_idx_to_cur_index[i] = i
        original_idx_to_value[i] = int(n) * DECRYPT_KEY
        if int(n) == 0:
            original_zero_index = i

    size = len(original_idx_to_cur_index) - 1

    for r in range(0, ROUNDS):
        for original_idx, val in original_idx_to_value.items():
            start_idx = original_idx_to_cur_index[original_idx]
            end_idx = (start_idx + val) % size
            end_idx = end_idx if end_idx != 0 else size
            shift_idxs = [i for i, v in original_idx_to_cur_index.items() \
                        if start_idx > v >= end_idx or start_idx < v <= end_idx]
            shift_dir = -1 if start_idx < end_idx else 1
            for idx in shift_idxs:
                original_idx_to_cur_index[idx] += shift_dir
            original_idx_to_cur_index[original_idx] = end_idx

    # calculate groove
    groove_coords = {}
    cur_zero_idx = original_idx_to_cur_index[original_zero_index]
    for i in [1000, 2000, 3000]:
        grove_idx = (cur_zero_idx + i) % len(original_idx_to_cur_index)
        grove_idx_orig = [orig for orig, cur in original_idx_to_cur_index.items() if cur == grove_idx]
        assert len(grove_idx_orig) == 1, 'Can only have 1'
        grove_idx_orig = grove_idx_orig[0]
        groove_coords[i] = original_idx_to_value[grove_idx_orig]

    print(groove_coords)
    print(sum(groove_coords.values()))