import pandas as pd
import numpy as np


class BingoCard:
    def __init__(self, bingo_df):
        self.bingo_card = bingo_df
        # No entry is marked
        self.marked_numbers = pd.DataFrame(np.zeros(self.bingo_card.shape))

    def mark_number(self, number):
        # Probably there is sth more efficient
        for row_index, row in self.bingo_card.iterrows():
            for colum_index, value in row.items():
                if value == number: # e.g bingo value equal to the called number
                    #mark it
                    self.marked_numbers[colum_index][row_index] = 1
                    pass

    def has_bingo(self):
        # Check columns
        for col in self.marked_numbers:
            # Bingo if there are only 1's and no more 0's in a column, so product of col == 1.
            if np.prod(self.marked_numbers[col].values) == 1:
                return True
        # Check rows
        for _, row in self.marked_numbers.iterrows():
            if np.prod(row) == 1:
                return True
        return False

    def get_score(self):
        sum_unmarked = 0
        for row_index, row in self.marked_numbers.iterrows():
            for colum_index, value in row.items():
                if value == 0: # e.g unmarked
                    sum_unmarked += int(self.bingo_card.at[row_index, colum_index])
        # The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board
        return sum_unmarked

    def __str__(self):
        return str(self.bingo_card) + " \n \n " + str(self.marked_numbers)



def get_input_data(filepath):
    list_bingo_cards = []
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
            list_bingo_cards.append(BingoCard(pd.DataFrame(bingo_nrs)))
            start_i += 6
    return drawn_numbers, list_bingo_cards


def resolve_puzzle_4_part1(filepath):
    drawn_numbers, bingo_cards = get_input_data(filepath)
    bingo = False
    i = 0
    while not bingo and i < len(drawn_numbers):
        for bingocard in bingo_cards:
            bingocard.mark_number(drawn_numbers[i])
            if bingocard.has_bingo():
                card_score =  bingocard.get_score()
                print("BINGO: with number {}".format(drawn_numbers[i]))
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