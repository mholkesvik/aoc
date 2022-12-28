#! /usr/bin/python3

PAYOUTS_PART_1 = {
  # X or A: Rock
  # Y or B: Paper
  # Z or C: Scissors
  'A': {'X': 3 + 1, 'Y': 6 + 2, 'Z': 0 + 3},
  'B': {'X': 0 + 1, 'Y': 3 + 2, 'Z': 6 + 3},
  'C': {'X': 6 + 1, 'Y': 0 + 2, 'Z': 3 + 3}
}


PAYOUTS_PART_2 = {
  # A: Rock
  # B: Paper
  # C: Scissors
  # X: Lose
  # Y: Draw
  # Z: Win
  'A': {'X': 0 + 3, 'Y': 3 + 1, 'Z': 6 + 2},
  'B': {'X': 0 + 1, 'Y': 3 + 2, 'Z': 6 + 3},
  'C': {'X': 0 + 2, 'Y': 3 + 3, 'Z': 6 + 1}
}


def my_score(round_string):
  opp_move, col_2 = round_string.split(' ')
  return PAYOUTS_PART_2[opp_move][col_2]


with open("input.txt", "r") as f:
    rounds = f.read().split('\n')

    my_total_score = 0
    for r in rounds:
      my_round_score = my_score(r)
      # print(f'{r}: {my_round_score}')
      my_total_score += my_round_score

    print(f'TOTAL: {my_total_score}')