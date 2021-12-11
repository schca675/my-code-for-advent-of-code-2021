# --- Day 11: Dumbo Octopus

class DumboOctopus:
    def __init__(self, energy_level):
        self.flashed_this_turn = False
        self.times_flashed = 0
        self.energy_level = energy_level

    def update_energy_level(self):
        # only update energy level if octopus has not flashed
        if not self.flashed_this_turn:
            self.energy_level += 1
        return self.will_flash()

    def will_flash(self):
        return self.energy_level > 9

    def flash(self):
        # return True if it has already flashed
        if self.flashed_this_turn:
            return True
        self.flashed_this_turn = True
        self.times_flashed += 1
        self.energy_level = 0
        return False


def get_puzzle_input(filepath):
    octopi_grid = []
    with open(filepath) as f:
        for line in f:
            octopi_line = [DumboOctopus(int(c)) for c in line.rstrip()]
            octopi_grid.append(octopi_line)
    return octopi_grid

def flash_octopus(i,j, grid):
    new_flashes = set()
    # flash octopus: if it has already flashed, return True
    has_already_flashed = grid[i][j].flash()
    if has_already_flashed:
        return new_flashes
    # add 1 energy level to surrounding octopi
    for k in [-1, 0, 1]:
        for l in [-1, 0, 1]:
            new_i = i + k
            new_j = j + l
            if 0 <= new_i < len(grid) and 0 <= new_j < len(grid[0]) and grid[new_i][new_j].energy_level != 0:
                will_flash = grid[new_i][new_j].update_energy_level()
                if will_flash:
                    new_flashes.add((new_i, new_j))
    return new_flashes


def flash_octopi(flashing_octopi, octopi_grid):
    new_flashing_octopi = set()
    for octopus_pos in flashing_octopi:
        new_flashing_octopi = new_flashing_octopi.union(flash_octopus(octopus_pos[0], octopus_pos[1], octopi_grid))
    return new_flashing_octopi


def resolve_puzzle_part1_and2(filepath, rounds):
    octopi_grid = get_puzzle_input(filepath)
    round_all_are_flashing = []
    step = 0
    while step <= rounds:
        step +=1
        # Step 2: flash
        flashing_octopi = set()
        # grid: 10x10
        # Step 1: highen energy levels by 1
        for i in range(0, len(octopi_grid)):
            for j in range(0, len(octopi_grid[0])):
                octopi_grid[i][j].flashed_this_turn = False
                will_flash = octopi_grid[i][j].update_energy_level()
                if will_flash:
                    flashing_octopi.add((i,j))
        while len(flashing_octopi) > 0:
            flashing_octopi = flash_octopi(flashing_octopi, octopi_grid)

        # Check whether all octopi flashed
        nr_flashed = 0
        for i in range(0, len(octopi_grid)):
            for j in range(0, len(octopi_grid[0])):
                if octopi_grid[i][j].flashed_this_turn:
                    nr_flashed +=1
        if nr_flashed == 100: # hardcoded how many, can also say len time slen
            break

    total_flashes = sum([sum([octopus.times_flashed for octopus in octopus_line]) for octopus_line in octopi_grid])
    print("PUZZLE SOLUTION Part 1: total_flashes after {} steps: {}".format(step, total_flashes))
    print("PUZZLE part 2: all flash on rounds {}".format(step))

def resolve_puzzle_part2(filepath):
    pass
print("TEST")
resolve_puzzle_part1_and2("test_data.txt", 10000)
print("PUZZLE")
resolve_puzzle_part1_and2("data.txt", 10000)
