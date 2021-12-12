# --- Day 12: Passage Pathing ---

class Path:
    def __init__(self, cave, steps_taken, next_step, ):
        self.cave = cave
        self.has_visited_lower_caves = dict()
        for node in cave.nodes:
            if node == node.lower():
                self.has_visited_lower_caves[node] = False
        self.steps_taken = steps_taken
        self.steps_taken.append(next_step)



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

    def get_all_paths(self, paths_so_far):
        updated_paths = []
        for path in paths_so_far:
            # Check next steps
            for poss_steps in self.neighbours[path.steps_taken[-1]]:
                updated_paths.append(Path(self.steps_taken, self.next_step))
        return updated_paths


def get_puzzle_input(filepath):
    nodes = set()
    edges = set()
    with open(filepath) as f:
        for line in f:
            [node_1, node_2] = line.rstrip().split('-')
            nodes.add(node_1)
            nodes.add(node_2)
            edges.add((node_1, node_2))
    return Cave(nodes, edges)


def resolve_puzzle_part1(filepath):
    cave = get_puzzle_input(filepath)
    paths = cave.get_all_paths([])
    print("PUZZLE SOLUTION: {} unique paths".format(paths))

def resolve_puzzle_part2(filepath):
    pass

print("TEST")
resolve_puzzle_part1("test_data.txt")
print("PUZZLE")
# resolve_puzzle_part1("data.txt")
#
# print("TEST")
# resolve_puzzle_part2("test_data.txt")
# print("PUZZLE")
# resolve_puzzle_part2("data.txt")