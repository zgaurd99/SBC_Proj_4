class StateMachine:
    """
    Handles phases and states and the transition logic between these states
    """

    def __init__(self, initial_state):
        self.state = initial_state
        self.state_start_time = 0
        self.transitions = {}

    def add_transition(self, from_state, to_state, condition_func):
        """
        To change states and add transition logic
        
        :param from_state: Current State
        :param to_state: Next State
        :param condition_func: condition_func(machine, current_time) -> boolon
        """

        if from_state not in self.transitions:
            self.transitions[from_state] = []
        
        self.transitions[from_state].append({
            "to": to_state,
            "condition": condition_func
        })

    def set_state(self, new_state, current_time):
        """
            changes the machine's state
        """
        self.state = new_state
        self.state_start_time = current_time

    def update(self, current_time):
        """
        Evaluates transitions for the current state.
        """

        if self.state not in self.transitions:
            return
    
        for transition in self.transitions[self.state]:
            if transition["condition"](self, current_time):
                self.set_state(transition["to"], current_time)
                break
        
    def time_in_state(self, current_time):
        return current_time - self.state_start_time