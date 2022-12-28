#! /usr/bin/python3
import string

def priority(char):
  # ord doesn't word here? :(
  pri_order = string.ascii_lowercase + string.ascii_uppercase
  return pri_order.index(char) + 1


def chunker(seq, size):
  return (seq[pos:pos + size] for pos in range(0, len(seq), size))


sum_pri = 0
with open("input.txt", "r") as f:
    rucks = f.read().split('\n')

    # part 1
    # for r in rucks:
    #   # assuming all even sized rucks
    #   split = int(len(r) / 2)
    #   front, back = set(r[:split]), set(r[split:])
    #   common = front.intersection(back)
    #   sum_pri += priority(common.pop())

    # part 2
    for elf_group in chunker(rucks, 3):
      rucks_unique = set.intersection(*[set(r) for r in elf_group])
      sum_pri += priority(rucks_unique.pop())

    print(sum_pri)
