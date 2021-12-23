
class Spot:
    def __init__(self, id, is_room=None, occupied_by = None):
        self.id = id # ==position
        self.is_room = is_room # A,B,C,D or None
        self.connected_to = set()
        self.occupied_by = occupied_by

    def __eq__(self, other):
        return isinstance(other, Spot) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return "{}:{}".format(self.id, self.occupied_by)

    def add_neighbours(self, neighbours):
        self.connected_to.union(neighbours)

class Field:
    def __init__(self, starting_pos):
        # Make field: all passable fields are numbered
        ##################################
        # 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11#
        #######12|##|14|##|16|##|18|######
              #13|##|15|##|17|##|19|
              ######################
        self.spots = {}
        for i in range(1, 12):
            self.spots[i] = Spot(id=i, is_room=False)
        self.rooms = {12:'A', 13:'A',
                 14:'B', 15:'B',
                 16:'C', 17:'C',
                 18:'D', 19:'D'}
        for i in range(12,20):
            self.spots[i] = Spot(id=i, is_room=self.rooms[i], occupied_by=starting_pos[i-12])
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
        for i in range(12, 20, 2):
            # connected to door behind:
            self.spots[i].add_neighbours({self.spots[i + 1]})
            self.spots[i + 1].add_neighbours({self.spots[i]})
            # connected to hallway:
            self.spots[i].add_neighbours({self.spots[i - 9]})
            self.spots[i - 9].add_neighbours({self.spots[i]})

        # which end_position_should be filled next by the fish:
        self.next_to_fill = {13:'A', 15:'B', 17:'C', 19:'D'}

        # Movement cost per fish
        self.movement_cost = {'A':1, 'B':10, 'C':100, 'D':1000}

    def get_solution(self):
        return 0


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

    # Make field
    field = Field(start_string)
    return field


def resolve_puzzle(usedata=False):
     field = get_puzzle_input_hardcoded(usedata)
     lowest_energy = field.get_solution()

print("Part 1")
resolve_puzzle()
resolve_puzzle(True)

print( "Part 2")
resolve_puzzle()
resolve_puzzle(True)