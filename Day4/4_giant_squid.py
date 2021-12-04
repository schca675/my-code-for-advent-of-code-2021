### #### PUZZLE 4 - 02/12/2021 Giant Squid!
import pandas as pd
import numpy as np


class BingoCard:
    def __init__(self, bingo_df, id):
        self.bingo_card = bingo_df
        # No entry is marked
        self.marked_numbers = pd.DataFrame(np.zeros(self.bingo_card.shape))
        self.bingo_card_id = id
        self.had_bingo_already = False

    def mark_number(self, number):
        # Probably there is sth more efficient
        for row_index, row in self.bingo_card.iterrows():
            for colum_index, value in row.items():
                if value == number: # e.g bingo value equal to the called number
                    #mark it
                    self.marked_numbers[colum_index][row_index] = 1
                    pass

    def has_bingo(self):
        # Do not call bingo again if bingo has been called once:
        if self.had_bingo_already:
            return False
        # Check columns
        for col in self.marked_numbers:
            # Bingo if there are only 1's and no more 0's in a column, so product of col == 1.
            if np.prod(self.marked_numbers[col].values) == 1:
                self.had_bingo_already = True
                return True
        # Check rows
        for _, row in self.marked_numbers.iterrows():
            if np.prod(row) == 1:
                self.had_bingo_already = True
                return True
        return False

    def get_score(self):
        # The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board
        sum_unmarked = 0
        for row_index, row in self.marked_numbers.iterrows():
            for colum_index, value in row.items():
                if value == 0: # e.g unmarked
                    sum_unmarked += int(self.bingo_card.at[row_index, colum_index])
        return sum_unmarked

    def __str__(self):
        return str(self.bingo_card) + " \n \n " + str(self.marked_numbers)



def get_input_data(filepath):
    list_bingo_cards = []
    bingo_id = 0 # purely to keep track of bingo cards
    with open(filepath, "r") as f:
        lines = f.readlines()
        drawn_numbers = lines[0].rstrip().split(',')
        # Formating of bingo cards:
        # 0: numbers drawn
        # 1: white space
        # 2-6: Bingo card
        start_i = 2
        while start_i < len(lines):
            bingo_nrs = [line.rstrip().split() for line in lines[start_i:start_i+5]]
            list_bingo_cards.append(BingoCard(pd.DataFrame(bingo_nrs), bingo_id))
            bingo_id += 0
            start_i += 6
    return drawn_numbers, list_bingo_cards


def resolve_puzzle_4_part1(filepath):
    # get first bingocard to win
    drawn_numbers, bingo_cards = get_input_data(filepath)
    bingo = False
    i = 0
    while not bingo and i < len(drawn_numbers):
        for bingocard in bingo_cards:
            bingocard.mark_number(drawn_numbers[i])
            if bingocard.has_bingo():
                card_score =  bingocard.get_score()
                print("BINGO: with drawn number".format(drawn_numbers[i]))
                print("card score: {}. Total score (puzzle solution): {}".format(card_score, card_score*int(drawn_numbers[i])))
                print("Bingo card: ")
                print(bingocard)
                bingo = True
                break
        i+=1

#TEST
print("TEST")
resolve_puzzle_4_part1("test_data_4.txt")

print("PUZZLE")
resolve_puzzle_4_part1("data_4.txt")

def resolve_puzzle4_part2(filepath):
    # What is the last bingocard to win
    drawn_numbers, bingo_cards = get_input_data(filepath)
    i = 0
    nr_bingo_cards_that_won = 0
    while i < len(drawn_numbers):
        for bingocard in bingo_cards:
            bingocard.mark_number(drawn_numbers[i])
            if bingocard.has_bingo():
                print("BINGO: with card number {} at drawn number {}".format(bingocard.bingo_card_id, drawn_numbers[i]))
                nr_bingo_cards_that_won += 1
                if nr_bingo_cards_that_won == len(bingo_cards): # so the last bingo card now also won
                    card_score = bingocard.get_score()
                    print("BINGO WITH LAST CARD: ")
                    print("card score: {}. Total score (puzzle solution): {}".format(card_score, card_score * int(
                        drawn_numbers[i])))
                    print("Bingo card: ")
                    print(bingocard)
        i+=1

#TEST
print("TEST")
resolve_puzzle4_part2("test_data_4.txt")
#PUZZLE
print("PUZZLE")
resolve_puzzle4_part2("data_4.txt")