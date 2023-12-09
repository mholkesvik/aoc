#! /usr/bin/python3


def next_value(line):
    # base case, if all items in line are 0, return 0
    if all([i == 0 for i in line]):
        return 0

    # recurse with array of difference values
    next_line = [(line[i + 1] - line[i]) for i in range(len(line) - 1)]

    return line[-1] + next_value(next_line)


def parse_line(line):
    return [int(i) for i in line.strip().split(" ")]


# part 1
with open("input.txt", "r") as f:
    lines = [parse_line(line) for line in f.readlines()]
    sum_next_vals = sum([next_value(line) for line in lines])
    print(sum_next_vals)

# part 2
with open("input.txt", "r") as f:
    lines = [parse_line(line) for line in f.readlines()]
    sum_pre_vals = sum([next_value(line[::-1]) for line in lines])
    print(sum_pre_vals)
