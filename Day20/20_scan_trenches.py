# --- Day 20: Trench Map ---

def get_puzzle_input(filepath):
    field = []
    image_alg = ""
    first_line = True
    with open(filepath) as f:
        for line in f:
            if first_line:
                image_alg = line.rstrip()
                first_line = False
                continue
            if len(line) > 1:
                # FIeld
                field.append(line.rstrip())
    return image_alg, field


def process_image(field, image_alg, zero):
    # zero: what bit is currently at the points outside
    # either 9x'.' or 9x'#'
    processed_field = []
    max_i = len(field) - 1
    ## FIRST row: no upper row exists
    # First col: no left exist: binary number: 000(top) 0cx(middle) 0xx(bottom) "0000{}0{}"
    first_c_index = int("{}{}{}{}".format(zero*4, field[0][0:2], zero, field[1][0:2]), 2)
    first_row = image_alg[first_c_index]
    for j in range(1, len(field[0])-1):
        b_index = int("{}{}{}".format(zero*3, field[0][j-1:j+2], field[1][j-1:j+2]), 2) #"000{}{}"
        first_row += image_alg[b_index]
    # Last col: no right exists
    last_c_index = int("{}{}{}{}{}".format(zero*3, field[0][-2:], zero,  field[1][-2:], zero ), 2) #"000{}0{}0"
    first_row += image_alg[last_c_index]
    processed_field.append(first_row)

    ## ALL rows but last
    for i in range(1, max_i):
        # First char
        first_c_index = int("{}{}{}{}{}{}".format(zero, field[i-1][0:2], zero, field[i][0:2], zero, field[i+1][0:2]), 2) #"0{}0{}0{}"
        row_i = image_alg[first_c_index]
        # All other char but last
        for j in range(1, len(field[0])-1):
            # all surrounding pixels exist
            # get upper row
            up = field[i-1][j-1:j+2]
            # get middle row
            middle = field[i][j-1:j+2]
            # get bottom row
            bottom = field[i+1][j-1:j+2]
            # make binary number
            b_index = int("{}{}{}".format(up, middle, bottom), 2)
            # get pixel
            row_i += image_alg[b_index]
        # Last char
        last_c_index = int("{}{}{}{}{}{}".format(field[i-1][-2:], zero, field[i][-2:], zero, field[i+1][-2:], zero), 2) #"{}0{}0{}0"
        row_i += image_alg[last_c_index]
        # Add processed row to field
        processed_field.append(row_i)

    # LAST row
    first_c_index = int("{}{}{}{}{}".format(zero, field[max_i-1][0:2], zero, field[max_i][0:2], zero*3), 2) #"0{}0{}000"
    last_row = image_alg[first_c_index]
    for j in range(1, len(field[0])-1):
        b_index = int("{}{}{}".format(field[max_i-1][j-1:j+2], field[max_i][j-1:j+2], zero*3), 2) #"{}{}000"
        last_row += image_alg[b_index]
    # Last col: no right exists
    last_c_index = int("{}{}{}{}".format(field[max_i-1][-2:], zero, field[max_i][-2:], zero*4), 2) #"{}0{}0000"
    last_row += image_alg[last_c_index]
    processed_field.append(last_row)

    # update zero
    zero_index = int('{}'.format(zero)*9, 2)
    zero = image_alg[zero_index]
    return processed_field, zero

def transform_char_to_0_1s(field):
    new_field = []
    for row in field:
        new_field.append("".join(['0' if c == '.' else '1' for c in row]))
    return new_field

def transform_0_1_to_chars(field):
    new_field = []
    for row in field:
        new_field.append(''.join(['.' if c == '0' else '#' for c in row]))
    return new_field


def extend_field(field, how_often):
    # extend the surrounding of the field by how_often + 1 corners, since field is growing
    # (infinite field and how_often circles around it become relevant)

    # add how_often + 1 rows in front
    for i in range(0, how_often + 1):
        field.insert(0, '.'*len(field[0]))
    # add how_often + 1 rows behind
    for i in range(0, how_often + 1):
        field.append('.'*len(field[0]))
    # add how_often + 1 to the left and right
    for i in range(0, len(field)):
        field[i] = '.'*(how_often + 1) + field[i] + '.'*(how_often + 1)




def apply_image_processing(field, image_alg, how_often):
    extend_field(field, how_often)
    final_image = transform_char_to_0_1s(field)
    image_alg_bin = transform_char_to_0_1s(image_alg)
    zero = '0'
    for i in range(0, how_often):
        final_image, zero = process_image(final_image, image_alg_bin, zero)
    return final_image, transform_0_1_to_chars(final_image)


def count_light_pixels(bin_field):
    light_count = 0
    for row in bin_field:
        light_count += sum([int(c) for c in row])
    return light_count


def resolve_puzzle(filepath, times):
    image_alg, field = get_puzzle_input(filepath)
    new_field_bin, new_field = apply_image_processing(field, image_alg, times)
    lights = count_light_pixels(new_field_bin)
    print("{}\nPUZZLE SOLUTION: {} light pixels".format(filepath, lights))

print("Part 1")
resolve_puzzle("test_data.txt", 2)
resolve_puzzle("data.txt", 2)

print( "Part 2")
resolve_puzzle("test_data.txt", 50)
resolve_puzzle("data.txt", 50)