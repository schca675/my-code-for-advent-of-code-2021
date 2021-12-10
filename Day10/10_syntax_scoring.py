# --- Day 10: Syntax Scoring ---
import statistics

syntax_score_dic = {')': 3,
             ']': 57,
             '}': 1197,
             '>':25137}
autocomplete_score_dic = {')': 1,
             ']': 2,
             '}': 3,
             '>': 4}
pairs = {'}': '{',
                  ')': '(',
                  ']': '[',
                  '>': '<'}
inv_pairs = {'{':'}',
             '[':']',
             '(':')',
             '<':'>'}

def check_if_corrupted(line):
    # To check for corruption, we keep track how many brackets have been opened
    opened = {'{': 0,
              '(': 0,
              '[': 0,
              '<': 0}
    last_opened = []
    for char in line:
        if char not in opened.keys():
            # char is a closing character.
            # Check if the last opened character is this one
            if last_opened[-1] != pairs[char]:
               # different character was opened last --> corrupt
                return True, char
            # Not needed for puzzle
            # Check if corresponding closing character has been opened:
            # elif opened[pairs[char]] == 0:
            #     # if it wasn't opened ---> line corrupt
            #     print("Got closing character that was not opened")
            #     return True, char
            else:
                # if it was opened: close a bracket now
                opened[pairs[char]]+= -1
                last_opened = last_opened[:-1]
        else:
            # open the character
            # can have characters internnested
            opened[char] += 1
            last_opened.append(char)
    # if this code is reached, the line is not corrupted
    last_opened.reverse()
    return False, "".join([inv_pairs[c] for c in last_opened])



class SyntaxChecker(object):
    def __init__(self, line):
        self.line = line
        self.is_corrupted = False
        self.problem_char = ''

    def check_if_corrupted(self):
        # returns True if corrupted + character where it went wrong
        self.is_corrupted, self.problem_char = check_if_corrupted(self.line)
        return self.is_corrupted, self.problem_char


def get_puzzle_input(filepath):
    syntax_checkers = []
    with open(filepath) as f:
        for line in f:
            syntax_checkers.append(SyntaxChecker(line.rstrip()))
    return syntax_checkers


def get_autocorrect_score(closing_chars):
    scores = []
    # get score for every line
    for s in closing_chars:
        score = 0
        for c in s:
            score = score * 5
            score += autocomplete_score_dic[c]
        scores.append(score)
    return statistics.median(scores)


def resolve_puzzle_part1(filepath):
    syntax_checkers = get_puzzle_input(filepath)
    corrupted_lines = []
    not_corrupted_lines = []
    score = 0
    for checker in syntax_checkers:
        # True if corrupted, then expected and found symbol shown, False if not, then None returned
        is_corrupted, found = checker.check_if_corrupted()
        if is_corrupted:
            # if corrupted, found is problematic character
            score += syntax_score_dic[found]
            corrupted_lines.append([checker.line, found])
        else:
            # if not corrupted, line is a string of closing characters to make line complete
            not_corrupted_lines.append([checker.line, found])
    auto_correct_score = get_autocorrect_score([x[1] for x in not_corrupted_lines])
    print("PUZZLE SOLUTION part 1: {} corrupted lines with a score of {}.".format(len(corrupted_lines), score))
    print("PUZZLE SOLUTION part 2: {} uncorrupted lines with a score of {} for autocompletion.".format(
        len(not_corrupted_lines), auto_correct_score))


def resolve_puzzle_part2(filepath):
    displays = get_puzzle_input(filepath)
    tot_digits = 0
    for display in displays:
        display.solve()
        digits, digits_str, number = display.decrypt_digits()
        # print(display.digits, ":", digits_str)
        tot_digits += number
    print("PUZZLE SOLUTION: {} sum of all digits".format(tot_digits))

print("TEST")
resolve_puzzle_part1("test_data.txt")
print("PUZZLE")
resolve_puzzle_part1("data.txt")

# print("TEST")
# resolve_puzzle_part2("test_data.txt")
# print("PUZZLE")
# resolve_puzzle_part2("data.txt")