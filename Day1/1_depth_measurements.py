#### PUZZLE 1 - 01/12/2021 SONAR SWEEP
# https://adventofcode.com/2021/day/1


def get_number_of_increases(list_measurements):
    prev = list_measurements[0]
    count_increases = 0
    for i in range(1, len(list_measurements)):
        if list_measurements[i] > prev:
            count_increases+=1
        prev = list_measurements[i]
    return count_increases


def get_list_of_numbers_from_txt_file(filepath):
    res = []
    with open(filepath) as f:
        for line in f:
            res.append(int(line))
    return res

## Test case
filepath_test = "1_test_data_measurements"
meas_list_test = get_list_of_numbers_from_txt_file(filepath_test)
print("1 TEST: Number of increases: ", get_number_of_increases(meas_list_test))

## Actual data measurements
filepath = "1_data_measurements"
meas_list = get_list_of_numbers_from_txt_file(filepath)
print("1 PUZZLE: Number of increases: ", get_number_of_increases(meas_list))


#### PUZZLE 2 in times of 3

def get_numbers_of_increases_in_time_three(list_measurements):
    count_increases = 0
    last_sum = 10000000
    for i in range(0, len(list_measurements)):
        new_sum = sum(list_measurements[i:i+3])
        if new_sum > last_sum:
            count_increases+=1
        last_sum = new_sum
    return count_increases


print("2 TEST: Number of increases per three ", get_numbers_of_increases_in_time_three(meas_list_test))

print("2 PUZZLE: Number of increases per three ", get_numbers_of_increases_in_time_three(meas_list))