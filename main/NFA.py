from queue import Queue


class NFA:
    def __init__(self, n, m, start_states, final_states, delta):
        self.num_of_states = n
        self.num_of_symbs = m
        self.start_states = set(start_states)
        self.final_states = set(final_states)
        self.simple_delta = delta
        self.delta = [[set() for j in range(self.num_of_symbs)] for i in range(self.num_of_states)]
        for q_from, symb, q_to in self.simple_delta:
            self.delta[q_from][symb].add(q_to)

    def solve(self, w):
        w = [int(symb) for symb in w]

        cur = self.start_states
        for symb in w:
            next = set()
            for q in cur:
                next |= self.delta[q][symb]
            cur = next

        return bool(cur & self.final_states)

    def convert_to_DFA(self):
        states = set()
        delta = []
        que = Queue()
        que.put(self.start_states)
        while not que.empty():
            cur = que.get()
            if cur not in states:
                states.add(frozenset(cur))
                for symb in range(self.num_of_symbs):
                    next = set()
                    for q in cur:
                        next |= self.delta[q][symb]
                    que.put(next)
                    delta.append((cur, symb, next))

        final_states = set()
        for q in states:
            if bool(q & self.final_states):
                final_states.add(q)

        return len(states), self.num_of_symbs, self.start_states, final_states, delta

    @staticmethod
    def init_from_file(input_path):
        input = open(input_path, "r")

        n = int(input.readline())
        m = int(input.readline())
        start_states = list(map(int, input.readline().split()))
        final_states = list(map(int, input.readline().split()))
        delta = []
        while True:
            line = input.readline()
            if not line:
                break
            delta.append(tuple(map(int, line.split())))

        input.close()
        return NFA(n, m, start_states, final_states, delta)
