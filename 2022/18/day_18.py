#! /usr/bin/python3

def cube_to_neighbors(c):
    if min_dim:
        if c[2] != min_dim[2]:
            yield (c[0], c[1], c[2]-1)
        if c[2] != max_dim[2]:
            yield (c[0], c[1], c[2]+1)
        if c[1] != min_dim[1]:
            yield (c[0], c[1]-1, c[2])
        if c[1] != max_dim[1]:
            yield (c[0], c[1]+1, c[2])
        if c[0] != min_dim[0]:
            yield (c[0]-1, c[1], c[2])
        if c[0] != max_dim[0]:
            yield (c[0]+1, c[1], c[2])

cubes = set()
with open('input.txt', 'r', encoding="utf8") as f:
    lines = [[int(i) for i in c.split(',')] for c in f.read().split('\n')]

    for l in lines:
        cubes.add(tuple(l))

min_x = min([c[0] for c in cubes]) - 1
min_y = min([c[1] for c in cubes]) - 1
min_z = min([c[2] for c in cubes]) - 1
max_x = max([c[0] for c in cubes]) + 1
max_y = max([c[1] for c in cubes]) + 1
max_z = max([c[2] for c in cubes]) + 1

min_dim = (min_x, min_y, min_z)
max_dim = (max_x, max_y, max_z)


# Part 1
total_surface_part_one = 0
for c in cubes:
    cube_surface = 6
    for neighbor_cube in cube_to_neighbors(c):
        if neighbor_cube in cubes:
            cube_surface -= 1

    total_surface_part_one += cube_surface

print(total_surface_part_one)

# Part 2
# first, get all the outside cubes
outside_cubes = set()
frontier = [(min_x, min_y, min_z)]
while len(frontier) > 0:
    cube = frontier.pop()
    if cube not in cubes and cube not in outside_cubes:
        outside_cubes.add(cube)
        for next_cube in cube_to_neighbors(cube):
            frontier.append(next_cube)

total_surface_part_two = 0
for c in cubes:
    cube_surface = 6
    for neighbor_cube in cube_to_neighbors(c):
        if (neighbor_cube in cubes) or (neighbor_cube not in outside_cubes):
            total_surface_part_two -= 1

    total_surface_part_two += cube_surface

print(total_surface_part_two)
