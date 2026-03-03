class StateMachine:
    """
    Handles phases and states and the transition logic between these states.
    """
    def __init__(self, initial_state):
        self.state = initial_state   # the current active state the machine is in
        self.time_in_state = 0.0     # tracks how long the machine has been in the current state
        self.transitions = []        # list of all registered (from_state, to_state, condition) rules

    def add_transition(self, from_state, to_state, condition):
        # registers a new transition rule — when in from_state and condition is met, move to to_state
        self.transitions.append((from_state, to_state, condition))

    def update(self, delta_time):
        # called every frame to advance time and check if any transition condition is met
        self.time_in_state += delta_time  # accumulate time spent in the current state

        for from_state, to_state, condition in self.transitions:
            # only evaluate transitions that are relevant to the current state
            if self.state == from_state and condition(self):
                self.set_state(to_state)
                break  # stop checking after the first valid transition to avoid multiple state changes in one frame

    def set_state(self, new_state):
        # switches to a new state and resets the timer so time_in_state is fresh for the new phase
        self.state = new_state
        self.time_in_state = 0.0