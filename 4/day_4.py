#! /usr/bin/python3

with open("input.txt", "r") as f:
    contains_count = 0
    overlap_count = 0
    pairs = [l.split(',') for l in f.read().split('\n')]
    for elf_1, elf_2 in pairs:
      elf_1_start, elf_1_end = [int(i) for i in elf_1.split('-')]
      elf_2_start, elf_2_end = [int(i) for i in elf_2.split('-')]

      # Part 1
      if elf_1_end >= elf_2_end and elf_1_start <= elf_2_start:
          # print(f"Elf 1 {elf_1} contains Elf 2 {elf_2}")
          contains_count += 1
      elif elf_2_end >= elf_1_end and elf_2_start <= elf_1_start:
          # print(f"Elf 2 ({elf_2}) contains Elf 1 ({elf_1})")
          contains_count += 1

      # Part 2
      if (elf_1_end >= elf_2_start and elf_1_start <= elf_2_end) or (
          elf_2_end >= elf_1_start and elf_2_start <= elf_1_end
      ):
          # print(f"Elf 1 ({elf_1}) and Elf 2 ({elf_2}) overlap")
          overlap_count += 1

    print(f'Contains: {contains_count}')
    print(f'Overlaps: {overlap_count}')