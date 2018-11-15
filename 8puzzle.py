import copy


class Instance:
    def __init__(self, step=0, state=None, prev_instance=None, prev_move=None):
        global count
        count += 1
        self.distance = 0
        self.next_states = []
        self.step = step
        self.prev_instance = prev_instance
        self.prev_move = prev_move
        if state:
            self.state = state
            self.compute_distance_disp()
        else:
            self.state = []

    def get_input(self):
        print("Enter the initial state")
        for i in range(3):
            row = []
            for j in range(3):
                element = int(input())
                row.append(element)
            self.state.append(row)
        self.compute_distance_disp()

    def print_state(self, label=""):
        tbp = label+"\n"
        for r in self.state:
            for e in r:
                if not e == 0:
                    tbp = tbp + str(e) + "\t"
                else:
                    tbp = tbp + " \t"
            tbp = tbp + "\n\n"
        print(tbp)

    def get_position(self, element, state):
        if state:
            for rn, r in enumerate(state):
                for cn, e in enumerate(r):
                    if e == element:
                        return rn, cn

    def get_possibilities(self):
        r, c = self.get_position(0, self.state)
        possibilities = {"up": 1, "left": 1, "down": 1, "right": 1}
        if r == 0 or self.prev_move == "down":
            possibilities["up"] = 0
        if r == 2 or self.prev_move == "up":
            possibilities["down"] = 0
        if c == 0 or self.prev_move == "right":
            possibilities["left"] = 0
        if c == 2 or self.prev_move == "left":
            possibilities["right"] = 0
        possible_moves = [m for m, v in possibilities.items() if v == 1]
        return possible_moves

    def compute_distance_disp(self):
        global final_state
        distance = 0
        for r in range(3):
            for c in range(3):
                if not self.state[r][c] == final_state[r][c]:
                    distance = distance + 1
                    # print(r, c)
        self.distance = distance + self.step

    def compute_distance_man(self):
        global final_state
        distance = 0
        for r in range(3):
            for c in range(3):
                current_pos_r, current_pos_c = self.get_position(r*3+c, self.state)
                final_pos_r, final_pos_c = self.get_position(r*3+c, final_state)
                distance += abs(final_pos_r-current_pos_r)+abs(final_pos_c-current_pos_c)
        self.distance = distance + self.step

    def generate_next_states(self):
        possibilities = self.get_possibilities()
        blank_r, blank_c = self.get_position(0, self.state)
        for p in possibilities:
            next_state = self.compute_next_state(p, blank_r, blank_c)
            self.next_states.append(Instance(self.step + 1, next_state, self, p))

    def compute_next_state(self, possible_move, blank_r, blank_c):
        state = copy.deepcopy(self.state)
        if possible_move == "up":
            state[blank_r][blank_c], state[blank_r - 1][blank_c] = state[blank_r - 1][blank_c], state[blank_r][blank_c]
        elif possible_move == "down":
            state[blank_r][blank_c], state[blank_r + 1][blank_c] = state[blank_r + 1][blank_c], state[blank_r][blank_c]
        elif possible_move == "left":
            state[blank_r][blank_c], state[blank_r][blank_c - 1] = state[blank_r][blank_c - 1], state[blank_r][blank_c]
        elif possible_move == "right":
            state[blank_r][blank_c], state[blank_r][blank_c + 1] = state[blank_r][blank_c + 1], state[blank_r][blank_c]
        return state


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def put(self, item):
        if len(self.queue) == 0:
            self.queue.append(item)
        else:
            for i, inst in enumerate(self.queue):
                if inst.distance > item.distance:
                    self.queue.insert(i, item)
                    break
                elif i == len(self.queue)-1:
                    self.queue.append(item)
                    break

    def get(self):
        return self.queue.pop(0)

    def __str__(self):
        return str(self.queue)


final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
count = 0
instance_queue = PriorityQueue()
puzzle = Instance()
puzzle.get_input()
puzzle.print_state("Initial state: ")
instance_queue.put(puzzle)
solved = False
while not solved:
    current_instance = instance_queue.get()
    # current_instance.print_state("step: {0}, distance: {1}".format(current_instance.step, current_instance.distance))
    if current_instance.state == final_state:
        solved = True
        print("Solved!!!")
        print("\nPath: ")
        ins = current_instance
        path = []
        while ins.prev_instance:
            path.append(ins)
            ins = ins.prev_instance
        path.reverse()
        for ins in path:
            ins.print_state("step: {0}, distance: {1}".format(ins.step, ins.distance))
        print("Count: {}".format(count))
        break
    current_instance.generate_next_states()
    for ins in current_instance.next_states:
        instance_queue.put(ins)
