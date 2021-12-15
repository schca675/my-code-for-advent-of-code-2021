import copy
import time


def get_puzzle_input(filepath):
    field = []
    with open(filepath) as f:
        for line in f:
            l = [int(x) for x in line.rstrip()]
            field.append(l)
    return field


def dynamical_programming(field):
    # find lowest cost/risk to start from <<start>> and end at every position on field:
    risk_matrix = [[0]] # starting cost: not added
    start_i = 0
    max_i = len(field)-1
    start_j = 0
    max_j = len(field[0]) -1
    # build up leftmost column, from top to bottom
    for i in range(start_i + 1, max_i + 1):
        # shortest path is going up all the way, so risk = current field plus previous
        risk_matrix.append([risk_matrix[i-1][start_j] + field[i][start_j]])
    # build up topmost row
    for j in range(start_j + 1, max_j + 1):
        # min risk is only coming from left
        risk_matrix[start_i].append(risk_matrix[start_i][j-1]+ field[start_i][j])
    # build up the rest: row by row from top to bottom
    for i in range(start_i+1, max_i + 1):
        # fill out cells from left to right, startindex already filled.
        for j in range(start_j+1, max_j + 1):
            # min risk is the minimum of coming from above or from the left
            min_risk = min(risk_matrix[i][j-1], risk_matrix[i-1][j]) + field[i][j]
            risk_matrix[i].append(min_risk)
    return risk_matrix


def update_risk_matrix_with_down_left(field, risk_matrix):
    updated = False
    # find lowest cost/risk to start from <<start>> and end at every position on field:
    start_i = 0
    max_i = len(field)-1
    start_j = 0
    max_j = len(field[0]) -1
    # check leftmost column --> also coming from right an option
    for i in range(start_i + 1, max_i + 1):
        min_risk = min(risk_matrix[i-1][start_j], risk_matrix[i][start_j+1]) + field[i][start_j]
        # check if improved:
        if min_risk < risk_matrix[i][start_j]:
            risk_matrix[i][start_j] = min_risk
            updated = True
    # build up topmost row
    for j in range(start_j + 1, max_j + 1):
        # min risk is only coming from left or down
        min_risk = min(risk_matrix[start_i][j-1], risk_matrix[start_i+1][j]) + field[start_i][j]
        # check if improved: then restart evaluation
        if min_risk < risk_matrix[start_i][j]:
            risk_matrix[start_i][j] = min_risk
            updated = True

    # build up the rest: row by row from top to bottom, except outmost column and row
    for i in range(start_i+1, max_i):
        # fill out cells from left to right, startindex already filled.
        for j in range(start_j+1, max_j):
            # min risk is the minimum of coming from above, below, right or from the left (not defined in this order)
            min_risk = min(risk_matrix[i][j-1], risk_matrix[i-1][j], risk_matrix[i][j+1], risk_matrix[i+1][j]) + field[i][j]
            if min_risk < risk_matrix[i][j]:
                risk_matrix[i][j] = min_risk
                updated =  True

    # Check rightmost column
    for i in range(start_i + 1, max_i + 1):
        # coming from left or up
        min_risk = min(risk_matrix[i-1][max_j], risk_matrix[i][max_j-1]) + field[i][max_j]
        # check if improved:
        if min_risk < risk_matrix[i][max_j]:
            risk_matrix[i][max_j] = min_risk
            updated =  True
    # Check bottommost row
    for j in range(start_j + 1, max_j + 1):
        # min risk is only coming from left or down
        min_risk = min(risk_matrix[max_i][j-1], risk_matrix[max_i-1][j]) + field[max_i][j]
        # check if improved: then restart evaluation
        if min_risk < risk_matrix[max_i][j]:
            risk_matrix[max_i][j] = min_risk
            updated =  True
    return updated


def make_full_field(field):
    new_field = []
    # make 5 copies of field
    rotation_instances = {0:copy.deepcopy(field)}
    for field_i in range(1, 9):
        rotated_field = []
        for row in field:
            rotated_field.append([x+field_i if x+field_i <= 9 else x+field_i-9 for x in row])
        rotation_instances[field_i] = rotated_field
    # append them to the original field in the following manner:
    # 0 1 2 3 4 # number is rotated by x
    # 1 2 3 4 5
    # 2 3 4 5 6
    # 3 4 5 6 7
    # 4 5 6 7 8
    # Do first column separate: need to add rows to field
    for field_i in range(0, 5):
        rot_field = rotation_instances[field_i]
        # add field to existing field
        new_field.extend(rot_field)
    # Do the rest of the field
    for field_i in range(0, 5):
        for j in range(field_i+1, field_i+5):
            rot_field = rotation_instances[j]
            for within_field_i in range(0, len(rot_field)):
                # extend every row with the row from the rotated field
                new_field[field_i*len(rot_field) + within_field_i].extend(rot_field[within_field_i])
    return new_field

def resolve_puzzle_dynamic_prog(filepath, is_part_2, update_grid_at_most_times):
    field = get_puzzle_input(filepath)
    if is_part_2:
        field = make_full_field(field)
    risk_matrix = dynamical_programming(field)
    needs_updating = True
    count = 0 # try after 1000 iterations
    while needs_updating and count < update_grid_at_most_times:
        # after updating it 10 times, right answer is found according to site.
        needs_updating = update_risk_matrix_with_down_left(field, risk_matrix)
        count += 1
    print(risk_matrix)
    print("To reach end, risk level is {}".format(risk_matrix[len(field)-1][len(field[0])-1]))

print("TEST")
#############################
## Dynamical programming   ##
#############################
# Initital dynamic programming model greedily assumes going right or down are best option.
## For test data this is correct
## For actual data: not correct
# --> so dynamic model is updated in new function where also going up and going right is considered
# Algorithm risks needing a long time to terminate, so we can add a maximum number on how often it is updated
# Basically, every update: new shortcut is found based on the update of a previous shortcut
# For this puzzle: after 10 iterations the correct result is found (~5-6s).
# Could add a stopping condition: if the shortest path has not changed in x updates --> we assume it to be correct.
## Other solution: implement dijkstra
start = time.time()
resolve_puzzle_dynamic_prog("test_data.txt", True, 1)
print("Time: {}".format(time.time()-start)) #0.015744447708129883
start = time.time()
resolve_puzzle_dynamic_prog("data.txt", True, 10)
print("Time: {}".format(time.time()-start)) # 5.75269079208374
