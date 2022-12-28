#! /usr/bin/python3
import math

DECODE = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}

ENCODE = {
    4: "2",
    3: "1",
    2: "0",
    1: "-",
    0: "="
}

def snafu_to_dec(snafu):
    total_sum = 0
    for place, c in enumerate(snafu[::-1], 0):
        place = math.pow(5, place)
        c = DECODE[c]
        total_sum += (c * place)

    return int(total_sum)


def dec_to_snafu(dec):
    return_str = ""
    while dec > 0:
        q, r = divmod(dec+2, 5)
        return_str = ENCODE[r] + return_str
        dec = q

    return return_str


with open('input.txt', encoding="utf8") as f:
    sum_dec = 0
    for line in f.read().split('\n'):
        sum_dec += snafu_to_dec(line)

    print(dec_to_snafu(sum_dec))


# TESTS
# assert 1 ==  snafu_to_dec("1"), "incorrect"
# assert 2 ==  snafu_to_dec("2"), "incorrect"
# assert 3 ==  snafu_to_dec("1="), "incorrect"
# assert 4 ==  snafu_to_dec("1-"), "incorrect"
# assert 5 ==  snafu_to_dec("10"), "incorrect"
# assert 6 ==  snafu_to_dec("11"), "incorrect"
# assert 7 ==  snafu_to_dec("12"), "incorrect"
# assert 8 ==  snafu_to_dec("2="), "incorrect"
# assert 9 ==  snafu_to_dec("2-"), "incorrect"
# assert 10 ==  snafu_to_dec("20"), "incorrect"
# assert 15 ==  snafu_to_dec("1=0"), "incorrect"
# assert 20 ==  snafu_to_dec("1-0"), "incorrect"
# assert 2022 ==  snafu_to_dec("1=11-2"), "incorrect"
# assert 12345 ==  snafu_to_dec("1-0---0"), "incorrect"
# assert 314159265 ==  snafu_to_dec("1121-1110-1=0"), "incorrect"
# assert "2=-1=0" == dec_to_snafu(4890), "incorrect"
# assert "1121-1110-1=0" ==  dec_to_snafu(snafu_to_dec("1121-1110-1=0")), "incorrect"
