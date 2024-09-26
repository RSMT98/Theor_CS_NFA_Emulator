from main.NFA import NFA
from main import task2
import unittest
from re import split
from random import randint, choice
import os


class TestNFASolvability(unittest.TestCase):
    """
    NFA for language L = {0^m1^n | there exists k in {2, 3, 5} into which both m and n are divided
    """

    def test_on_hw2_3(self):
        nfa = NFA(20, 2, {0, 4, 10}, {0, 4, 10, 2, 7, 15}, [(0, 0, 1), (1, 0, 0), (0, 1, 3), (3, 1, 2), (2, 1, 3),
                                                            (4, 0, 5), (5, 0, 6), (6, 0, 4), (4, 1, 8), (8, 1, 9),
                                                            (9, 1, 7),
                                                            (7, 1, 8),
                                                            (10, 0, 11), (11, 0, 12), (12, 0, 13), (13, 0, 14),
                                                            (14, 0, 10),
                                                            (10, 1, 16), (16, 1, 17), (17, 1, 18), (18, 1, 19),
                                                            (19, 1, 15),
                                                            (15, 1, 16)])
        self.assertTrue(nfa.solve("0011"))
        self.assertTrue(nfa.solve("000000111111"))
        self.assertTrue(nfa.solve("0000011111"))
        self.assertFalse(nfa.solve("01"))
        self.assertTrue(nfa.solve("00001111"))
        self.assertFalse(nfa.solve("000011111"))
        self.assertFalse(nfa.solve("000001111"))
        self.assertFalse(nfa.solve("1100"))

    """
    the third character from the end is 0
    """

    def test_on_example_from_lec2(self):
        nfa = NFA(4, 2, {0}, {3}, [(0, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 2), (1, 1, 2), (2, 0, 3), (2, 1, 3)])
        self.assertFalse(nfa.solve("00"))
        self.assertFalse(nfa.solve("0"))
        self.assertTrue(nfa.solve("000"))
        self.assertTrue(nfa.solve("0001"))
        self.assertTrue(nfa.solve("00011"))
        self.assertFalse(nfa.solve("000111"))
        self.assertFalse(nfa.solve("111"))
        self.assertFalse(nfa.solve("1110"))
        self.assertFalse(nfa.solve("11100"))
        self.assertTrue(nfa.solve("111000"))

    """
    has no substring 110
    """

    def test_on_nfa_from_practice3(self):
        nfa = NFA(4, 2, {0}, {0, 1, 2},
                  [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 2), (2, 1, 2), (2, 0, 3), (3, 0, 3), (3, 1, 3)])
        self.assertTrue(nfa.solve("0010011"))
        self.assertTrue(nfa.solve("011"))
        self.assertTrue(nfa.solve("101"))
        self.assertTrue(nfa.solve("111111"))
        self.assertTrue(nfa.solve("0100101011"))
        self.assertFalse(nfa.solve("01100101011"))
        self.assertFalse(nfa.solve("1111011"))
        self.assertFalse(nfa.solve("0110"))


class TestNFAConvertibility(unittest.TestCase):
    input_path = "test_input.txt"
    output_path = "test_output.txt"
    max_w_len = 1000
    num_of_stress_tests = 1000

    def tearDown(self):
        os.remove(self.input_path)
        os.remove(self.output_path)

    @staticmethod
    def write_NFA_to_file(nfa, output_path):
        output = open(output_path, 'w')
        n, m, start_states, final_states, delta = nfa.num_of_states, nfa.num_of_symbs, nfa.start_states, nfa.final_states, nfa.simple_delta

        output.write(f'{n}\n')
        output.write(f'{m}\n')
        task2.write_in_correct_format(output, list(start_states))
        task2.write_in_correct_format(output, list(final_states))
        for step in delta:
            task2.write_in_correct_format(output, step)
        output.close()

    @staticmethod
    def read_DFA_with_sets(input_path):
        input = open(input_path, "r")

        n = int(input.readline())
        m = int(input.readline())

        class SetEncoder:
            cur_state_num = 0
            set_encoder = dict()

            def encode(self, _set):
                if _set not in self.set_encoder:
                    self.set_encoder[_set] = self.cur_state_num
                    self.cur_state_num += 1

                return self.set_encoder[_set]

        se = SetEncoder()
        start_states = [se.encode(_set) for _set in split('{|}', input.readline().strip()) if _set.strip()]
        final_states = [se.encode(_set) for _set in split('{|}', input.readline().strip()) if _set.strip()]
        delta = []
        while True:
            line = input.readline()
            if not line:
                break
            line = [st for st in split('{|}', line.strip().replace('{}', '{trap}')) if st.strip()]
            delta.append((se.encode(line[0]), int(line[1]), se.encode(line[2])))

        input.close()
        return NFA(n, m, start_states, final_states, delta)

    def stress_test(self, nfa):
        self.write_NFA_to_file(nfa, self.input_path)
        task2.solve(self.input_path, self.output_path)
        dfa = self.read_DFA_with_sets(self.output_path)

        for _ in range(self.num_of_stress_tests):
            w_len = randint(0, self.max_w_len)
            w = ''.join(choice(list(map(str, range(nfa.num_of_symbs)))) for i in range(w_len))
            self.assertEqual(nfa.solve(w), dfa.solve(w))

    """
    NFA for language L = {0^m1^n | there exists k in {2, 3, 5} into which both m and n are divided
    """

    def test_on_hw2_3(self):
        nfa = NFA(20, 2, {0, 4, 10}, {0, 4, 10, 2, 7, 15}, [(0, 0, 1), (1, 0, 0), (0, 1, 3), (3, 1, 2), (2, 1, 3),
                                                            (4, 0, 5), (5, 0, 6), (6, 0, 4), (4, 1, 8), (8, 1, 9),
                                                            (9, 1, 7),
                                                            (7, 1, 8),
                                                            (10, 0, 11), (11, 0, 12), (12, 0, 13), (13, 0, 14),
                                                            (14, 0, 10),
                                                            (10, 1, 16), (16, 1, 17), (17, 1, 18), (18, 1, 19),
                                                            (19, 1, 15),
                                                            (15, 1, 16)])
        self.stress_test(nfa)

    """
    the third character from the end is 0
    """

    def test_on_example_from_lec2(self):
        nfa = NFA(4, 2, {0}, {3}, [(0, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 2), (1, 1, 2), (2, 0, 3), (2, 1, 3)])
        self.stress_test(nfa)

    """
    has no substring 110
    """

    def test_on_nfa_from_practice3(self):
        nfa = NFA(4, 2, {0}, {0, 1, 2},
                  [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 2), (2, 1, 2), (2, 0, 3), (3, 0, 3), (3, 1, 3)])
        self.stress_test(nfa)


if __name__ == '__main__':
    unittest.main()
