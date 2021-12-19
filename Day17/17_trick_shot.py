# --- Day 17: Trick Shot ---
import math
import time


def get_puzzle_input(filepath):
    with open(filepath) as f:
        for line in f:
            # target area: x=269..292, y =-68..-44
            parts = line.rstrip().replace(',', '').split()
            [x1, x2] = parts[2][2:].split("..")
            [y1, y2] = parts[3][2:].split("..")
            return int(x1), int(x2), int(y1), int(y2)

class Position:
    def __init__(self, vx, vy):
        self.x = 0
        self.y = 0
        self.max_y = 0
        self.vx = vx
        self.vy = vy
        self.steps_to_start_searching_y = 10000

    # def get_position_at_step(self, t):
    #     if self.vx >= 0:
    #         x = max(0, self.vx - t) + self.x
    #     else:
    #         x = min(0, self.vx + t) + self.x
    #     y = min(0, self.vy + t) + self.y
    #     return x, y

    def __eq__(self, other):
        if type(other) == type([1,2]):
            return other[0] == self.vx and other[1] == self.vy
        return self == other

    def __gt__(self, other):
        return self.x > other.x

    def __lt__(self, other):
        return self.x < other.x

    def get_position_at_step(self, t):
        if self.vx >= 0:
            if self.vx+1 <= t:
                # there is no horizontal speed left anymore
                x = 0.5* (self.vx*self.vx + self.vx)
            else:
                # t * self.vy - (0.5 * (t - 1) * t)  # TODO
                x = t*self.vx - 0.5*(t*t - t)
                # vx_t == 0 <=> t >= vx+1
        else:
            if self.vx+1 <= t:
                vx_abs = abs(self.vx)
                # there is no horizontal speed left anymore
                x = vx_abs * self.vx + 0.5* (vx_abs * vx_abs + vx_abs)
            else:
                x = t * self.vx + 0.5 * (t * t + t)
        y = self.get_y_at_step(t)
        return x, y

    def get_y_at_step(self, t):
        # vy_t = vy - t
        # y_t = y_t-1 + vy_t = y_t-1 + (vy-t)
        #     = vy-t + vy-(t-1) + vy-(t-2) + ... + vy-0
        #     = (t+1) * vy - sum_0^t = (t+1) vy - t(t+1)/2
        # y_1 = 0 + vy
        # y_2 = vy + vy-1 = 2*vy - 1
        # y_3 = 2vy -1 + vy - 2 = 3 vy - sum_1^t-1
        # y_t =
        return t* self.vy -(0.5 * (t-1) * t) #TODO

    def __str__(self):
        return "{},{} {} steps".format(str(self.vx), str(self.vy), self.steps_to_start_searching_y)

    def check_if_hitting_target(self, x1, x2, y1, y2, maxsteps=1000):
        ### assuming positive distances
        # Otherwise make: if max(x1, 0) > x > min(x2, 0): for first inequation

        # if at t steps: y is under y1 but left of x1:  will not hit it anymore
        #    |        |
        #  x1|________|x2       .0
        #   .
        #   |
        # At vx steps --> no more horizontal movement left
        ## if we still havent reached target in a horizontal level --> will not hit it
        x, y = self.get_position_at_step(self.vx)
        if x < x1:
            return False
        ## if the y position once we only move straight down is above the bottom y line
        #   y2_________
        #    |    .   |
        #  y1|____|___|
        #         |
        #         |
        if x1 <= x <= x2:
            # Hits target only if movement stops above the target area, but could miss while going down
            if y >= min(y1, y2):
                self.steps_to_start_searching_y = self.vx
                # check every step after that
                t = self.vx
                while y >= y1:
                    y = self.get_y_at_step(t)
                    if y2 >= y >= y1:
                        return True
                    t += 1
                return False

        # Else: check whether the steps before hit the target area at a integer step
        t = self.vx - 1
        wx,wy = self.get_position_at_step(max(t - 10, 0))
        while wx > x2:
            t -=10
            wx,wy = self.get_position_at_step(max(t - 10, 0))

        while x >= x1:
            x, y = self.get_position_at_step(t)
            if x1 <= x <= x2 and y2 >= y >= y1:
                return True
            t -= 1

        #### has some mistake in it...
        # next_t = round(self.vx/2)
        # prev_t = self.vx
        # while next_t != prev_t:
        #     prev_round = prev_t
        #     prev_t = next_t
        #     # new target: trunc(vx/2)
        #     new_x, new_y = self.get_position_at_step(next_t)
        #     # as long
        #     if x1 <= new_x <=x2 and y1 <= new_y <= y2:
        #         self.steps_to_start_searching_y = next_t
        #         return True
        #     elif new_x < x1:
        #         if new_y < y1:
        #             # left of target but still below
        #             return False
        #         else:
        #             # go to right, add half distance
        #             next_t += round(0.5*(prev_round - next_t))
        #     elif new_x <= x2 and new_y > y2:
        #         # go to right (steps forwards)
        #         next_t += round(0.5 * (prev_round - next_t))
        #     else:
        #         # now one is either still to the right of target area or under it, so to have a chance to hit it:
        #         # must be on an earlier step
        #         if prev_round > next_t:
        #             # now reference point is 0
        #             next_t = round(next_t/2)
        #         else:
        #             next_t -= round(0.5*(next_t - prev_round))
        return False

    def check_highest_y(self, left_t, right_t, t):
        y = self.get_y_at_step(t)
        # check step one to left and one to right
        next_y = self.get_y_at_step(t+1)
        if next_y > y:
            # y+1/ \
            # y /   \
            #        \
            # still going up -> take step to right
            new_t = t + math.floor(0.5*(right_t - t))
            return self.check_highest_y(left_t=t, right_t=right_t, t=new_t)
        prev_y = self.get_y_at_step(t-1)
        if prev_y > y:
            #    / \  y-1
            #   /   \  y
            #        \
            # going down --> take step to the left
            new_t = t - math.floor(0.5*(t - left_t))
            return self.check_highest_y(left_t=left_t, right_t=t, t=new_t)
        # if neither are true: y >= next and prev y ---> highest y achieved
        return y

    def get_highest_y(self):
        if self.vy <= 0:
            # if vy is negative highest point is at start
            return 0
        # return self.check_highest_y(0, self.target_hit_after_steps, self.target_hit_after_steps)
        return self.vy*(self.vy+1)/2

