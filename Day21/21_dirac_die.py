# --- Day 21: Dirac Dice ---
import copy
import time

import numpy as np


class DeterministicDie:
    def get_dice(self, step):
        # 3* for 3 DICE steps how many times times 3 has happened * times 3 to add to all die
        # Turn 1: P1 rolls 1,2,3
        return 9*(step-1) + 6 # (1+2+3)


def get_score_deterministic_die(p1_start, p2_start):
    die = DeterministicDie()
    # 10 fields: 0,1,2,3,4,5,6,7,8,9: x % 10
    # score: field +
    throws = 0
    current_player = 1
    player_position = {2:p2_start-1, 1:p1_start-1} # -1 to make it adhere to 0-9 playground
    player_score = {2:0, 1:0}
    while player_score[2] < 1000 and player_score[1] < 1000:
        throws += 1
        # update score
        player_position[current_player] = (player_position[current_player] + die.get_dice(throws)) % 10
        player_score[current_player] += player_position[current_player] + 1 # to offset 0-9 playground
        current_player = 3- current_player
    total_die_throws = 3*throws # 3 per step
    return player_score, player_position, total_die_throws, total_die_throws*min(player_score[1], player_score[2])



class DiracDie:
    def __init__(self):
        self.score_dict = {0:{}, 1:{}} # 0/1: whose turn it is
        # 10 fields: 0,1,2,3,4,5,6,7,8,9: x % 10
        # score: field + 1
        #   1 2 3       1       2       3
        # 1 2 3 4    (3,4,5) (4,5,6) (5,6,7)
        # 2 3 4 5    (4,5,6) (5,6,7) (6,7,8)
        # 3 4 5 6    (5,6,7) (6,7,8) (7,8,9)
        #
        # ---> outcome: how often
        # ----> 3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1.
        self.die_outcomes = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}

    def get_score_dirac_die_recursive(self, dimension, current_player):
        # total wins for 1 of these dimension
        total_wins = [0,0]
        # get state of current dimension
        pos, score = dimension[0], dimension[1]
        for die, occurrence in self.die_outcomes.items():
            # update pos with die
            new_pos_current_player = (pos[current_player] + die) % 10
            # update score
            new_score_current_player = score[current_player] + new_pos_current_player + 1 # to offset 0-9 playground
            # resolve score
            if new_score_current_player >= 21:
                # this player wins
                total_wins[current_player] += occurrence
            else:
                # Make tuples of new positions of players after this die:
                if current_player == 0:
                    new_pos = (new_pos_current_player, pos[1])
                    new_score = (new_score_current_player, score[1])
                else:
                    new_pos = (pos[0], new_pos_current_player)
                    new_score = (score[0], new_score_current_player)
                # check if new dimension (next turn) has already been in the score dict:
                new_dimension_hash = (new_pos, new_score)
                if new_dimension_hash in self.score_dict[1-current_player]:
                    [p1_wins_in_this_dimension, p2_wins_after_this_dimension] = self.score_dict[1-current_player][new_dimension_hash]
                else:
                    # if not: recursively check new round:
                    new_dimension = [new_pos, new_score, 1]
                    [p1_wins_in_this_dimension, p2_wins_after_this_dimension] = self.get_score_dirac_die_recursive(new_dimension, 1-current_player)
                total_wins[0] += p1_wins_in_this_dimension * occurrence  # p1_wins: once; so multiply with how often this die is rolled
                total_wins[1] += p2_wins_after_this_dimension * occurrence

        # Return score
        dimension_hash = ((pos[0], pos[1]), (score[0], score[1]))
        self.score_dict[current_player][dimension_hash] = total_wins # for 1 of these dimensions (positions + scores), we got so many wins
        return [x*dimension[2] for x in total_wins] # we have dimension[2] of this dimension


def get_score_dirac_p2_rec(p1_start, p2_start):
    die = DiracDie()
    return die.get_score_dirac_die_recursive([(p1_start-1, p2_start-1), (0,0), 1], 0)


def resolve_puzzle_part1(p1_start, p2_start):
    player_score, player_position, throws, res = get_score_deterministic_die(p1_start, p2_start)
    print("SOLUTION part 1: ", res)


def resolve_puzzle2_rec(p1_start, p2_start):
    total_wins = get_score_dirac_p2_rec(p1_start, p2_start)
    print("Starting position: ({},{})".format(p1_start, p2_start))
    print('Solution: ', total_wins)

# test.txt
# resolve_puzzle_part1(4, 8) # Part 1
# resolve_puzzle2_rec(4, 8)  # Part 2
# data.txt
start = time.time()
resolve_puzzle_part1(6, 8)   # Part 1  0.0s
print("Time: ", time.time()-start)
start = time.time()
resolve_puzzle2_rec(6, 8)    # Part 2 0.3254072666168213
print("Time: ", time.time()-start)