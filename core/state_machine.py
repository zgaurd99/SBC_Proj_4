class StateMachine:
    """
    Handles phases and states and the transition logic between these states.
    """

    def __init__(self, initial_state):
        self.state = initial_state
        self.time_in_state = 0.0
        self.transitions = []

    def add_transition(self, from_state, to_state, condition):
        self.transitions.append((from_state, to_state, condition))

    def update(self, delta_time):
        self.time_in_state += delta_time

        for from_state, to_state, condition in self.transitions:
            if self.state == from_state and condition(self):
                self.set_state(to_state)
                break

    def set_state(self, new_state):
        self.state = new_state
        self.time_in_state = 0.0