class Action:
    def __init__(self, operation, **kwargs):
        self.operation = operation
        self.args = kwargs

    def run_action(self):
        return self.operation(**self.args)
