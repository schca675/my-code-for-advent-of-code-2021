# --- Day 13: Transparent Origami ---

def fold(dots, fold_axis, fold_index ):
    new_dots = set()
    # fold dots
    if fold_axis == 'y':
        for dot in dots:
            diff = abs(dot[1] - fold_index)
            new_dots.add((dot[0], fold_index - diff))  # - diff since we fold up
    else:
        # it is axis = x
        for dot in dots:
            diff = abs(dot[0] - fold_index)
            new_dots.add((fold_index - diff, dot[1]))  # - diff since we fold left
    return new_dots

def do_origami(dots, instructions):
    new_dots = dots
    for instruction in instructions:
        # instruction of form (x, 2) for x=2 or (y, 7) for y=7
        new_dots = fold(new_dots, instruction[0], instruction[1])
    return new_dots


def get_puzzle_input(filepath):
    dots = set()
    instructions = []
    with open(filepath) as f:
        for line in f:
            if ',' in line:
                # it is a dot:
                parts = line.rstrip().split(',')
                dots.add((int(parts[0]), int(parts[1])))
            elif "fold" in line:
                # it is instruction
                parts = line.rstrip().split('=')
                # example string: "fold along x=5", so we retrieve 5 and x
                instructions.append((parts[0][-1], int(parts[1])))
    return dots, instructions


def resolve_puzzle(filepath, only_first):
    dots, instructions = get_puzzle_input(filepath)
    if only_first:
        res_points = do_origami(dots, instructions[:1])
        print("PUZZLE SOLUTION: {} points after first fold".format(len(res_points)))
    else:
        res_points = do_origami(dots, instructions)

    # Draw grid
    sorted_dots = sorted(res_points,key=lambda x: (x[1], x[0]))
    grid_string = ""
    last_y = 0
    last_x = -1
    for point in sorted_dots:
        # check if point starts a new y-line
        if point[1] > last_y:
            grid_string += "\n"
            # reset x axis
            last_x = -1

        # add dots til the x index of the point is hit
        grid_string += ' '*(point[0] - last_x -1)
        # add # character to mark this point, should now be correct index
        grid_string += '#'
        # update metrics
        last_y = point[1]
        last_x = point[0]

    print(grid_string)


print("TEST")
resolve_puzzle("test_data.txt", False)
print("PUZZLE")
resolve_puzzle("data.txt", False)
