import sys
from copy import deepcopy
from utils import input_to_matrix, find_empty_position, Position

from ps_engine.problem import Problem
from ps_engine.state import State
from ps_engine.core import solve_problem
from ps_engine.action import Action

target_positions = {
    '1': Position(0, 0),
    '2': Position(0, 1),
    '3': Position(0, 2),
    '4': Position(0, 3),
    '5': Position(1, 0),
    '6': Position(1, 1),
    '7': Position(1, 2),
    '8': Position(1, 3),
    '9': Position(2, 0),
    'A': Position(2, 1),
    'B': Position(2, 2),
    'C': Position(2, 3),
    'D': Position(3, 0),
    'E': Position(3, 1),
    'F': Position(3, 2),
    '.': Position(3, 3),
}


def step_cost_calculator(first_state, second_state):
    first_blank_pos = find_empty_position(first_state.matrix)
    second_blank_pos = find_empty_position(second_state.matrix)

    x_diff = second_blank_pos.x - first_blank_pos.x
    y_diff = second_blank_pos.y - first_blank_pos.y

    swapped_value = second_state.matrix[second_blank_pos.x - x_diff][second_blank_pos.y - y_diff]
    target_pos = target_positions[swapped_value]

    step_cost = abs(target_pos.x - (second_blank_pos.x - x_diff)) + abs(
        target_pos.y - (second_blank_pos.y - y_diff))
    return step_cost


def goal_test(state):
    goal = [['1', '2', '3', '4'],
            ['5', '6', '7', '8'],
            ['9', 'A', 'B', 'C'],
            ['D', 'E', 'F', '.']]

    if state.matrix == goal:
        return True
    else:
        return False


def swap_values(**kwargs):
    first_pos = kwargs.get("first_pos")
    second_pos = kwargs.get("second_pos")
    matrix = kwargs.get("matrix")

    first_value = matrix[first_pos.x][first_pos.y]
    second_value = matrix[second_pos.x][second_pos.y]
    new_matrix = deepcopy(matrix)

    new_matrix[first_pos.x][first_pos.y] = second_value
    new_matrix[second_pos.x][second_pos.y] = first_value
    return new_matrix


def get_actions(state):
    actions = []
    pos = find_empty_position(state.matrix)

    if pos.x - 1 >= 0:
        actions.append(Action(swap_values, matrix=state.matrix, first_pos=pos,
                              second_pos=Position(pos.x - 1, pos.y)))
    if pos.x + 1 < len(state.matrix):
        actions.append(Action(swap_values, matrix=state.matrix, first_pos=pos,
                              second_pos=Position(pos.x + 1, pos.y)))
    if pos.y - 1 >= 0:
        actions.append(Action(swap_values, matrix=state.matrix, first_pos=pos,
                              second_pos=Position(pos.x, pos.y - 1)))
    if pos.y + 1 < len(state.matrix[0]):
        actions.append(Action(swap_values, matrix=state.matrix, first_pos=pos,
                              second_pos=Position(pos.x, pos.y + 1)))

    return actions


def heuristic_calculator(matrix):
    heuristic = 16
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            t_pos = target_positions[matrix[i][j]]
            if t_pos.x == i and t_pos.y == j:
                heuristic -= 1
    return heuristic


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
