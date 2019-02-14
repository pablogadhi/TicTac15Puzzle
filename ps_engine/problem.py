class Problem:
    def __init__(self, initial_state, step_cost_calculator, goal_test, get_actions, get_result):
        self.initial_state = initial_state
        self.step_cost_calculator = step_cost_calculator
        self.goal_test = goal_test
        self.get_actions = get_actions
        self.get_result = get_result
