import pprint
import copy

def get_next_el(s):
    """"
    returns (el, rest) tuple, e.g. [1,2,3] --> (1, [2,3])
    """
    if len(s) < 1 or s == '[]':
        return None

    assert s[0] == '[', "Assume first char is left"

    is_list = (s[1] == '[')

    if not is_list:
        s = s.split(',')
        if len(s) == 1:
            return (s[0][1:-1], '[]')
        return_str = s[0][1:]
        rest = '[' + ','.join(s[1:])
        return (return_str, rest)

    if is_list:
        left_count = 0
        right_count = 0
        for i, c in enumerate(s[1:]):
            if c == '[':
                left_count += 1
            if c == ']':
                right_count += 1
            if right_count == left_count:
                return_str = s[1:i+2]
                rest = s[i+2:] if s[i+2] != ',' else s[i+3:]
                rest = '[' + rest
                return (return_str, rest)

    assert False, 'Bad String!'


def parse_to_list(s):
    if s.isdigit():
        return int(s)

    if s == '[]':
        return []

    parsed_list = []
    while next_el := get_next_el(s):
        next_el, s = next_el
        parsed_list.append(parse_to_list(next_el))

    return parsed_list


def is_valid(l, r, print_level):
    # print((' ' * print_level) + f'Compare {l} vs. {r}')
    if isinstance(l, int) and isinstance(r, int):
        # print((' ' * print_level) + f'{l} and {r} are BOTH ints')
        if l < r:
            # print(f'Left {l} is smaller than {r}, returning True')
            return True
        if l > r:
            # print(f'Left {l} is bigger than {r}, returning False')
            return False
        if l == r:
            return None
        print('DANGER')

    if isinstance(l, int):
        l = [l]

    if isinstance(r, int):
        r = [r]

    while len(r)>0 and len(l)>0:
        r_el = r.pop(0)
        l_el = l.pop(0)
        result = is_valid(l_el, r_el, print_level + 1)
        if result is not None:
            return result

    if len(l) > 0:
        # print('Right ran out first, returning FALSE')
        return False
    if len(r) > 0:
        # print('Left ran out first, returning True')
        return True

    return None


def run():
    with open('input.txt') as f:

        tests = {
            '': None,
            '[]': None,
            '[3]': ('3', '[]'),
            '[[[4,3]]]': ('[[4,3]]', '[]'),
            '[[42]]': ('[42]', '[]'),
            '[1,2,3]': ('1', '[2,3]'),
            '[[1],2,3]': ('[1]', '[2,3]'),
            '[[1,2,3],[4,5]]': ('[1,2,3]','[[4,5]]')
        }
        for test_in, out in tests.items():
            assert get_next_el(test_in) == out, \
                f'Error! Input {test_in} got {get_next_el(test_in)}, expected {out}'

        pairs = [p for p in f.read().split('\n\n') if p]
        valid_pairs = []
        all_lines = [[[2]], [[6]]]
        for i, p in enumerate(pairs):
            l, r = p.split('\n')
            l = parse_to_list(l)
            r = parse_to_list(r)
            all_lines.append(copy.deepcopy(l))
            all_lines.append(copy.deepcopy(r))
            if is_valid(l, r, 0):
                valid_pairs.append(i + 1)

        # Part 2
        # Bubble sort! lol
        for passnum in range(len(all_lines) - 1, 0, -1):
            for i in range(passnum):
                l = copy.deepcopy(all_lines[i])
                r = copy.deepcopy(all_lines[i+1])
                result = is_valid(l, r, 0)
                if result is False:
                    temp = all_lines[i]
                    all_lines[i] = all_lines[i+1]
                    all_lines[i+1] = temp
        decoder_keys = []
        for i, l in enumerate(all_lines, 1):
            if l == [[2]] or l == [[6]]:
                decoder_keys.append(i)
        print(decoder_keys)
        print(decoder_keys[0] * decoder_keys[1])

        # Part 1
        # print(f'Found {len(valid_pairs)} valid pairs: {valid_pairs}')
        # print(f'Sum: {sum(valid_pairs)}')


if __name__ == '__main__':
    run()