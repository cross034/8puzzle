import copy
from colorama import init, Fore, Style
init()


class Instance:
    def __init__(self, conf, prev_instance=None):
        self.conf = conf
        if prev_instance:
            self.prev_instance = prev_instance
            self.g = prev_instance.g+1
        else:
            self.g = 0
            self.prev_instance = None
        self.h = self.get_heuristic()
        self.f = self.g + self.h

    def __str__(self):
        to_print = "\n"
        for r in self.conf:
            to_print += "| "
            for value in r:
                if value == 0:
                    # to_print += colored(str(value), "red") + " "
                    to_print += Fore.RED + Style.BRIGHT + str(value) + Style.RESET_ALL + " "
                else:
                    to_print += str(value) + " "
            to_print += "|\n"
        return to_print[:-1]

    def __eq__(self, other):
        return self.conf == other.conf

    def is_goal(self):
        global goal_conf
        return self.conf == goal_conf

    def get_blank_pos(self, conf=None):
        if not conf:
            conf = self.conf
        for r, row in enumerate(conf):
            for c, value in enumerate(row):
                if value == 0:
                    return r, c

    def swap(self, pos_r, pos_c):
        blank_row, blank_col = self.get_blank_pos()
        temp_conf = copy.deepcopy(self.conf)
        temp_conf[blank_row][blank_col] = self.conf[pos_r][pos_c]
        temp_conf[pos_r][pos_c] = self.conf[blank_row][blank_col]
        temp_instance = Instance(temp_conf, prev_instance=self)
        return temp_instance

    def get_heuristic(self):
        global goal_conf
        h = 0
        for r, row in enumerate(goal_conf):
            for c, value in enumerate(row):
                if value != self.conf[r][c]:
                    h += 1
        if self.get_blank_pos() != self.get_blank_pos(goal_conf):
            h -= 1
        return h

    def get_possible_moves(self):
        blank_row, blank_col = self.get_blank_pos()
        all_moves = [[blank_row+r, blank_col+c] for r, c in [[0, 1], [0, -1], [1, 0], [-1, 0]]]
        possible_moves = [move for move in all_moves if -1 < move[0] < 3 and -1 < move[1] < 3]
        return possible_moves

    def get_possible_next_instances(self):
        possible_moves = self.get_possible_moves()
        instances = [self.swap(*move) for move in possible_moves]
        return instances

    def print_trace(self):
        previous_instances = [self]
        current_instance = self
        while current_instance.prev_instance is not None:
            previous_instances.append(current_instance.prev_instance)
            current_instance = current_instance.prev_instance
        previous_instances.reverse()
        for instance in previous_instances:
            print(instance)
            print("g : " + str(instance.g))
            print("h : " + str(instance.h))
            print("f : " + str(instance.f))


init_conf = [[2, 3, 6],
             [1, 0, 5],
             [4, 7, 8]]
goal_conf = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 0]]

open_list = []
closed_list = []
init_instance = Instance(init_conf)
open_list.append(init_instance)


def search_in_list(input_list, element):
    for e in input_list:
        if e == element:
            return True
    return False


while len(open_list) > 0:
    instance = min(open_list, key=lambda i: i.f)
    if instance.is_goal():
        print("Done!!!")
        instance.print_trace()
        break
    open_list.remove(instance)
    closed_list.append(instance)
    next_instances = instance.get_possible_next_instances()
    new_instances = [instance for instance in next_instances if not search_in_list(closed_list, instance)]
    open_list.extend(next_instances)
    
    # FOR DEBUGGING
    #
    # print("Closed :")
    # for e in closed_list:
    #     print(e)
    # print("new_instances :")
    # for e in new_instances:
    #     print(e)
    # input()
    
    if len(open_list) == 0:
        print("Bummer!!!")
