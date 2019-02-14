class State:
    def __init__(self, matrix, heuristic):
        self.matrix = matrix
        if callable(heuristic):
            self.heuristic = heuristic(matrix)
        else:
            self.heuristic = heuristic
