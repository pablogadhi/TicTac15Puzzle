from copy import deepcopy


class Path:
    def __init__(self, states, step_cost_calculator, path_cost=None):
        self.states = deepcopy(states)
        self.last = states[len(states) - 1]
        self.step_cost_calculator = step_cost_calculator
        if path_cost is None:
            self.path_cost = self.get_path_cost()
        else:
            self.path_cost = path_cost

    def add_state(self, state):
        self.states.append(state)
        self.last = state

    def get_path_cost(self):
        cost = 0
        for i in range(0, len(self.states) - 1):
            cost += self.step_cost_calculator(self.states[i], self.states[i + 1])
        return cost

    def update_path_cost(self, pre_last_state, last_state):
        self.path_cost += self.step_cost_calculator(pre_last_state, last_state)
