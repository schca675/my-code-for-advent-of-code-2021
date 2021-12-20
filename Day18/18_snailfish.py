# --- Day 18: Snailfish ---
import math


class snail_fish_number:
    def __init__(self, number_str):
        self.number = self.parse_number(number_str)
        self.representation = number_str

    def parse_number(self, number_str):
        # [1:-1] to remove outer brackets surrounding number
        [left, right] = number_str[1:-1].split(',')
        if '[' in left:
            left = self.parse_number(left)
        if '[' in right:
            right = self.parse_number(right)
        return [int(left), int(right)]

    def reduce_number_once(self):
        rep = str(self.number)
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
                    #    [2,3]
                    left = int(rep[i+1])
                    right = int(rep[i+3])
                    # if there are no numbers to the left or right, we keep the original:
                    left_rep = rep[:i]
                    right_rep = rep[i+5:]

                    # if there is one: add left to next left number
                    if index_leftmost > 0:
                        new_number = nr_leftmost + left
                        # check if it is more than one digit
                        left_rep = "{}{}{}".format(rep[:index_leftmost], new_number, rep[index_left_end+1:i])

                    # if there is one to the right
                    right_int = ''
                    right_i = i+1
                    right_first_i = -1
                    while right_i < len(rep):
                        if rep[right_i].isdigit():
                            # check if number is larger
                            right_first_i = i
                            right_int += rep[right_i]
                            right_i += 1
                            while rep[right_i].isdigit():
                                right_int += rep[right_i]
                                right_i += 1
                            right_int = int(right_int) + right
                            break
                    if right_first_i > i:
                        # was changed, we can update right representation
                        right_rep = "{}{}{}".format(rep[:right_first_i], right_int, rep[right_i:]) # right_i is first index where there was no digit anymore

                    # add right to next right number
                    # replace exploding part by 0
                    rep = "{}{}{}".format(left_rep,0,right_rep)
            elif c == ']':
                depth -= 1
            elif c != ',':
                index_leftmost = i
                # then c must be an integer
                while rep[i+1].isdigit():
                    i += 1
                    c += rep[i]
                    index_left_end = i

                c = int(c)
                nr_leftmost = c

                if c >= 10:
                    # SPLITS
                    c = c/2
                    rep = "{}{}{}".format(rep[:index_leftmost],[math.floor(c), math.ceil(c)], rep[i+1:])
                    self.number = self.parse_number(rep)
                    no_action = False
        return no_action

    def reduce_number(self):
        no_action = False
        while not no_action:
            no_action = self.reduce_number_once()



    def get_rep(self, parent):
        [left, right] = parent
        if type(left) != int:
            left = self.get_rep(left)
        left_rep = "[{},".format(left)
        if type(right) != int:
            right = self.get_rep(right)
        right_rep = "{}]".format(right)
        return left_rep + right_rep

    def __str__(self):
        self.representation = self.get_rep(self.number)
        return self.representation


    def add_number_to_it(self, other):
        self.number = [self.number, other]
        self.reduce_number()


def get_puzzle_input(filepath):
    field = []
    image_alg = ""
    first_line = True
    with open(filepath) as f:
        for line in f:
            if first_line:
                image_alg = line.rstrip()
                first_line = False
                continue
            if len(line) > 1:
                # FIeld
                field.append(line.rstrip())
    return image_alg, field

def resolve_puzzle(filepath, times):
    image_alg, field = get_puzzle_input(filepath)
    print("{}\nPUZZLE SOLUTION: {} light pixels".format(filepath, magnitude))

print("Part 1")
resolve_puzzle("test_data.txt", 2)
resolve_puzzle("data.txt", 2)

print( "Part 2")
resolve_puzzle("test_data.txt", 50)
resolve_puzzle("data.txt", 50)