def get_highest_trick_shot(x1, x2, y1, y2):
    hitting_shots = []
    max_y_at_hitting_shots = []
    # try different vx and vy
    for vx in range(math.floor(math.sqrt(x1)), x2+1):
        for vy in range(y1, 10*x2): #969
        # for vy in range(-100, 5000): 969
            pos = Position(vx, vy)
            hits = pos.check_if_hitting_target(x1, x2, y1, y2)
            if hits:
                hitting_shots.append(pos)
                max_y_at_hitting_shots.append(pos.get_highest_y())
    return max(max_y_at_hitting_shots), len(hitting_shots), hitting_shots


def resolve_puzzle_part1(filepath):
    x1, x2, y1, y2 = get_puzzle_input(filepath)
    y, count, hitting_shots = get_highest_trick_shot(x1, x2, y1, y2)
    print("HIghest position is: {}, Count: {}".format(y, count))

    with open("hitting_shots.txt") as f:
        for line in f:
            hits = line.rstrip().split()
            int_hits = []
            for hit in hits:
                [x, y] = hit.split(',')
                int_hits.append([int(x), int(y)])
    pass
print("TEST")
start = time.time()
resolve_puzzle_part1("test_data.txt")
print("Time: {}".format(time.time()-start))
print("PUZZLE")
start = time.time()
resolve_puzzle_part1("data.txt")
print("Time: {}".format(time.time()-start))
