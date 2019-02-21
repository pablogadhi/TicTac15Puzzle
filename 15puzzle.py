import sys
import curses
from copy import deepcopy
from time import sleep

from utils import input_to_matrix, find_empty_position, Position
from ps_engine.problem import Problem
from ps_engine.state import State
from ps_engine.core import solve_problem
from ps_engine.action import Action
from graphics import puzzle_grid

TARGET_POSITIONS = {
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

GOAL = [['1', '2', '3', '4'],
        ['5', '6', '7', '8'],
        ['9', 'A', 'B', 'C'],
        ['D', 'E', 'F', '.']]


def step_cost_calculator(first_state, second_state):
    # overall_distance = 0
    # for i, row in enumerate(second_state.matrix):
    #     for j, val in enumerate(row):
    #         t_pos = TARGET_POSITIONS[val]
    #         overall_distance += (abs(t_pos.x - i) + abs(t_pos.y - j)) * (
    #                 len(second_state.matrix) - (t_pos.x * t_pos.y))
    # return overall_distance

    first_blank_pos = find_empty_position(first_state.matrix)
    second_blank_pos = find_empty_position(second_state.matrix)

    swapped_value = second_state.matrix[first_blank_pos.x][first_blank_pos.y]
    target_pos = TARGET_POSITIONS[swapped_value]

    if second_blank_pos.x == target_pos.x and second_blank_pos.y == target_pos.y:
        return 7

    first_state_distance = abs(target_pos.x - second_blank_pos.x) + abs(
        target_pos.y - second_blank_pos.y)
    second_state_distance = abs(target_pos.x - first_blank_pos.x) + abs(
        target_pos.y - first_blank_pos.y)

    if second_state_distance <= first_state_distance:
        return 0

    return second_state_distance


def goal_test(state):
    if state.matrix == GOAL:
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
    heuristic = 2 ** 16
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            t_pos = TARGET_POSITIONS[matrix[i][j]]
            if t_pos.x == i and t_pos.y == j:
                heuristic /= 2
            else:
                return heuristic / 1000
    return heuristic / 1000


def get_result(action):
    new_matrix = action.run_action()
    return State(new_matrix, heuristic_calculator)


def main(stdscr):
    if len(sys.argv) != 2:
        sys.exit(-1)

    curses.use_default_colors()
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_MAGENTA, -1)
    stdscr.addstr(0, 0, "Procesando...", curses.color_pair(1))
    stdscr.refresh()

    inp = sys.argv[1]
    mat = input_to_matrix(inp)

    problem = Problem(mat, step_cost_calculator, goal_test, get_actions, get_result,
                      heuristic_calculator)
    result = solve_problem(problem)

    if result is not None:
        for state in result.states:
            flattened_matrix = lambda matrix: [val for row in matrix for val in row]
            state_string = puzzle_grid(tuple(flattened_matrix(state.matrix)))
            stdscr.addstr(0, 0, state_string, curses.color_pair(1))
            stdscr.refresh()
            sleep(.2)
    else:
        stdscr.addstr(0, 0, "No hay solucion!\n")
        stdscr.refresh()

    while True:
        key = stdscr.getkey()
        if key == 'q':
            sys.exit(0)


if __name__ == '__main__':
    curses.wrapper(main)
