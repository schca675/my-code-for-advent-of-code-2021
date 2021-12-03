import pandas as pd

def get_panda_from_txt(filepath):
    char_list = []
    byte_list = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.rstrip()
            char_list.append(list(line))
            binary = int(line,2)
            byte_list.append(bin(binary))
    df = pd.DataFrame(char_list, columns=range(0, len(char_list[0])))
    return df, byte_list

def get_least_gamma_and_epsilon_rate(df):
    gamma = "" # most common bit
    epsilon = "" # least common bit
    # column names defined as
    for i in range(0, df.shape[1]):
        counts = df[i].value_counts()
        if counts["0"] > counts["1"]:
            gamma+="0"
            epsilon+="1"
        else:
            gamma += "1"
            epsilon += "0"
    return gamma, epsilon, int(gamma, 2), int(epsilon, 2)

def resolve_puzzle_part1(filepath):
    df, byte_list = get_panda_from_txt(filepath)
    gamma_bin, epsilon_bin, gamma, epsilon = get_least_gamma_and_epsilon_rate(df)
    print("Gamma {} ({}), Epsilon: {} ({})".format(gamma, gamma_bin, epsilon, epsilon_bin))
    print("Solution: Power consumption {}".format(epsilon*gamma))

# print("TEST")
# resolve_puzzle_part1("test_data.txt")
# print("PUZZLE")
# resolve_puzzle_part1("binary_data.txt")
#


def get_oxygen_rating(df):
    df_oxy = df
    i = 0
    while df_oxy.shape[0] > 1 and i < df_oxy.shape[1]:
        counts = df_oxy[i].value_counts()
        value = "0" if counts["0"] > counts["1"] else "1"
        df_oxy = df_oxy[df_oxy[i] == value]
        i +=1
    oxygen = ""
    for char in df_oxy.iloc[0].values:
        oxygen +=char
    return int(oxygen, 2), oxygen

def get_co2_scrubber_rating(df):
    df_co2 = df
    i = 0
    while df_co2.shape[0] > 1 and i < df_co2.shape[1]:
        counts = df_co2[i].value_counts()
        value = "0" if counts["0"] <= counts["1"] else "1"
        df_co2 = df_co2[df_co2[i] == value]
        i += 1
    co2 = ""
    for char in df_co2.iloc[0].values:
        co2 +=char
    return int(co2, 2), co2



def resolve_puzzle_part2(filepath):
    df, byte_list = get_panda_from_txt(filepath)
    oxygen, oxygen_bin = get_oxygen_rating(df)
    co2_scrubber, co2_scrubber_bin = get_co2_scrubber_rating(df)
    print("Oxygen: {} ({}), Co2: {} ({})".format(oxygen, oxygen_bin, co2_scrubber, co2_scrubber_bin))
    print("Solution: Life Support {}".format(oxygen*co2_scrubber))

print("TEST")
resolve_puzzle_part2("test_data.txt")
print("PUZZLE")
resolve_puzzle_part2("binary_data.txt")
# resolve_puzzle_part2("binary_data.txt")
