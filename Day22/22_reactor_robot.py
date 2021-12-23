# --- Day 22: Reactor Reboot ---
import numpy


def binary_search(arr, low, high, x):
    # adapted from: https://www.geeksforgeeks.org/python-program-for-binary-search/
    # low, high are indexes
    # x = range as well
    # Check base case
    if high > low:
        mid = (high + low) // 2

        # If element is present in the middle range itself
        if arr[mid][0] <= x[0] <= arr[mid][1]:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif x < arr[mid][0]:
            return binary_search(arr, low, mid - 1, x)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


class EfficientReactor:
    def __init__(self, size):
        # only keep track of lights that are on
        self.size = size
        self.lit_ranges = []
        self.x_ranges = set()
        self.y_ranges = set()

    def turn_on(self,  x_range, y_range, z_range):
        # check if overlapping
        ## Check x:
        # Function call
        result = binary_search(arr, 0, len(arr) - 1, x)
        # if not overlapping
        self.lit_ranges.append([x_range, y_range, z_range])
        # sort the updated list
        self.lit_ranges = sorted(self.lit_ranges, key=lambda x: (x[0], x[1], x[2]))


        for x in range(max(-self.size, x_range[0]), 1+ min(self.size, x_range[1])):
            for y in range(max(-self.size, y_range[0]), 1+ min(self.size,y_range[1])):
                for z in range(max(-self.size, z_range[0]),1+ min(self.size,z_range[1])):
                    # turn on light
                    self.lit_cubes.add((x, (y, z)))

    def turn_off(self,  x_range, y_range, z_range):
        light_out = set()
        # here we don't care if the cubes are out of range, could still add the max/min check
        for x in range(x_range[0], x_range[1] + 1):
            for y in range(y_range[0], y_range[1] + 1):
                for z in range(z_range[0], z_range[1] + 1):
                    # turn on light
                    light_out.add((x, (y, z)))
        self.lit_cubes = self.lit_cubes.difference(light_out)

    def do_instruction(self, instruction, x_range, y_range, z_range):
        if instruction == "on":
            self.turn_on(x_range, y_range, z_range)
        elif instruction == "off":
            self.turn_off(x_range, y_range, z_range)

    def get_number_lit_cubes(self):
        return len(self.lit_cubes)

class Reactor:
    def __init__(self, size):
        # only keep track of lights that are on
        self.size = size
        self.lit_cubes = set()

    def turn_on(self,  x_range, y_range, z_range):
        if self.size > 0:
            for x in range(max(-self.size, x_range[0]), 1+ min(self.size, x_range[1])):
                for y in range(max(-self.size, y_range[0]), 1+ min(self.size,y_range[1])):
                    for z in range(max(-self.size, z_range[0]),1+ min(self.size,z_range[1])):
                        # turn on light
                        self.lit_cubes.add((x, (y, z)))
        else:
            for x in range( x_range[0], 1 +  x_range[1]):
                for y in range( y_range[0], 1 +  y_range[1]):
                    for z in range( z_range[0], 1 +  z_range[1]):
                        # turn on light
                        self.lit_cubes.add((x, (y, z)))

    def turn_off(self,  x_range, y_range, z_range):
        light_out = set()
        # here we don't care if the cubes are out of range, could still add the max/min check
        for x in range(x_range[0], x_range[1] + 1):
            for y in range(y_range[0], y_range[1] + 1):
                for z in range(z_range[0], z_range[1] + 1):
                    # turn on light
                    light_out.add((x, (y, z)))
        self.lit_cubes = self.lit_cubes.difference(light_out)

    def do_instruction(self, instruction, x_range, y_range, z_range):
        if instruction == "on":
            self.turn_on(x_range, y_range, z_range)
        elif instruction == "off":
            self.turn_off(x_range, y_range, z_range)

    def get_number_lit_cubes(self):
        return len(self.lit_cubes)


def get_puzzle_input(filepath):
    instructions = []
    with open(filepath) as f:
        for line in f:
            parts = line.rstrip().split()
            instruction = [parts[0]] # parts[0] = on/off
            [x,y,z] = parts[1].split(',')
            x = [int(n) for n in x[2:].split('..')]
            y = [int(n) for n in y[2:].split('..')]
            z = [int(n) for n in z[2:].split('..')]
            instruction.extend([x, y, z])
            instructions.append(instruction)
    return instructions


def resolve_puzzle(filepath, size):
    instructions = get_puzzle_input(filepath)
    reactor = Reactor(size)
    for instruction in instructions:
        reactor.do_instruction(instruction[0], instruction[1], instruction[2], instruction[3])
    lit = reactor.get_number_lit_cubes()
    print("{}\nPUZZLE SOLUTION: {} lit cubes".format(filepath, lit))


print("Part 1")
# resolve_puzzle("small_test.txt", 50)
# resolve_puzzle("test_data.txt", 50)
# resolve_puzzle("data.txt", 50)

print("Part 2")
# resolve_puzzle("test_data.txt", 50)
resolve_puzzle("data.txt", -1)
