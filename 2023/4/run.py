#! /usr/bin/python3


def parse_line(line):
    """
    input: str e.g. "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"

    output: tuple of two lists of ints
        e.g. [[41, 48, 83, 86, 17], [83, 86, 6, 31, 17, 9, 48, 53]]
    """
    line = line.strip()
    winning_nums, my_nums = line.split(": ")[1].split(" | ")
    winning_nums = [int(n) for n in winning_nums.split(" ") if n]
    my_nums = [int(n) for n in my_nums.split(" ") if n]
    return (winning_nums, my_nums)


# part 2
with open("input.txt", "r") as f:
    lines = [parse_line(l) for l in f.readlines()]

    # find count of winning numbers for each card
    card_scores = {}
    for i, (winning_nums, my_nums) in enumerate(lines):
        card_scores[i + 1] = sum([my_nums.count(n) for n in winning_nums])

    # tally up how many cards you won
    card_tally = {i: 1 for i in range(1, len(lines) + 1)}
    for card in card_tally.keys():
        for card_to_add in range(card, card + card_scores[card] + 1):
            if card_to_add != card and card_to_add in card_tally.keys():
                card_tally[card_to_add] += card_tally[card]

    print(f"Total score part 2: {sum(card_tally.values())}")


# part 1
with open("input.txt", "r") as f:
    lines = [parse_line(l) for l in f.readlines()]

    sum_score = 0
    for i, (winning_nums, my_nums) in enumerate(lines):
        win_count = sum([my_nums.count(n) for n in winning_nums])
        win_score = 0 if win_count == 0 else 2 ** (win_count - 1)
        sum_score += win_score

    print(f"Total score part 1: {sum_score}")
