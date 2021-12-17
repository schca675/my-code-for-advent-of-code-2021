# --- Day 16: Packet Decoder ---
import math


def get_puzzle_input(filepath):
    binary_packets = []
    with open(filepath) as f:
        for line in f:
            # get hex representation
            hex_rep = line.rstrip()
            # transform to integer
            integer_rep = int(hex_rep, 16)
            # transform to binary <with> leading zeros using
            # https://stackoverflow.com/questions/1425493/convert-hex-to-binary
            spec = '{fill}{align}{width}{type}'.format(fill='0', align='>', width=4 * len(hex_rep), type='b')
            binary_packet = format(integer_rep, spec)
            binary_packets.append(binary_packet)
    return binary_packets

class Packet:
    def __init__(self, binary_rep, is_subpacket, nr_subpackets_after_this):
        # every packet has
        self.version = int(binary_rep[0:3], 2) # first three bits
        self.type_id = int(binary_rep[3:6], 2) # next three bits
        self.literal_value = False
        self.ordinary_value = False
        self.number = 0 # only for literal
        self.subpackets = [] # only for ordinary
        self.next_packet = None
        self.is_subpacket = is_subpacket # type of subpacket: 0, no subpacket, 1: bits; 2: number of packets
        self.nr_subpackets_after_this = nr_subpackets_after_this
        self.index_pointer = 0
        if self.type_id == 4:
            # it is a literal value
            self.literal_value = True
            # then the rest is a number
            self.index_pointer = 6
            nr_continues = True
            nr_binary = ""
            while nr_continues:
                digits = binary_rep[self.index_pointer:self.index_pointer+5]
                nr_continues = digits[0] == '1'
                nr_binary += digits[1:]
                self.index_pointer += 5

            self.number = int(nr_binary, 2)
            # parse next packet
            self.parse_next_packet(binary_rep)
        else:
            # is an operator
            self.ordinary_value = True
            self.length_type_id = binary_rep[6] # bit after header + version
            self.index_pointer = 7
            if self.length_type_id == '0':
                # next 15 bits represents  total_length_of_subbits
                length = 15
                length_of_subpackets = int(binary_rep[self.index_pointer:self.index_pointer + length], 2)
                self.index_pointer += length
                subpacket_bits = binary_rep[self.index_pointer:self.index_pointer + length_of_subpackets]
                self.index_pointer += length_of_subpackets
                subpacket = Packet(subpacket_bits, 1, 0)  # will be literal values most probably
                self.subpackets.append(subpacket)
                while subpacket.next_packet is not None:
                    subpacket = subpacket.next_packet
                    self.subpackets.append(subpacket)
                # parse next packet
                self.parse_next_packet( binary_rep)
            else:
                # next 11 bits represent number that represent number of sub-packets contained
                length = 11
                nr_packets = int(binary_rep[self.index_pointer:self.index_pointer + length], 2)
                self.index_pointer += length
                subpacket = Packet(binary_rep[self.index_pointer:], 2, nr_packets-1)  # nr_packets -1 because one will be the one defined
                self.subpackets.append(subpacket)
                self.index_pointer += subpacket.index_pointer
                while subpacket.next_packet is not None:
                    subpacket = subpacket.next_packet
                    self.index_pointer += subpacket.index_pointer
                    self.subpackets.append(subpacket)
                # parse next packet

                self.parse_next_packet(binary_rep)


    def parse_next_packet(self, binary_rep):
        # depends on a lot of stuff
        # next packet starts at start_i + leading zeros making the packet a multiple of 4
        # So ex: start_i = 33 -> 34 bits ==> 2 padding zeros need to be ignored --> + 3
        # 3 = 33 % 4 + 1 (index starting at 0) + 1 (to go to next packet) = 1 + 1 + 1
        ## above only if it is not a subpacket.

        if self.is_subpacket == 0:
            # index pointer += % 4 + 1 (index starting at 0) + 1 (to go to next packet)
            self.index_pointer += (8 - self.index_pointer % 4)
            if len(binary_rep) > self.index_pointer:
                self.next_packet = Packet(binary_rep[self.index_pointer:], 0, 0)
        elif self.is_subpacket == 1:
            # number of bits passed on
            if len(binary_rep) > self.index_pointer:
                self.next_packet = Packet(binary_rep[self.index_pointer:], 1, 0)
        elif self.is_subpacket == 2:
            # number of packets passed on
            if self.nr_subpackets_after_this > 0:
                self.next_packet = Packet(binary_rep[self.index_pointer:], 2, self.nr_subpackets_after_this - 1)

def get_subpackets(packet):
    subpackets = packet.subpackets
    return subpackets

def decode_packets(binary_packet):
    all_packets = []
    starting_packet = Packet(binary_packet, 0, 0)
    packets_to_check = [starting_packet]
    while len(packets_to_check) > 0:
        current_packet = packets_to_check.pop()
        packets_to_check.extend(current_packet.subpackets)

        all_packets.append(current_packet)
        current_packet = current_packet.next_packet
    return all_packets, starting_packet


def greater_than(first,second):
    if first > second:
        return 1
    return 0

def less_than(first, second):
    if first < second:
        return 1
    return 0

def equal_to(first, second):
    if first == second:
        return 1
    return 0

def operate(a, b, operation):
    return operation(a,b)

def operate_on_list(list_a, operation):
    return operation(list_a)

def get_value(packet):
    fun_dict = {0: lambda x: sum(x),
                1: lambda x: math.prod(x),
                2: lambda x: min(x),
                3: lambda x: max(x),
                5: lambda x: greater_than(x[0],x[1]),
                6: lambda x: less_than(x[0], x[1]),
                7: lambda x: equal_to(x[0],x[1])}
    if packet.type_id == 4:
        # literal
        return packet.number
    else:
        t = packet.type_id
        values = [get_value(subpacket) for subpacket in packet.subpackets]
        value = operate_on_list(values, fun_dict[packet.type_id])
        return value

def resolve_puzzle(filepath):
    binary_packets = get_puzzle_input(filepath)
    for binary_packet in binary_packets:
        packets, starting_packet = decode_packets(binary_packet)
        value = get_value(starting_packet)
        res_list = [packet.version for packet in packets] # get version numbers
        sum_version = sum(res_list)
        print("Packet {}".format(hex(int(binary_packet, 2))))
        print("Solution: sum of version numbers is {}".format(sum_version))
        print("Solution part 2: result value: {}".format(value))

# resolve_puzzle("test_literal_packet.txt")
print("TEST")
# resolve_puzzle("test_data_operator_packet.txt")
print("PUZZLE")
resolve_puzzle("data.txt")