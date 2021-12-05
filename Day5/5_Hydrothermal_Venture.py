### PUZZLE Day 5: Hydrothermal Venture

class Line:
    def __init__(self, start_point, end_point):
        # assert: x1 <> x2 so it is not vertical
        self.x1 = start_point[0] # (x_1, y_1)
        self.y1 = start_point[1]
        self.x2 = end_point[0]     # (x_2, y_2)
        self.y2 = end_point[1]

    def get_all_points_in_line(self):
        return []

class Linear_Line(Line):
    def __init__(self, start_point, end_point):
        # assert: x1 <> x2 so it is not vertical
        super().__init__(start_point, end_point)
        # Formula: y = m x + b
        self.slope_m = (self.y2 - self.y1) / (self.x2 - self.x1)
        # y-intercept b:
        self.b = self.y1 - self.slope_m * self.x1

    def get_all_points_in_line(self):
        # get all x's to consider:
        inputs_x = range(self.x2, self.x1 + 1)
        if self.x1 < self.x2:
            inputs_x = range(self.x1, self.x2 + 1)
        return [(x, int(self.slope_m * x + self.b)) for x in inputs_x]


class Vertical_Line(Line):
    def __init__(self, start_point, end_point):
        # assert: x1 == x2 so is not vertical
        super().__init__(start_point, end_point)
        # Formula: x = x1 for all y

    def get_all_points_in_line(self):
        # get all y's to consider:
        inputs_y = range(self.y1, self.y2 + 1)
        if self.y2 < self.y1:
            inputs_y = range(self.y2, self.y1 + 1)
        return [(self.x1, y) for y in inputs_y]


def get_only_horizontal_and_vertical_lines(line):
    pass


def get_puzzle_input(filepath, only_vert_hor_lines):
    lines = []
    min_x = 1000000000
    max_x = 0
    min_y = 1000000000
    max_y = 0
    with open(filepath) as f:
        # File structure
        # 0,9 -> 5,9
        # 8,0 -> 0,8
        for line in f:
            # Get end points
            line_contents = line.rstrip().split()
            start_point_str = line_contents[0].split(',')
            end_point_str = line_contents[2].split(',')
            start_point = [int(x) for x in start_point_str]
            end_point = [int(x) for x in end_point_str]
            # Get line: first add vertical, then horizontal line and all
            # other lines only if so specified in input boolean
            if start_point[0] == end_point[0]:
                # if the x coordinates are equal : vertical line
                lines.append(Vertical_Line(start_point, end_point))
            elif start_point[1] == end_point[1]:
                lines.append(Linear_Line(start_point, end_point))
            elif not only_vert_hor_lines:
                lines.append(Linear_Line(start_point, end_point))
            # Update grid size
            min_y = min(min_y, start_point[1], end_point[1])
            min_x = min(min_x, start_point[0], end_point[0])
            max_x = max(max_x, start_point[0], end_point[0])
            max_y = max(max_y, start_point[1], end_point[1])
    return lines, min_x, max_x, min_y, max_y


def draw_lines(lines):
    points = {} # dictionary how often points are drawn
    for line in lines:
        line_points = line.get_all_points_in_line()
        for point in line_points:
            count = points.get(point, 0)
            points[point] = count + 1
    return points


def get_count_of_points_drawn_more_than_twice(points):
    return sum(count >= 2 for count in points.values())


def resolve_puzzle_5_part1(filepath):
    # Get puzzle input: Lines and sizes: ONLY horizontal
    lines, min_x, max_x, min_y, max_y = get_puzzle_input(filepath, True)
    # Draw the lines: how many times are individual points drawn
    points = draw_lines(lines)
    count = get_count_of_points_drawn_more_than_twice(points)
    print("PUZZLE solution: {} points drawn at least twice".format(count))

print("TEST")
resolve_puzzle_5_part1("test_data.txt")
print("PUZZLE")
resolve_puzzle_5_part1("data.txt")

def resolve_puzzle_5_part2(filepath):
    # Get puzzle input: Lines and sizes: ONLY horizontal
    lines, min_x, max_x, min_y, max_y = get_puzzle_input(filepath, False)
    # Draw the lines: how many times are individual points drawn
    points = draw_lines(lines)
    count = get_count_of_points_drawn_more_than_twice(points)
    print("PUZZLE solution: {} points drawn at least twice".format(count))

print("TEST")
resolve_puzzle_5_part2("test_data.txt")
print("PUZZLE")
resolve_puzzle_5_part2("data.txt")