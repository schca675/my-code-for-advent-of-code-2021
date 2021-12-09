# --- Day 9: Smoke Basin ---


import numpy as np


def get_puzzle_input(filepath):
    field = []
    with open(filepath) as f:
        for line in f:
            l = [int(x) for x in line.rstrip()]
            field.append(l)
    return field


def is_lower_field(i, j, field):
    # assert len(field) >= 1
    if field[i][j] == 9:
        # height 9 are never part of any bassin
        return False
    # lower than right? yes, continue; no -> return False
    if i+1 < len(field):
        if field[i][j] > field[i+1][j]:
            return False
    # lower than left
    if i-1 >= 0:
        if field[i][j] > field[i-1][j]:
            return False
    # lower than upper
    if j-1 >= 0:
        if field[i][j] > field[i][j-1]:
            return False
    # lower than lower
    if j+1 < len(field[0]):
        if field[i][j] > field[i][j+1]:
            return False
    return True

def is_lower_field_bassin(i, j, field, already_in_bassin):
    # assert len(field) >= 1
    # v = field[i][j]
    # Check: is valid? (valid index, not already in the bassin)
    # lower than right? yes, continue; no -> return False
    if field[i][j] == 9:
        # height 9 are never part of any bassin
        return False
    if i+1 < len(field) and (i+1, j) not in already_in_bassin:
        if field[i][j] > field[i+1][j]:
            return False
    # lower than left
    if i-1 >= 0 and (i-1, j) not in already_in_bassin:
        if field[i][j] > field[i-1][j]:
            return False
    # lower than upper
    if j-1 >= 0 and (i, j-1) not in already_in_bassin:
        if field[i][j] > field[i][j-1]:
            return False
    # lower than lower
    if j+1 < len(field[0]) and (i, j+1) not in already_in_bassin:
        if field[i][j] > field[i][j+1]:
            return False
    return True


def get_nines(field):
    indices = set()
    # not very efficient, looop over all elements in field and check
    for i in range(0, len(field)):
        for j in range(0, len(field[0])):
            if field[i][j] == 9:
                indices.add((i,j))
    return indices


def get_lower_fields(field):
    minimals = []
    indices = []
    # not very efficient, looop over all elements in field and check
    for i in range(0, len(field)):
        for j in range(0, len(field[0])):
            if is_lower_field(i, j, field):
                minimals.append(field[i][j])
                indices.append((i,j))
    return minimals, indices

def get_pos_to_check(from_position, in_bassin_already, field):
    ps = set()
    for i in [-1,1]: # up and down if valid: valid index + not already in bassin
        new_i = from_position[0] + i
        if 0 <= new_i < len(field) and (new_i, from_position[1]) not in in_bassin_already:
            ps.add((new_i, from_position[1]))
    for j in [-1,1]: # left and right if valid
        new_j = from_position[1] + j
        if 0 <= new_j < len(field[0]) and (from_position[0], new_j) not in in_bassin_already:
            ps.add((from_position[0], new_j))
    return ps

def grow_bassin(field, from_position, in_bassin_already):
    to_check = get_pos_to_check(from_position, in_bassin_already, field)
    # for every potential new place in the bassin check whether it is a lower field:
    for pos in to_check:
        if pos == (83, 44):
            pass
        ## check whether it is a lower field: ignore elements that are already in bassin, they could be lower
        if is_lower_field_bassin(pos[0], pos[1], field, in_bassin_already):
            in_bassin_already.add(pos) # add position to the bassin
            in_bassin_already = grow_bassin(field, pos, in_bassin_already) # add positions to the bassin attached to this position
    # return all elements found to belong to bassin.
    return in_bassin_already


def get_bassins(field, potential_starts):
    bassins = []
    # potential starts are lower fields
    for pos in potential_starts:
        bassin = grow_bassin(field, pos, {pos})
        bassins.append(bassin)

    return bassins

def resolve_puzzle_part1(filepath):
    field = get_puzzle_input(filepath)
    lower_fields, _ = get_lower_fields(field)
    risk_levels = [1 + height for height in lower_fields]
    print("PUZZLE SOLUTION: {} total risk level, {} total fields".format(sum(risk_levels), len(lower_fields)))


def resolve_puzzle_part2(filepath):
    field = get_puzzle_input(filepath)
    _, lower_fields_indices = get_lower_fields(field)
    bassins = get_bassins(field, lower_fields_indices)
    bassin_sizes = [len(bassin) for bassin in bassins]
    bassin_sizes.sort(reverse=True)
    print("PUZZLE SOLUTION: Largest bassins of size {}, {}, {} \n "
          "{} total product".format(bassin_sizes[0], bassin_sizes[1], bassin_sizes[2], np.prod(bassin_sizes[0:3])))
    nines = get_nines(field)
    bassin_count = sum(bassin_sizes)
    print("nines {}, bassins {}, total field {}x{} so {}".format(len(nines), bassin_count, len(field),
                                                                 len(field[0]), len(field)* len(field[0])))
    ## which ones are not in a bassin:
    all_indices_counted = nines
    for bassin in bassins:
        all_indices_counted  = all_indices_counted.union(bassin)
    not_in_bassin = set()
    for i in range(0, len(field)):
        for j in range(0, len(field[0])):
            if (i,j) not in all_indices_counted:
                not_in_bassin.add((i,j))
    print(not_in_bassin)
    # print field
    str_field = []
    for i in range(0, len(field)):
        str_field.append(["|{}:{:3d}".format(x, 0) if x != 9 else "|{}:{:3d}".format(x, 9) for x in field[i]])
    i = 10
    for bassin in bassins:
        for pos in bassin:
            str_field[pos[0]][pos[1]] = "|{}:{:3d}".format(field[pos[0]][pos[1]], i)
        i+=1
    for line in str_field:
        print("".join(line))
print("TEST")
# resolve_puzzle_part1("test_data.txt")
print("PUZZLE")
resolve_puzzle_part1("data.txt")

print("TEST")
# resolve_puzzle_part2("test_data.txt")
print("PUZZLE")
resolve_puzzle_part2("data.txt")