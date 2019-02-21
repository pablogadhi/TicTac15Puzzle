def input_to_matrix(input_string):
    matrix = []

    dimension = 4
    if len(input_string) % 9 == 0:
        dimension = 9

    index = 0
    for i, char in enumerate(input_string):
        if i % dimension == 0:
            matrix.append([])
            index += 1

        matrix[index - 1].append(char)

    return matrix


def intersection(first_array, second_array):
    inter = []
    for i in first_array:
        if i in second_array:
            inter.append(i)
    return inter


def find_empty_position(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if matrix[i][j] == '.':
                return Position(i, j)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
