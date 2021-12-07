# --- Day 6: Lanternfish ---

class Lanternfish:
    reproduction_value = 7

    def __init__(self, fish_timer_str):
        self.internal_timer = int(fish_timer_str)

    def update_timer(self):
        # new fish is created when timer is reset to 6, so when current timer is 0
        if self.internal_timer == 0:
            self.internal_timer = self.reproduction_value - 1 # -1 since 0 is also taken into account
            return True, Lanternfish(str(self.reproduction_value + 2 - 1))
        # otherwise only update (this will not be negative)
        self.internal_timer = self.internal_timer - 1 % self.reproduction_value
        # otherwise no new fish is created
        return False, None

    def __str__(self):
        return str(self.internal_timer)

def get_puzzle_input(filepath):
    fish = []
    with open(filepath) as f:
        for line in f:
            parts = line.rstrip().split(',')
            for fish_timer in parts:
                fish.append(Lanternfish(fish_timer))
    return fish

def resolve_puzzle_part1(filepath, days):
    fish = get_puzzle_input(filepath)
    for i in range(0, days):
        new_fish = []
        for lantern_fish in fish:
            is_new_fish, new_lantern_fish = lantern_fish.update_timer()
            # if there is a new fish: add it to existing fish
            if is_new_fish:
                new_fish.append(new_lantern_fish)
        # add newly created fish to fish pool
        fish.extend(new_fish)
    print("After {} days we have {} fish".format(days, len(fish)))

#
# print("TEST")
# resolve_puzzle_part1("test_data.txt", 80)
# print("PUZZLE")
# resolve_puzzle_part1("data.txt", 80)

class LanternFishGroup(Lanternfish):
    def __init__(self, fish_timer_str, amount):
        super().__init__(fish_timer_str=fish_timer_str)
        self.number_of_fish = amount

    def add_new_fish_to_group(self, amount):
        self.number_of_fish += amount

    def get_count(self):
        return self.number_of_fish

    def update_timer(self):
        # new fish is created when timer is reset to 6, so when current timer is 0
        if self.internal_timer == 0:
            self.internal_timer = self.reproduction_value - 1 # -1 since 0 is also taken into account
            return True, None
        # otherwise only update (this will not be negative)
        self.internal_timer = self.internal_timer - 1 % self.reproduction_value
        # otherwise no new fish is created
        return False, None

    def __str__(self):
        return str(self.internal_timer) + ":" + str(self.number_of_fish)

def get_puzzle_input_efficient(filepath):
    fish = []
    with open(filepath) as f:
        for line in f:
            parts = line.rstrip().split(',')
            for fish_timer in parts:
                fish.append(LanternFishGroup(fish_timer, 1))
    return fish

def get_total_number_of_fish(fishgroups):
    sum = 0
    for fish_group in fishgroups:
        sum+= fish_group.get_count()
    return sum

def resolve_puzzle_part2(filepath, days):
    fish = get_puzzle_input_efficient(filepath)
    for i in range(0, days):
        new_fish = 0
        for lantern_fish in fish:
            is_new_fish, _ = lantern_fish.update_timer()
            # count how many new fish
            if is_new_fish:
                # Every fish in group makes a new fish
                new_fish += lantern_fish.number_of_fish
        fish.append(LanternFishGroup(str(Lanternfish.reproduction_value + 1), new_fish))
        # no fish with a timer of 8 exists anymore, so we can add a new class
        # --> can be optimized once the timer is reset, merging all classes that created new fish that moment.
        # Now this list still increases but only linearly (1 more class per day).
    print("After {} days we have {} fish".format(days, get_total_number_of_fish(fish)))


print("TEST 2")
resolve_puzzle_part2("test_data.txt", 256)
print("PUZZLE 2")
resolve_puzzle_part2("data.txt", 256)

