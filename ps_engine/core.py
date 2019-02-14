from .path import Path
from .state import State


def solve_problem(problem):
    frontier = [Path([State(problem.initial_state, problem.heuristic_calculator)],
                     problem.step_cost_calculator)]

    while True:
        if len(frontier) > 0:
            current_path = select_next_path(frontier)
            path_edge = current_path.last

            if problem.goal_test(path_edge):
                return current_path

            for action in problem.get_actions(path_edge):
                new_path = Path(current_path.states, problem.step_cost_calculator,
                                current_path.path_cost)
                new_path.add_state(
                    State(problem.get_result(action, path_edge), problem.heuristic_calculator))
                new_path.update_path_cost(new_path.states[len(new_path.states) - 2],
                                          new_path.states[len(new_path.states) - 1])
                frontier.append(new_path)

        else:
            return None


def select_next_path(frontier):
    selected_path = Path([State([], 9999)], None, 9999)
    for path in frontier:
        if a_star_condition(path) < a_star_condition(selected_path):
            selected_path = path
    return selected_path


def a_star_condition(path):
    return path.path_cost + path.last.heuristic
