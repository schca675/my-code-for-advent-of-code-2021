import copy


class Spot:
    hallway = (1,11)
    doors = (3,5,7,9)
    rooms = (12, 19)

    def __init__(self, id, is_room=None, occupied_by = None, other_room = None):
        self.id = id # ==position
        self.is_room = is_room # A,B,C,D or None
        self.connected_to = set()
        self.occupied_by = occupied_by
        self.connected_to_other_room = None

    def __eq__(self, other):
        return isinstance(other, Spot) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return "{}:{}".format(self.id, self.occupied_by)

    def __repr__(self):
        return "{}:{}".format(self.id, self.occupied_by)

    def add_neighbours(self, neighbours):
        self.connected_to = self.connected_to.union(neighbours)

    def now_occupied_by(self, ampi):
        self.occupied_by = ampi


class Amphipod:
    def __init__(self,id,starting_pos, type):
        self.id = id
        self.pos = starting_pos
        self.type = type
        self.arrived = False
        self.is_in_hallway = False

    def possible_moves(self, next_end_pos):
        # if arrived --> don't move
        if self.arrived:
            return set(), False, True
        # check if optimal position is available
        pos_to_go_to = set()
        next_steps = self.pos.connected_to
        number = 1
        checked_places = {self.pos}
        while len(next_steps) > 0:
            new = set()
            while len(next_steps) > 0:
                neighbour = next_steps.pop()
                checked_places.add(neighbour)
                if neighbour.occupied_by is None:
                    if neighbour == next_end_pos:
                        return (neighbour, number), True, False
                    if Spot.rooms[0] <= neighbour.id <= Spot.rooms[1]:
                        other_room_ampi = neighbour.connected_to_other_room.occupied_by
                        check = other_room_ampi is None or other_room_ampi == self.type
                        if check:
                            # only go there if other room has fish of same type or None
                            pos_to_go_to.add((neighbour, number))

                    if neighbour.id not in Spot.doors and not self.is_in_hallway:
                        # will not move to doors and
                        # will not move if fish is in hallway (except to end position)
                        pos_to_go_to.add((neighbour, number))
                    new = new.union(neighbour.connected_to)
            next_steps = next_steps.union(new).difference(checked_places)
            number +=1
        return pos_to_go_to, False, False # set of (positions, cost) , whether or not end position could be reached

    def move(self, new_pos, next_end_pos):
        self.pos.occupied_by = None
        self.pos = new_pos
        new_pos.occupied_by = self.type
        if new_pos == next_end_pos:
            self.arrived = True
            return True
        return False

    def __eq__(self, other):
        return isinstance(other, Spot) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return "{}{}".format(self.type,self.id)

    def __repr__(self):
        return self.__str__()


class Field:
    def __init__(self, starting_pos):
        # Make field: all passable fields are numbered
        ##################################
        # 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11#
        #######12|##|14|##|16|##|18|######
              #13|##|15|##|17|##|19|
              ######################
        # which end_position_should be filled next by the fish:
        self.next_to_fill = {'A':13, 'B':15, 'C':17, 'D':19}
        self.amphipods = set()
        self.spots = {}
        # Make hallway
        for i in range(1, 12):
            fish = starting_pos[i-1]
            if fish is not None:
                self.spots[i] = Spot(id=i, is_room=False, occupied_by=fish)
                ampi = Amphipod(id=i - 12, starting_pos=self.spots[i], type=fish)
                # self.spots[i].now_occupied_by(ampi)
                self.amphipods.add(ampi)
            self.spots[i] = Spot(id=i, is_room=False)
        self.rooms = {12:'A', 13:'A',
                 14:'B', 15:'B',
                 16:'C', 17:'C',
                 18:'D', 19:'D'}
        #Make rooms
        for i in range(12,20):
            fish = starting_pos[i-1]
            if fish is not None:
                self.spots[i] = Spot(id=i, is_room=self.rooms[i], occupied_by=fish)
                ampi = Amphipod(id=i-12, starting_pos=self.spots[i], type=fish)
                # self.spots[i].now_occupied_by(ampi)
                self.amphipods.add(ampi)
            else:
                self.spots[i] = Spot(id=i, is_room=self.rooms[i])
        self.where_is_room = dict()
        # Make rooms
        for k,v in self.rooms.items():
            self.where_is_room[v] = self.where_is_room.get(v, set()).union({k})
        # Specify connecting spots
        # Hallway
        for i in range(1, 11):
            # hallway --> connected back and forth
            self.spots[i].add_neighbours({self.spots[i+1]})
            self.spots[i+1].add_neighbours({self.spots[i]})
        # Rooms
        for i in range(12, 19, 2):
            # connected to room behind:
            self.spots[i].add_neighbours({self.spots[i + 1]})
            self.spots[i + 1].add_neighbours({self.spots[i]})
            self.spots[i].connected_to_other_room = self.spots[i + 1]
            self.spots[i+1].connected_to_other_room = self.spots[i]
            # connected to hallway:
            self.spots[i].add_neighbours({self.spots[i - 9]})
            self.spots[i - 9].add_neighbours({self.spots[i]})

        # Movement cost per fish
        self.movement_cost = {'A':1, 'B':10, 'C':100, 'D':1000}

    def __str__(self):
        ##################################
        # 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11#
        #######12|##|14|##|16|##|18|######
              #13|##|15|##|17|##|19|
              ######################
        # ---> ".. . . . . . . . . ABABCDCD"
        return "".join([self.spots[i].occupied_by for i in range(1, 20)])

    def get_current_pos(self):
        l = []
        for i in range(1, 20):
            l.append(self.spots[i].occupied_by)
        return l

    def __eq__(self, other):
        return isinstance(other, Field) and self.__hash__() == other.__hash__()

    def __hash__(self):
        s = ""
        for i in range(1, 20):
            s += str(self.spots[i].occupied_by)
        return hash(s)


