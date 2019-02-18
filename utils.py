def input_to_matrix(input_string):
    matrix = []

    index = 0
    for i, char in enumerate(input_string):
        if i % 4 == 0:
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


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y