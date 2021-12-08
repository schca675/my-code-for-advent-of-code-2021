# --- Day 8: Seven Segment Search ---

class DisplaySolver:

    unique_lenghts = {2: 1,
                      4: 4,
                      3: 7,
                      7: 8} # length -> digit
    def __init__(self, patterns, digits):

        self.patterns = [set(pattern) for pattern in patterns] # list of pattern Patterns
        self.digits = ["".join(sorted(digit)) for digit in digits] # list of digit Patterns
        self.len_to_digit = {} # dic: number of segments to digit
        # Solution
        self.patterns_to_digits = dict()
        self.digits_to_patterns = dict()

    def solve(self):
        patterns_5 = [] # patterns of size 5
        patterns_6 = [] # patterns of size 6
        # Determine unique numbers: 1, 4, 7, 8
        for pattern in self.patterns:
            l = len(pattern)
            if l in self.unique_lenghts:
                pattern_str = "".join(sorted(pattern))
                self.patterns_to_digits[pattern_str] = self.unique_lenghts[l]
                self.digits_to_patterns[self.unique_lenghts[l]] = pattern
                continue
            if l == 6:
                patterns_6.append(pattern)
            else:
                patterns_5.append(pattern)
        # Determine which pattern is number 3:
        ## 3 = (Intersection of all 3 patterns of length 5) union 7
        intersection_5 = patterns_5[0].intersection(patterns_5[1]).intersection(patterns_5[2])
        union_int_9 = intersection_5.union(self.digits_to_patterns[7])
        for pattern in patterns_5:
            if pattern == union_int_9:
                pattern_str = "".join(sorted(pattern))
                self.patterns_to_digits[pattern_str]  = 3
                self.digits_to_patterns[3] = pattern
                continue
        patterns_5.remove(self.digits_to_patterns[3])

        # Determine number 6
        ## pattern where cf (1) is not fully included <=> intersection of both is not length 2
        for pattern in patterns_6:
            if len(pattern.intersection(self.digits_to_patterns[1])) != 2:
                pattern_str = "".join(sorted(pattern))
                self.patterns_to_digits[pattern_str]  = 6
                self.digits_to_patterns[6] = pattern
                continue
        patterns_6.remove(self.digits_to_patterns[6])

        # Determine numbers 0 and 9
        ## substract 4 from patterns of 6: of size 2 --> 9, of size 3 --> 0
        for pattern in patterns_6:
            difference = pattern.difference(self.digits_to_patterns[4])
            if len(difference) == 2:
                pattern_str = "".join(sorted(pattern))
                self.patterns_to_digits[pattern_str]  = 9
                self.digits_to_patterns[9] = pattern
            elif len(difference) == 3:
                pattern_str = "".join(sorted(pattern))
                self.patterns_to_digits[pattern_str]  = 0
                self.digits_to_patterns[0] = pattern
            else:
                print("Shouldnt happen, error!")

        # Determine numbers 2 and 5
        ## Take difference 9 \ pattern. If result is of length 1 --> 5 elso 2.
        for pattern in patterns_5:
            diff = self.digits_to_patterns[9].difference(pattern)
            if len(diff) == 1:
                pattern_str = "".join(sorted(pattern))
                self.patterns_to_digits[pattern_str]  = 5
                self.digits_to_patterns[5] = pattern
            else:
                pattern_str = "".join(sorted(pattern))
                self.patterns_to_digits[pattern_str]  = 2
                self.digits_to_patterns[2] = pattern

    def decrypt_digits(self):
        digits = [self.patterns_to_digits[digit] for digit in self.digits]
        digits_str = "".join([str(d) for d in digits])
        return digits, digits_str, int(digits_str)

    def get_and_count_unique_digits(self):
        sum = 0
        for pattern in self.digits:
            l = len(pattern)
            if l in self.unique_lenghts:
                sum += 1
        return sum


def get_puzzle_input(filepath):
    displays = []
    with open(filepath) as f:
        for line in f:
            parts = line.rstrip().split('|')
            display = DisplaySolver(patterns=parts[0].split(), digits=parts[1].split())
            displays.append(display)
    return displays


def resolve_puzzle_part1(filepath):
    displays = get_puzzle_input(filepath)
    tot_unique_digits = 0
    for display in displays:
        digit_count = display.get_and_count_unique_digits()
        tot_unique_digits += digit_count
    print("PUZZLE SOLUTION: {} unique digits".format(tot_unique_digits))

def resolve_puzzle_part2(filepath):
    displays = get_puzzle_input(filepath)
    tot_digits = 0
    for display in displays:
        display.solve()
        digits, digits_str, number = display.decrypt_digits()
        print(display.digits, ":", digits_str)
        tot_digits += number
    print("PUZZLE SOLUTION: {} sum of all digits".format(tot_digits))

# print("TEST")
# resolve_puzzle_part1("test_data.txt")
# print("PUZZLE")
# resolve_puzzle_part1("data.txt")
#
# print("TEST")
resolve_puzzle_part2("test_data.txt")
# resolve_puzzle_part2("errorish.txt")
print("PUZZLE")
resolve_puzzle_part2("data.txt")