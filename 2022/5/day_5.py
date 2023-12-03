#! /usr/bin/python3

def parse_stacks(stacks):
  # rotate
  stacks = list(zip(*stacks[::-1]))  # https://stackoverflow.com/a/8421412

  # clean
  stacks = [list(r[1:]) for r in stacks if r[0].isdigit()]
  stacks = [[e for e in s if e != ' '] for s in stacks]

  return stacks


with open("input.txt", "r") as f:
    stacks, moves = f.read().split('\n\n')
    stacks = parse_stacks(stacks.split('\n'))

    for m in moves.split('\n'):
      _, q, _, from_col, _, to_col = m.split(' ')
      q, from_col, to_col = int(q), int(from_col), int(to_col)
      # stacks[to_col - 1] += stacks[from_col - 1][-q:][::-1] # part 1
      stacks[to_col - 1] += stacks[from_col - 1][-q:] # part 2
      del stacks[from_col - 1][-q:]

    print(''.join([s.pop() for s in stacks]))