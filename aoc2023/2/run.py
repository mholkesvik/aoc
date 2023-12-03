#! /usr/bin/python3


def process_line(l):
    # print(f"Processing line: {l}")
    line_data = []
    l = l.split(":")[1].strip()
    for draw in l.split("; "):
        draw_data = {}
        for color in draw.split(", "):
            num, color_type = color.split(" ")
            draw_data[color_type] = int(num)
        line_data.append(draw_data)

    # print(f"Line data: {line_data}")
    return line_data


# MAX = {
#     "red": 12,
#     "green": 13,
#     "blue": 14,
# }

# with open("input.txt", "r") as f:
#     lines = [l.strip() for l in f.readlines()]
#     sum = 0
#     for i, l in enumerate(lines):
#         is_possible = True
#         draws = process_line(l)
#         for draw in draws:
#             for color, num in draw.items():
#                 if int(num) > MAX[color]:
#                     print(
#                         f"Line {i+1} is impossible because we drew {num} {color} balls"
#                     )
#                     is_possible = False
#                     break

#         if is_possible:
#             sum += i + 1
#             print(f"OK! sum is now {sum}")

#     print(f"Sum: {sum}")

from functools import reduce
import operator

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    sum = 0
    for l in lines:
        draws = process_line(l)
        all_keys = set().union(*draws)
        max_draws = {key: max(d.get(key, 0) for d in draws) for key in all_keys}
        sum += reduce(operator.mul, max_draws.values())

    print(sum)
