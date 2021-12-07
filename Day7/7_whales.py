# --- Day 7: The Treachery of Whales ---
import pandas as pd


def get_puzzle_input(filepath):
    crab_positions = []
    with open(filepath) as f:
        for line in f:
            parts = line.rstrip().split(',')
            for crab_position in parts:
                crab_positions.append(int(crab_position))
    return crab_positions


def get_position_of_lowest_fuel_one_fuel_per_step(crabs):
    min_crabs = min(crabs)
    max_crabs = max(crabs)
    all_fuels = []
    for crab_pos in crabs:
        # fuel to be spent to end in every position
        # crab_pos + fuel = end_pos if  end_pos > crab_pos
        # crab_pos - fuel = end
        fuel_for_crab = [crab_pos - end_pos if end_pos < crab_pos else end_pos - crab_pos for end_pos in range(min_crabs, max_crabs + 1)]
        all_fuels.append(fuel_for_crab)
    df_fuel = pd.DataFrame(all_fuels)
    return min([sum(df_fuel[col]) for col in df_fuel])


def resolve_puzzle_part1(filepath):
    crab_positions = get_puzzle_input(filepath)
    min_fuel = get_position_of_lowest_fuel_one_fuel_per_step(crab_positions)
    print("PUZZLE SOLUTION: minimally {} fuel necessary".format(min_fuel))

print("TEST")
resolve_puzzle_part1("test_data.txt")
print("PUZZLE")
resolve_puzzle_part1("data.txt")


def get_position_of_lowest_fuel_increasing_steps(crabs):
    min_crabs = min(crabs)
    max_crabs = max(crabs)
    all_fuels = []
    for crab_pos in crabs:
        # fuel to be spent to end in every position
        # crab_pos + fuel = end_pos if  end_pos > crab_pos
        # crab_pos - fuel = end
        ## SUM: m*(m+1)/2
        fuel_for_crab = [(crab_pos - end_pos) * (crab_pos - end_pos + 1)/2 if end_pos < crab_pos
                         else (end_pos - crab_pos) * (end_pos - crab_pos + 1)/2
                         for end_pos in range(min_crabs, max_crabs + 1)]

        all_fuels.append(fuel_for_crab)
    df_fuel = pd.DataFrame(all_fuels)
    return min([sum(df_fuel[col]) for col in df_fuel])

def resolve_puzzle_part2(filepath):
    crab_positions = get_puzzle_input(filepath)
    min_fuel = get_position_of_lowest_fuel_increasing_steps(crab_positions)
    print("PUZZLE SOLUTION: minimally {} fuel necessary".format(min_fuel))

print("TEST")
resolve_puzzle_part2("test_data.txt")
print("PUZZLE")
resolve_puzzle_part2("data.txt")
