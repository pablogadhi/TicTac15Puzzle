from .path import Path
from .state import State
from copy import deepcopy


def solve_problem(problem):
    frontier = [Path([State(problem.initial_state, problem.heuristic_calculator)],
                     problem.step_cost_calculator)]
    explored = []

    while True:
        if len(frontier) > 0:
            current_path = select_next_path(frontier)
            explored.append(current_path.last.matrix)
            # for i in current_path.last.matrix:
            #     print(i)
            # print()
            path_edge = current_path.last

            if problem.goal_test(path_edge):
                return current_path

            for action in problem.get_actions(path_edge):
                result = problem.get_result(action)
                if result.matrix not in explored:
                    new_path = Path(current_path.states, problem.step_cost_calculator,
                                    current_path.path_cost)
                    new_path.add_state(result)
                    new_path.update_path_cost(new_path.states[len(new_path.states) - 2],
                                              new_path.states[len(new_path.states) - 1])
                    frontier.append(new_path)

        else:
            return None


def select_next_path(frontier):
    selected_path = Path([State([], 99999999999999)], None, 99999999999999)
    for path in frontier:
        if a_star_condition(path) < a_star_condition(selected_path):
            selected_path = path
    path_to_return = deepcopy(selected_path)
    frontier.remove(selected_path)
    return path_to_return


def a_star_condition(path):
    # print(path.path_cost, path.last.heuristic)
    return path.path_cost + path.last.heuristic
