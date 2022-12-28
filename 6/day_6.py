#! /usr/bin/python3

INPUT_EXAMPLES = [
  'mjqjpqmgbljsphdztnvjfqwrcgsmlb', # first marker after character 19
  'bvwbjplbgvbhsrlpgdmjqwftvncz', # first marker after character 23
  'nppdvjthqldpwncqszvftbrmjlhg', # first marker after character 23
  'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', # first marker after character 29
  'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', # first marker after character 26
]

PART_1_CHUNKSIZE = 4
PART_2_CHUNKSIZE = 14

with open("input.txt", "r") as f:
    lines = f.read()
    for i in range(0, len(lines)):
      substr = lines[i:i+PART_2_CHUNKSIZE]
      if len(set(substr)) == PART_2_CHUNKSIZE:
        print(f'found signal {substr} at {i+PART_2_CHUNKSIZE} position')
        break
