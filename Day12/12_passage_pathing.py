# --- Day 12: Passage Pathing ---
import copy


class Path:
    def __init__(self, cave, steps_taken, next_step, has_visited_lower_caves):
        self.has_visited_lower_caves = has_visited_lower_caves
        if len(has_visited_lower_caves) == 0:
            for node in cave.nodes:
                # set all nodes to False, upper-case ones will stay false
                self.has_visited_lower_caves[node] = False
        # if it is a lower case step: set it to true if that is the next step
        if next_step == next_step.lower():
            self.has_visited_lower_caves[next_step] = True
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
        all_paths = []
        for path in paths_so_far:
            updated_paths = []
            # if path has reached end --> skip
            if path.steps_taken[-1] == 'end':
                # end is reached, so we attach it to all paths without next steps
                all_paths.append(path)
                continue
            # Else: Check next steps and add those to final list
            for poss_steps in self.neighbours[path.steps_taken[-1]]:
                if not path.has_visited_lower_caves[poss_steps]:
                    new_path = Path(self, copy.deepcopy(path.steps_taken), poss_steps, copy.deepcopy(path.has_visited_lower_caves))
                    updated_paths.append(new_path)
            all_paths.extend(self.get_all_paths(updated_paths))
        return all_paths


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
    paths = cave.get_all_paths([Path(cave, [], 'start', dict())])
    print("PUZZLE SOLUTION: {} unique paths".format(len(paths)))

def resolve_puzzle_part2(filepath):
    pass

print("TEST")
resolve_puzzle_part1("test_data.txt")
print("PUZZLE")
resolve_puzzle_part1("data.txt")
#
# print("TEST")
# resolve_puzzle_part2("test_data.txt")
# print("PUZZLE")
# resolve_puzzle_part2("data.txt")