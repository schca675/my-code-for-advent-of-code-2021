# --- Day 12: Passage Pathing ---

class Path:
    def __init__(self, cave):
        self.cave = cave
        self.has_visited_lower_caves = dict()
        for node in cave.nodes:
            if node == node.lower():
                self.has_visited_lower_caves[node] = False

class Cave:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges # tuples (a, b) connections
        self.neighbours = dict() # node --> neighbours
        for edge in self.edges:
            conn_a = self.neighbours.get(edge[0], set())
            conn_a.add(edge[1])
            conn_b = self.neighbours.get(edge[1], set())
            conn_b.add(edge[0])
            self.neighbours[edge[0]] = conn_a
            self.neighbours[edge[1]] = conn_b


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
        # print(display.digits, ":", digits_str)
        tot_digits += number
    print("PUZZLE SOLUTION: {} sum of all digits".format(tot_digits))

print("TEST")
resolve_puzzle_part1("test_data.txt")
print("PUZZLE")
# resolve_puzzle_part1("data.txt")
#
# print("TEST")
# resolve_puzzle_part2("test_data.txt")
# print("PUZZLE")
# resolve_puzzle_part2("data.txt")