prev_fields = dict()

def get_solution(field):
    energy_level = 0
    amphipods_arrives = set() # at 8 we are done
    end_reached = False
    while len(amphipods_arrives) < 8:
        possible_moves = {}
        for amphipod in field.amphipods.difference(amphipods_arrives):
            moves, end_reached, arrived = amphipod.possible_moves(field.next_to_fill[amphipod.type])
            if arrived:
                amphipods_arrives.add(amphipod)
            if end_reached:
                amphipod.move(moves[0], field.next_to_fill[amphipod.type])
                energy_level += moves[1]*field.movement_cost[amphipod.type]
                field.next_to_fill[amphipod.type] += 1 # if both amphipods arrived, they won't move so whatever
                amphipods_arrives += 1
                break
            if len(moves) > 0:
                possible_moves[amphipod] = moves
        if end_reached:
            continue
        # not solvable?
        if len(possible_moves) == 0:
            return -1

        # there are moves that are not end moves: finish recursively
        prev_energy_level = 0
        for ampi, moves in possible_moves.items():
            for move in moves:
                field_copy = Field(field.get_current_pos())
                ampi.move(move[0], field.next_to_fill[ampi.type])
                # Get best energy level from the new field
                if field in prev_fields:
                    new_energy_level = prev_fields[field]
                else:
                    new_energy_level = move[1]*field.movement_cost[ampi.type]
                    new_costs = get_solution(field) # needs to be added to current one
                if 0 < new_costs and (new_energy_level + new_costs < prev_energy_level or prev_energy_level == 0):
                    prev_energy_level = new_energy_level + new_costs
                field = field_copy
        energy_level += prev_energy_level
        break
    # only arrive here if solution is found
    prev_fields[field] = energy_level
    return energy_level



def get_solution_of_puzzle(field):
    energy_level = get_solution(field)
    return energy_level


def get_puzzle_input_hardcoded(data=True):
    # Make field: all passable fields are numbered
    ##################################
    # 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11#
    #######12|##|14|##|16|##|18|######
          #13|##|15|##|17|##|19|
          ######################

    # Starting positions: Test
    #############
    #...........#
    ###B#C#B#D###
      #A#D#C#A#
      #########
    start_string = "BACDBCDA"
    # Data:
    #############
    #...........#
    ###C#A#B#D###
      #B#A#D#C#
      #########
    if data:
        start_string = "CBAABDDC"
    start_pos = [start_string[i - 12] if i>=12 else None for i in range(1, 20)]
    # Make field
    return Field(start_pos)

def resolve_puzzle(usedata=False):
     field = get_puzzle_input_hardcoded(usedata)
     lowest_energy = get_solution_of_puzzle(field)
     print("Lowest energy: {}".format(lowest_energy))

print("Part 1")
resolve_puzzle()
resolve_puzzle(True)

print( "Part 2")
resolve_puzzle()
resolve_puzzle(True)