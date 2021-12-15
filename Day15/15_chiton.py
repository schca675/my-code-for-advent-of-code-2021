import copy
import time


def get_puzzle_input(filepath):
    field = []
    with open(filepath) as f:
        for line in f:
            l = [int(x) for x in line.rstrip()]
            field.append(l)
    return field


def grow_path(field, paths):
    final_paths = []
    for path in paths:
        # For shortest risk from up left to down right: only move down or right
        # Move down: i+1
        # Move right: j+1
        last_pos = path[-1]
        to_check = [(last_pos[0] + 1, last_pos[1]),(last_pos[0], last_pos[1] + 1)]

        # create a new path for every possible new path:
        new_paths = []
        for pos in to_check:
            ## check whether it is still in the field
            if pos[0] < len(field) and pos[1] < len(field[0]):
                if pos[0] == len(field) -1 and pos[1] == len(field[0])-1:
                    ## so POS is the end --> go there
                    path.append(pos)
                    final_paths.append(path)
                else:
                    # call same function til the end is found
                    new_path = copy.deepcopy(path)
                    new_path.append(pos)
                    new_paths.append(new_path)
        final_paths.extend(grow_path(field, new_paths))
    return final_paths


def get_risk_level(path, field):
    return sum([[field[x][y]] for (x,y) in path])

def resolve_puzzle_part1(filepath):
    field = get_puzzle_input(filepath)
    all_paths = grow_path(field, [[(0,0)]]) # start with one path [(0,0)]: starting at the start namely 0,0
    risk_levels = [get_risk_level(path) for path in all_paths]
    min_risk = min(risk_levels)
    print("PUZZLE SOLUTION: Minimally {} risk level.".format(min_risk))


print("TEST")
start = time.time()
resolve_puzzle_part1("test_data.txt")
print("PUZZLE")
resolve_puzzle_part1("data.txt")
print("Time: {}".format(start - time.time()))

print("TEST")
# resolve_puzzle_part2("test_data.txt")
print("PUZZLE")
# resolve_puzzle_part2("data.txt")