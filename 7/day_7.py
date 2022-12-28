#! /usr/bin/python3

from pathlib import Path
from functools import reduce

PART_1_SIZE_MAX = 100000
PART_2_TOTAL_SPACE = 70000000
PART_2_UNUSED_MIN = 30000000


def sum_dicts(dict_a, dict_b):
  return {k: dict_a.get(k, 0) + dict_b.get(k, 0) for k in set(dict_a) | set(dict_b)}


# generate full list of files and sizes
files = {}
with open('input.txt') as f:
    pwd = Path('/')  # start at root
    cmds = [c for c in f.read().split('$ ') if c]
    for cmd in cmds:
      if cmd.startswith('cd '):
        cd_arg = cmd.split(' ')[-1].strip()
        if cd_arg == '/':
          pwd = Path('/')
        elif cd_arg == '..':
          pwd = pwd.parent
        else:
          pwd = pwd / cd_arg
      elif cmd.startswith('ls'):
        dir_files = [str(f) for f in cmd.split('\n')[1:] if not f.startswith('dir ') and f]
        for filepath in dir_files:
          size, fn = filepath.split(' ')
          size = int(size)
          files[pwd / fn] = int(size)
      else:
        raise Exception(f'Unknown cmd {cmd}')

    # group into dir size sums
    dirs = reduce(
        sum_dicts,
        [{str(p): s for p in f.parents} for f, s in files.items()],
        {})
    print(f'Part 1: {sum([v for v in dirs.values() if v <= PART_1_SIZE_MAX])}')

    # Part 2
    free_space = PART_2_TOTAL_SPACE - dirs['/']
    delete_min = PART_2_UNUSED_MIN - free_space
    options = {k:v for (k,v) in dirs.items() if v > delete_min}
    min_option = min(options.items(), key=lambda x: x[1])
    print(f'Part 2: {min_option[1]}')