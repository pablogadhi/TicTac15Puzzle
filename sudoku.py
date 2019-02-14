import sys


def input_to_matrix(input_string):
    matrix = []

    index = 0
    for i, char in enumerate(input_string):
        if i % 4 == 0:
            matrix.append([])
            index += 1

        matrix[index - 1].append(char)

    return matrix


def main():
    if len(sys.argv) != 2:
        sys.exit(-1)

    inp = sys.argv[1]
    mat = input_to_matrix(inp)
    print(mat)
    sys.exit(0)


if __name__ == '__main__':
    main()
