### #### PUZZLE 1 - 02/12/2021 DRIVE!

# Sub marine:
# ^ Depth
# |
# |
# |
# |
# |
# |
# |------------------------> Horizontal position
# 0,0

FORWARD = "forward"
DOWN = "down"
UP = "up"

def forward(pos, depth, amount):
    # forward X increases the horizontal position by X units.
    return pos + amount, depth

def down(pos, depth, amount):
    # down X increases the depth by X units.
    return pos, depth + amount

def up(pos, depth, amount):
    # up X decreases the depth by X units.
    return pos, depth - amount

def drive_submarine(commands, pos, depth):
    for command in commands:
        # command: tuple (forward/down/up, amount)
        if command[0] == FORWARD:
            pos, depth = forward(pos, depth, command[1])
        elif command[0] == UP:
            pos, depth = up(pos, depth, command[1])
        elif command[0] == DOWN:
            pos, depth = down(pos, depth, command[1])
    return pos, depth

def get_list_of_commands_from_txt_file(filepath):
    res = []
    with open(filepath) as f:
        for line in f:
            line_list = line.split()
            res.append([line_list[0], int(line_list[1])])
    return res

def get_puzzle_result(pos, depth):
    return pos*depth

def puzzle_resolution_part_1(filepath):
    commands = get_list_of_commands_from_txt_file(filepath)
    print("Starting position: \\ Position: 0, Depth: 0 ")
    start_pos, start_depth = 0, 0
    final_pos, final_depth = drive_submarine(commands, start_pos, start_depth)
    print("End position: \\ Position {}, Depth: {}".format(final_pos, final_depth))
    print("Solution: ", get_puzzle_result(final_pos, final_depth))


## PUZZLE 2
filepath_test = "2_test_data_commands"
print("2.1 TEST")
puzzle_resolution_part_1(filepath_test)
print("2.1 PUZZLE")
filepath = "2_data_commands"
puzzle_resolution_part_1(filepath)


### Part Two: updated up, down and forward commands, now with aim

def forward_with_aim(pos, depth, aim, amount):
    # forward X increases the horizontal position by X units.
    return pos + amount, depth + (aim * amount), aim


def down_with_aim(pos, depth, aim, amount):
    # down X increases the depth by X units.
    return pos, depth, aim + amount


def up_with_aim(pos, depth, aim, amount):
    # up X decreases the depth by X units.
    return pos, depth, aim - amount


def drive_submarine_with_aim(commands, pos, depth, aim):
    for command in commands:
        # command: tuple (forward/down/up, amount)
        if command[0] == FORWARD:
            pos, depth, aim = forward_with_aim(pos, depth, aim, command[1])
        elif command[0] == UP:
            pos, depth, aim = up_with_aim(pos, depth, aim, command[1])
        elif command[0] == DOWN:
            pos, depth, aim = down_with_aim(pos, depth, aim, command[1])
    return pos, depth, aim


def puzzle_resolution_part_2(filepath):
    commands = get_list_of_commands_from_txt_file(filepath)
    print("Starting position: \\ Position: 0, Depth: 0, Aim: 0 ")
    start_pos, start_depth, start_aim = 0, 0, 0
    final_pos, final_depth, final_aim = drive_submarine_with_aim(commands, start_pos, start_depth, start_aim)
    print("End position: \\ Position {}, Depth: {}, Aim: {}".format(final_pos, final_depth, final_aim))
    print("Solution: ", get_puzzle_result(final_pos, final_depth))

## PUZZLE 2 Part 2
filepath_test = "2_test_data_commands"
print("2.2 TEST")
puzzle_resolution_part_2(filepath_test)
print("2.2 PUZZLE")
filepath = "2_data_commands"
puzzle_resolution_part_2(filepath)
