# --- Day 18: Snailfish ---
import copy
import math
import re


class snail_fish_number:
    def __init__(self, number_str):
        self.representation = number_str

    def reduce_number_once(self, also_split=False):
        rep = copy.deepcopy(self.representation)
        i = 0
        index_leftmost = -1
        index_left_end = -1
        nr_leftmost = -1
        depth = 0
        no_action = True
        while no_action and i < len(rep):
            # walk over string from left to right
            c = rep[i]
            if c == '[':
                depth += 1
                if depth > 4:
                    # EXPLODE
                    no_action = False
                    # Exploding pairs always consist of regular numbers,
                    # so i1234
                    #    [2,3] or [12, 10]
                    # find the length of current bracket
                    m = re.search("]", rep[i+1:])
                    next_bracket =i+5
                    if m:
                        next_bracket = i + 2 + m.start()  # i+1 for start index, then + 1 to get placement after ]
                    [left, right] = rep[i+1:next_bracket-1].split(',')
                    left, right = int(left), int(right)
                    # if there are no numbers to the left or right, we keep the original:
                    left_rep = rep[:i]
                    right_rep = rep[next_bracket:]

                    # if there is one: add left to next left number
                    if index_leftmost > 0:
                        new_number = nr_leftmost + left
                        # check if it is more than one digit
                        left_rep = "{}{}{}".format(rep[:index_leftmost], new_number, rep[index_left_end+1:i])

                    # if there is one to the right
                    m = re.search(r"\d", rep[next_bracket:])
                    if m:
                        right_first_i = next_bracket + m.start()
                        right_end_i = right_first_i
                        right_int = rep[right_first_i]
                        while rep[right_end_i + 1].isdigit():
                            right_end_i += 1
                            right_int += rep[right_end_i]
                        right_int = int(right_int) + right
                        right_rep = "{}{}{}".format(rep[next_bracket:right_first_i], right_int, rep[right_end_i+1:])
                        # right_i is first index where there was no digit anymore

                    # add right to next right number
                    # replace exploding part by 0
                    rep = "{}{}{}".format(left_rep,0,right_rep)
                    self.representation = rep
            elif c == ']':
                depth -= 1
            elif c != ',':
                index_leftmost = i
                index_left_end = i
                # then c must be an integer
                while rep[i+1].isdigit():
                    i += 1
                    c += rep[i]
                    index_left_end = i

                c = int(c)
                nr_leftmost = c

                if also_split and c >= 10:
                    # SPLITS
                    no_action = False
                    c = c/2
                    rep = "{}{}{}".format(rep[:index_leftmost],[math.floor(c), math.ceil(c)], rep[i+1:])
                    self.representation = rep
            i +=1
        return no_action

    def reduce_number(self):
        no_action = False
        while not no_action:
            # check only explodes first
            while not no_action:
                no_action = self.reduce_number_once()
            no_action = self.reduce_number_once(also_split=True)

    def __str__(self):
        return self.representation

    def add_number_to_it(self, other):
        self.representation = "[{},{}]".format(self.representation, other.representation)
        self.reduce_number()

    def parse_number(self):
        # [1:-1] to remove outer brackets surrounding number
        [left, right] = self.representation[1:-1].split('')
        if '[' in left:
            left = self.parse_number()
        if '[' in right:
            right = self.parse_number()
        return [int(left), int(right)]

    def get_magnitude(self):
        # if there is one to the right
        magnitude = copy.deepcopy(self.representation)
        m = re.search(r'\[\d+,\d+\]', magnitude)
        while m:
            start = m.start()
            end = m.end()
            [left, right] = magnitude[start+1: end-1].split(',')
            magnitude = "{}{}{}".format(magnitude[:start], 3*int(left) + 2*int(right), magnitude[end:])
            m = re.search(r'\[\d+,\d+\]', magnitude)
        return magnitude


def get_puzzle_input(filepath):
    snail_fish_numbers = []
    with open(filepath) as f:
        for line in f:
            snail_fish_numbers.append(snail_fish_number(line.rstrip()))
    return snail_fish_numbers


def resolve_puzzle(filepath):
    snail_fish_numbers = get_puzzle_input(filepath)
    # add all snailfish to first one:
    for i in range(1, len(snail_fish_numbers)):
        snail_fish_numbers[0].add_number_to_it(snail_fish_numbers[i])
    magnitude = snail_fish_numbers[0].get_magnitude()
    print("{}\nPUZZLE SOLUTION: {}\n magnitude: {} ".format(filepath,
                                                            snail_fish_numbers[0], magnitude))

def resolve_puzzle_part2(filepath):
    print(filepath)
    snail_fish_numbers = get_puzzle_input(filepath)
    max_mag = 0
    for i in range(0, len(snail_fish_numbers)):
        rep = copy.deepcopy(snail_fish_numbers[i].representation)
        for j in range(0, len(snail_fish_numbers)):
            if i !=j:
                snail_fish_numbers[i].representation = copy.deepcopy(rep)
                snail_fish_numbers[i].add_number_to_it(snail_fish_numbers[j])
                # sometimes spaces appear
                snail_fish_numbers[i].representation = snail_fish_numbers[i].representation.replace(' ', '')
                mag = int(snail_fish_numbers[i].get_magnitude())
                # print(rep, " + \n", snail_fish_numbers[j], " = \n", str(mag))
                if mag > max_mag:
                    max_mag = mag
        snail_fish_numbers[i].representation = copy.deepcopy(rep)
    print("MAX Magnitude:", max_mag)

def test():
    # Get string representation of two fish
    test_snailfish = get_puzzle_input("test_snails.txt")
    test_snailfish[0].reduce_number()
    for i in range(1, len(test_snailfish)):
        test_snailfish[0].add_number_to_it(test_snailfish[i])
    print("TEST: Resulting fish: ", str(test_snailfish[0]))

def test_mag():
    test_snailfish = get_puzzle_input("test_magnitudes")
    for fish in test_snailfish:
        print(fish)
        print(fish.get_magnitude())
# test()
# test_mag()

print("Part 1")
# resolve_puzzle("test_data.txt")
# # resolve_puzzle("sum_example.txt")
# resolve_puzzle("data.txt")
# #
# print( "Part 2")
resolve_puzzle_part2("test_data.txt")
resolve_puzzle_part2("data.txt")