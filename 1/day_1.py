#! /usr/bin/python3

from itertools import groupby


with open("input.txt", "r") as f:
    lines = [l for l in f.readlines()]
    elf_chunks = [list(group) for key, group in groupby(lines, key=lambda x: x == '\n') if not key]
    elf_sums = [sum([int(i.strip()) for i in l]) for l in elf_chunks]

    # Part 1
    print(max(elf_sums))

    # Part 2
    print(sum(sorted(elf_sums)[-3:]))
