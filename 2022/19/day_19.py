#! /usr/bin/python3

import pprint
import heapq
from collections import namedtuple

pp = pprint.PrettyPrinter(indent=4)

Inventory = namedtuple('Inventory',
    [
        'ore', 'clay', 'obs', 'geod',
        'ore_robots', 'clay_robots', 'obs_robots', 'geod_robots'
    ])

# start with 1 ore robot
START_INVENTORY = Inventory(
    0, 0, 0, 0,
    1, 0, 0, 0)

START_MINS = 24


def sucessor(bp, inv, mins_left):

    for robot_type in ['geod', 'obs', 'clay', 'ore']:
        # yield each next robot build decision
        ore, clay, obs, geod, \
            ore_robots, clay_robots, obs_robots, geod_robots = inv

        suc_mins_left = mins_left

        if robot_type == 'geod' and inv.obs_robots > 0: # you start with ore robot
            while ore < bp['geod_cost_ore'] or obs < bp['geod_cost_obs']:
                suc_mins_left -= 1
                ore += ore_robots
                obs += obs_robots
                clay += clay_robots
                geod += geod_robots
                if suc_mins_left == 0:
                    yield (Inventory(
                        ore, clay, obs, geod,
                        ore_robots, clay_robots, obs_robots, geod_robots
                    ), suc_mins_left)
            ore -= bp['geod_cost_ore']
            obs -= bp['geod_cost_obs']
            geod_robots += 1
            if suc_mins_left > 0:
                yield (Inventory(
                    ore, clay, obs, geod,
                    ore_robots, clay_robots, obs_robots, geod_robots
                ), suc_mins_left)
        elif robot_type == 'obs' and inv.clay_robots > 0: # you start with ore robot
            while ore < bp['obs_cost_ore'] or clay < bp['obs_cost_clay']:
                suc_mins_left -= 1
                ore += ore_robots
                obs += obs_robots
                clay += clay_robots
                geod += geod_robots
                if suc_mins_left == 0:
                    yield (Inventory(
                        ore, clay, obs, geod,
                        ore_robots, clay_robots, obs_robots, geod_robots
                    ), suc_mins_left)
            ore -= bp['obs_cost_ore']
            clay -= bp['obs_cost_clay']
            clay_robots += 1
            if suc_mins_left > 0:
                yield (Inventory(
                    ore, clay, obs, geod,
                    ore_robots, clay_robots, obs_robots, geod_robots
                ), suc_mins_left)
        elif robot_type == 'clay':
            while ore < bp['clay_cost']:
                suc_mins_left -= 1
                ore += ore_robots
                obs += obs_robots
                clay += clay_robots
                geod += geod_robots
                if suc_mins_left == 0:
                    yield (Inventory(
                        ore, clay, obs, geod,
                        ore_robots, clay_robots, obs_robots, geod_robots
                    ), suc_mins_left)
            ore -= bp['clay_cost']
            clay_robots += 1
            if suc_mins_left > 0:
                yield (Inventory(
                    ore, clay, obs, geod,
                    ore_robots, clay_robots, obs_robots, geod_robots
                ), suc_mins_left)
        elif robot_type == 'ore':
            while ore < bp['ore_cost']:
                suc_mins_left -= 1
                ore += ore_robots
                obs += obs_robots
                clay += clay_robots
                geod += geod_robots
                if suc_mins_left == 0:
                    yield (Inventory(
                        ore, clay, obs, geod,
                        ore_robots, clay_robots, obs_robots, geod_robots
                    ), suc_mins_left)
            ore -= bp['ore_cost']
            ore_robots += 1
            if suc_mins_left > 0:
                yield (Inventory(
                    ore, clay, obs, geod,
                    ore_robots, clay_robots, obs_robots, geod_robots
                ), suc_mins_left)



def heuristic(inv, mins_left):
    score = (1_000 * inv.geod) + (inv.geod_robots * mins_left * 1_000) + \
        (inv.obs_robots * mins_left * 100) + \
        (inv.clay_robots * mins_left * 10) + \
        (inv.ore_robots * mins_left)

    return -1 * score


with open('input_example.txt', 'r', encoding="utf8") as f:
    blue_prints = []
    for l in f.read().split('\n'):
        words = l.split(' ')
        blue_prints.append({
            'id': int(words[1][:-1]),
            'ore_cost': int(words[6]),
            'clay_cost': int(words[12]),
            'obs_cost_ore': int(words[18]),
            'obs_cost_clay': int(words[21]),
            'geod_cost_ore': int(words[27]),
            'geod_cost_obs': int(words[30])
        })

    bp = blue_prints[0]
    frontier = []
    heapq.heappush(frontier,
        (heuristic(START_INVENTORY, START_MINS), (START_INVENTORY, START_MINS)))

    max_geod_so_far = 0
    while len(frontier) > 0:
        heur_score, (inv, mins_left) = heapq.heappop(frontier)
        # print(heur_score, mins_left, inv)
        if mins_left == 0:
            max_geod_so_far = max(max_geod_so_far, inv.geod)
            print(max_geod_so_far)
            continue

        for next_state in sucessor(bp, inv, mins_left):
            heapq.heappush(frontier, (heuristic(*next_state), next_state))

    print(max_geod_so_far)

    # assert bp_max(blue_prints[0], 24, START_INVENTORY) == 9, "wrong answer on example 1"
    # assert bp_max(blue_prints[1], 24, START_INVENTORY) == 12, "wrong answer on example 2"

    # TEST_BP = {
    #     'id': 999,
    #     'ore_cost': 1,
    #     'clay_cost': 1,
    #     'obs_cost_ore': 1,
    #     'obs_cost_clay': 1,
    #     'geod_cost_ore': 1,
    #     'geod_cost_obs': 1
    # }
    # TEST_INV = Inventory(
    #     1,1,1,1,
    #     1,1,1,1
    # )
    # print(list(sucessor(TEST_BP ,TEST_INV)))