import sys
from utils import input_to_matrix, intersection, Position
from ps_engine.problem import Problem
from ps_engine.state import State
from ps_engine.core import solve_problem
from ps_engine.action import Action


def step_cost_calculator(first_state, second_state):
    return 1


def goal_test(state):
    for row in state.matrix:
        for col in row:
            if col == '.':
                return False
    return True


def find_empty_position(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if matrix[i][j] == '.':
                return Position(i, j)


def get_possibilities(matrix, position):
    v_possibilities = ['1', '2', '3', '4']
    h_possibilities = ['1', '2', '3', '4']
    sq_possibilities = ['1', '2', '3', '4']

    for i in range(0, 4):
        value = matrix[position.x][i]
        if value != '.':
            h_possibilities.remove(value)

        value = matrix[i][position.y]
        if value != '.':
            v_possibilities.remove(value)

    offset_x = 0
    if position.x % 2 != 0:
        offset_x = -1
    offset_y = 0
    if position.y % 2 != 0:
        offset_y = -1

    new_position_x = position.x + offset_x
    new_position_y = position.y + offset_y

    for i in range(new_position_x, new_position_x + 2):
        for j in range(new_position_y, new_position_y + 2):
            value = matrix[i][j]
            if value != '.':
                sq_possibilities.remove(value)

    return intersection(v_possibilities, intersection(h_possibilities, sq_possibilities))


def set_value(**kwargs):
    matrix = kwargs.get("matrix")
    position = kwargs.get("position")
    value = kwargs.get("value")
    matrix[position.x][position.y] = value
    return matrix


def get_actions(state):
    position = find_empty_position(state.matrix)
    possibilities = get_possibilities(state.matrix, position)
    actions = []
    for possibility in possibilities:
        actions.append(Action(set_value, matrix=state.matrix, position=position, value=possibility))

    return actions


def heuristic_calculator(matrix):
    return 1


def get_result(action):
    new_matrix = action.run_action()
    return State(new_matrix, heuristic_calculator)


def main():
    if len(sys.argv) != 2:
        sys.exit(-1)

    inp = sys.argv[1]
    mat = input_to_matrix(inp)

    problem = Problem(mat, step_cost_calculator, goal_test, get_actions, get_result,
                      heuristic_calculator)
    result = solve_problem(problem)

    if result is not None:
        print(result.last.matrix)
    else:
        print("No hay solucion!")

    sys.exit(0)


if __name__ == '__main__':
    main()
