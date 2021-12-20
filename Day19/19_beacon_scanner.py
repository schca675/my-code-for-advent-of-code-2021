# --- Day 19: Beacon Scanner ---

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