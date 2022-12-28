#! /usr/bin/python3

from collections import defaultdict
import copy

from sympy import symbols, Eq, solve
from sympy.parsing.sympy_parser import parse_expr


name_to_cmd = {}

def expand_eq(start):
    eq = [start]
    updated = True
    while updated:
        updated = False
        new_eq = []
        for w in eq:
            if w != 'humn' and w in name_to_cmd:
                updated = True
                if isinstance(w, int):
                    new_eq.append(w)
                else:
                    if isinstance(name_to_cmd[w], int):
                        new_eq.append(name_to_cmd[w])
                    else:
                        new_eq.append('(')
                        new_eq += name_to_cmd[w]
                        new_eq.append(')')
            else:
                new_eq.append(w)
        eq = new_eq

    eq = [str(c) for c in eq]
    return ' '.join(eq)


def shout(name):
    assert name in name_to_cmd, f'Missing monkey {name}'

    cmd = name_to_cmd[name]
    if isinstance(cmd, int):
        return cmd

    if cmd[1] == '+':
        return int(shout(cmd[0]) + shout(cmd[2]))
    if cmd[1] == '-':
        return int(shout(cmd[0]) - shout(cmd[2]))
    if cmd[1] == '*':
        return int(shout(cmd[0]) * shout(cmd[2]))
    if cmd[1] == '/':
        return int(shout(cmd[0]) / shout(cmd[2]))


with open('input.txt', encoding="utf8") as f:
    # parse inputs
    for name, cmd in [m.split(': ') for m in f.read().split('\n')]:
        cmd = cmd.strip()
        cmd = int(cmd) if cmd.isdigit() else cmd
        cmd = cmd.split(' ') if isinstance(cmd, str) else cmd
        name_to_cmd[name] = cmd

    # Part 1
    print(f'Part 1: {shout("root")}')

    # Part 2
    left, __, right = name_to_cmd['root']
    left = expand_eq(left)
    right = expand_eq(right)

    sympy_humn = symbols('humn')
    if 'humn' in left:
        right = eval(right)
        sympy_left = parse_expr(left)
        eq_solver = Eq(sympy_left, right)
    elif 'humn' in right:
        left = eval(left)
        sympy_right = parse_expr(right)
        eq_solver = Eq(sympy_right, left)

    print(f'Part 2: {int(solve(eq_solver)[0])}')
