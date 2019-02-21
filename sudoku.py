import sys
import math
import curses
from copy import deepcopy
from time import sleep

from utils import input_to_matrix, intersection, find_empty_position
from ps_engine.problem import Problem
from ps_engine.state import State
from ps_engine.core import solve_problem
from ps_engine.action import Action
from graphics import sudoku_grid, sudoku_grid_9


def step_cost_calculator(first_state, second_state):
    return 1


def goal_test(state):
    for row in state.matrix:
        for col in row:
            if col == '.':
                return False
    return True


def get_possibilities(matrix, position):
    v_possibilities = [str(i).zfill(1) for i in range(1, len(matrix) + 1)]
    h_possibilities = [str(i).zfill(1) for i in range(1, len(matrix) + 1)]
    sq_possibilities = [str(i).zfill(1) for i in range(1, len(matrix) + 1)]

    for i in range(0, len(matrix)):
        value = matrix[position.x][i]
        if value != '.':
            h_possibilities.remove(value)

        value = matrix[i][position.y]
        if value != '.':
            v_possibilities.remove(value)

    dim = int(math.sqrt(len(matrix)))

    offset_x = 0
    offset_y = 0
    if dim == 2:
        if position.x % 2 != 0:
            offset_x = -1
        if position.y % 2 != 0:
            offset_y = -1
    else:
        offset_x = - (position.x % 3)
        offset_y = - (position.y % 3)

    new_position_x = position.x + offset_x
    new_position_y = position.y + offset_y

    for i in range(new_position_x, new_position_x + dim):
        for j in range(new_position_y, new_position_y + dim):
            value = matrix[i][j]
            if value != '.':
                sq_possibilities.remove(value)

    return intersection(v_possibilities, intersection(h_possibilities, sq_possibilities))


def set_value(**kwargs):
    matrix = deepcopy(kwargs.get("matrix"))
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
    pos = find_empty_position(matrix)
    if pos is None:
        return 99

    possibilities_amount = len(get_possibilities(matrix, pos))
    if possibilities_amount == 0:
        return 99
    else:
        return 1 - (1 / possibilities_amount)


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

    if len(inp) == 16:
        get_sudoku_grid = sudoku_grid
    else:
        get_sudoku_grid = sudoku_grid_9

    if result is not None:
        for state in result.states:
            flattened_matrix = lambda matrix: [val for row in matrix for val in row]
            state_string = get_sudoku_grid(tuple(flattened_matrix(state.matrix)))
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
