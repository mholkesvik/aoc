#! /usr/bin/python3

WORD_TO_NUM = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

REVERSE_WORD_TO_NUM = {
    "eno": 1,
    "owt": 2,
    "eerht": 3,
    "ruof": 4,
    "evif": 5,
    "xis": 6,
    "neves": 7,
    "thgie": 8,
    "enin": 9,
}


def get_first_num(s, replace_dict=WORD_TO_NUM):
    w_index = {}
    for w in replace_dict.keys():
        w_index[w] = s.find(w)

    # replace first numeric substring
    w_index = {k: v for k, v in w_index.items() if v != -1}
    if len(w_index) > 0:
        w = min(w_index, key=w_index.get)
        s = s.replace(w, str(replace_dict[w]), 1)

    for c in s:
        if c.isdigit():
            return c


with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

    first_nums = [get_first_num(l) for l in lines]
    last_nums = [get_first_num(l[::-1], REVERSE_WORD_TO_NUM) for l in lines]
    print(sum([int(a + b) for (a, b) in zip(first_nums, last_nums)]))
