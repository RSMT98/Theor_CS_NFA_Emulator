from NFA import NFA

if __name__ == '__main__':
    input_path, w = input().split()
    print(NFA.init_from_file(input_path).solve(w))
