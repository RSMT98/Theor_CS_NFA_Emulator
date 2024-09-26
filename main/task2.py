from main.NFA import NFA


def write_in_correct_format(output, iterable):
    for i in range(len(iterable)):
        if i > 0:
            output.write(' ')
        if (isinstance(iterable[i],set)) and (len(iterable[i]) == 0):
            output.write('{}')
        else:
            output.write(f'{iterable[i]}')
    output.write('\n')


def solve(input_path, output_path):
    output = open(output_path, 'w')
    n, m, start_state, final_states, delta = NFA.init_from_file(input_path).convert_to_DFA()

    output.write(f'{n}\n')
    output.write(f'{m}\n')
    output.write(f'{start_state}\n')
    write_in_correct_format(output, [set(elem) for elem in final_states])
    for step in delta:
        write_in_correct_format(output, step)
    output.close()

if __name__ == '__main__':
    _input_path, _output_path = input().split()
    solve(_input_path, _output_path)
