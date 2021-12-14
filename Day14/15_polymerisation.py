# --- Day 14: Extended Polymerization ---
import copy
import time


def get_puzzle_input(filepath):
    rule_dict = dict()
    start_polymere = ""
    with open(filepath) as f:
        for line in f:
            if '->' in line:
                # is a rule:
                rule = line.rstrip().replace(" ", "").split('->')
                rule_dict[rule[0]] = rule[1]
            else:
                # first or second line, second line empty so we can also attach it to start polymere
                start_polymere += line.rstrip()
    return start_polymere, rule_dict


def do_pair_insertion(polymere, rule_dict):
    result = ""
    for i in range(0, len(polymere)-1):
        pair = polymere[i:i+2] # first index inclusive, second exclusive
        insert = rule_dict.get(pair, "")
        result += "{}{}".format(pair[0], insert) # don't append second character
    # correct for last character which still needs to be added
    result += polymere[-1]
    return result


def count_letters_after_iterations(pair, count_dict, rule_dict, iterations_left, pair_dict, reset_dict):
    if iterations_left > 0:
        insert = rule_dict.get(pair, "")
        # new pairs for the next iterations:
        #f.ex NC --> NBC --> NB and NC
        if (pair, iterations_left) in pair_dict.keys():
            # add values we already found to the dictionary
            for (k,v) in pair_dict[(pair, iterations_left)].items():
                count_dict[k] = count_dict.get(k, 0) + v
                reset_dict[k] = reset_dict.get(k, 0) + v
        else:
            # count values for this round
            new_reset_dict = dict()
            count_letters_after_iterations(pair[0] + insert, count_dict, rule_dict, iterations_left - 1, pair_dict,
                                           new_reset_dict)
            count_letters_after_iterations(insert + pair[1], count_dict, rule_dict, iterations_left - 1, pair_dict,
                                           new_reset_dict)
            pair_dict[(pair, iterations_left)] = new_reset_dict
            for (k,v) in new_reset_dict.items():
                reset_dict[k] =  reset_dict.get(k, 0) + v
    else:
        count_dict[pair[0]] = count_dict.get(pair[0], 0) + 1
        reset_dict[pair[0]] = reset_dict.get(pair[0], 0) + 1
        pair_dict[(pair, iterations_left)] = {pair[0]: 1}


def get_score(polymere):
    counts = {}
    # count characters
    for char in polymere:
        counts[char] = counts.get(char, 0) + 1
    # sort characters
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts[0][1] - sorted_counts[-1][1], sorted_counts


def get_score_from_dict(counts):
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts[0][1] - sorted_counts[-1][1]


def resolve_puzzle_part2(filepath, iterations):
    start_polymere, rule_dict = get_puzzle_input(filepath)
    polymere = start_polymere
    count_dict = dict()
    pair_dict = dict()
    # for every pair in polymere, get count
    for i in range(0, len(polymere) - 1):
        count_dic_per_round = dict()
        pair = polymere[i:i + 2]  # first index inclusive, second exclusive
        count_letters_after_iterations(pair, count_dic_per_round, rule_dict, iterations, pair_dict, dict())
        for (k,v) in count_dic_per_round.items():
            count_dict[k] = count_dict.get(k, 0) + v
    count_dict[polymere[-1]] = count_dict.get(polymere[-1], 0) + 1  # last character not counted before
    score = get_score_from_dict(count_dict)
    print("Score: {}\n Dictionary: ".format(score))

def resolve_puzzle_part1(filepath, iterations):
    start_polymere, rule_dict = get_puzzle_input(filepath)
    polymere = start_polymere
    for i in range(0, iterations):
        polymere = do_pair_insertion(polymere, rule_dict)
    print("Polymere is {}".format(polymere))
    score, count_dic = get_score(polymere)
    print("Score: {}\n Count dic: {}".format(score, count_dic))

print("TEST")
start = time.time()
resolve_puzzle_part1("test_data.txt", 10)
print("PUZZLE")
# resolve_puzzle_part1("data.txt", 20)
print("Time: {}".format(time.time()-start))

print("TEST")
start = time.time()
resolve_puzzle_part2("test_data.txt", 40)
print("PUZZLE")
resolve_puzzle_part2("data.txt", 40)
print("Time: {}".format(time.time()-start))