import sys
import numpy as np
from skimage.morphology import diamond
import z3

DISTRESS_MAX = 4000000
# DISTRESS_MAX = 20

def man_dist(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])

def tuning_freq(pt):
    return (4000000 * pt[0]) + pt[1]

def gen_pts_within_dist(pt, dist):
    for x in range(max(0, pt[0] - dist), min(DISTRESS_MAX, pt[0] + dist + 1)):
        for y in range(max(0, pt[1] - dist), min(DISTRESS_MAX, pt[1] + dist + 1)):
            if not man_dist((x, y), pt) > dist:
                yield (x, y)

def gen_pts_on_edge(pt, dist):
    for x in range(max(0, pt[0] - dist), min(DISTRESS_MAX, pt[0] + dist + 1)):
        for y in range(max(0, pt[1] - dist), min(DISTRESS_MAX, pt[1] + dist + 1)):
            if not man_dist((x, y), pt) > dist:
                yield (x, y)

def run():
    sensor_to_closest_beacon = {}
    with open('input.txt') as f:
        min_x, max_x, min_y, max_y = [
            sys.maxsize, -sys.maxsize, sys.maxsize, -sys.maxsize]
        for line in f.read().split('\n'):
            line = line.replace('=', ' ').replace(':', ' ').replace(',', ' ')
            sx, sy, bx, by = [
                int(c) for c in line.split(' ') if c.lstrip("-").isdigit()]
            min_x = min(min_x, sx, bx)
            min_y = min(min_y, sy, by)
            max_x = max(max_x, sx, bx)
            max_y = max(max_y, sy, by)
            sensor_to_closest_beacon[(sx, sy)] = (bx, by)

    sensor_to_dist = {
        s: man_dist(s, b) for (s, b) in sensor_to_closest_beacon.items()}

    # Part 1
    max_dist = max(sensor_to_dist.values())

    # ROW_NUM = 2000000
    # in_range_count = 0
    # for x in range(min_x - max_dist, max_x + max_dist):
    #     pt = (x, ROW_NUM)

    #     # skip if pt is beacon or sensor
    #     if pt in sensor_to_closest_beacon or pt in sensor_to_closest_beacon.values():
    #         # print(f'{pt} is a beacon or sensor, skipping')
    #         continue

    #     if pt[0] % 10000 == 0: print(pt)
    #     for sensor, sensor_range in sensor_to_dist.items():
    #         if sensor_range >= man_dist(pt, sensor):
    #             # print(f'sensor {sensor} can see: YES')
    #             in_range_count += 1
    #             break

    # Part 2 Solution 1 (skimage.morphology can't make binary diamonds big enough :( )
    # possible_locs = np.zeros((DISTRESS_MAX, DISTRESS_MAX), dtype=bool)
    # print('1')

    # print(len(sensor_to_dist))
    # for s, dist in sensor_to_dist.items():
    #     print(s, dist)

    #     grid_x_start = max(0, (s[0] - dist))
    #     grid_y_start = max(0, (s[1] - dist))
    #     grid_x_end = min(DISTRESS_MAX, s[0] + dist) + 1
    #     grid_y_end = min(DISTRESS_MAX, s[1] + dist) + 1

    #     diamond_x_start = abs(s[0] - dist) if s[0] - dist < 0 else 0
    #     diamond_y_start = abs(s[1] - dist) if s[1] - dist < 0 else 0
    #     diamond_x_end = 2 * dist + 1 if (s[0] + dist) < DISTRESS_MAX else - (s[0] + 1 + dist - DISTRESS_MAX)
    #     diamond_y_end = 2 * dist + 1 if (s[1] + dist) < DISTRESS_MAX else - (s[1] + 1 + dist - DISTRESS_MAX)

    #     grid_window = possible_locs[
    #         grid_y_start:grid_y_end,
    #         grid_x_start:grid_x_end]

    #     diamond_window = diamond(dist, dtype=bool)[
    #         diamond_y_start:diamond_y_end,
    #         diamond_x_start:diamond_x_end]

    #     log_or = np.logical_or(diamond_window, grid_window)

    #     possible_locs[
    #         grid_y_start:grid_y_end,
    #         grid_x_start:grid_x_end] = log_or

    # possible_idx = list(zip(*np.where(possible_locs == False)))


    # Part 2 Solution 2: using z3 solver :)

    solver = z3.Solver()
    x, y = z3.Int("x"), z3.Int("y")
    solver.add(0 <= x); solver.add(x <= 4000000)
    solver.add(0 <= y); solver.add(y <= 4000000)

    def z3_abs(x):
        return z3.If(x >= 0, x, -x)

    for s, b in sensor_to_closest_beacon.items():
        m = abs(s[0] - b[0]) + abs(s[1] - b[1])
        solver.add(z3_abs(s[0] - x) + z3_abs(s[1] - y) > m)

    assert s.check() == z3.sat

    model = s.model()
    print("Part 2:", model[x].as_long() * 4000000 + model[y].as_long())
    # print(possible_idx)
    # y, x = possible_idx[0]
    # print(tuning_freq((x,y)))

if __name__ == '__main__':
    run()