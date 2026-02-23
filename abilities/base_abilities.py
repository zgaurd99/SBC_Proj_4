from core.state_machine import StateMachine

class BaseAbilitiy:
    def __init__(self, owner):
        self.owner = owner

        self.windup_time = 0
        self.active_time = 0
        self.recovery_time = 0
        self.cooldown_time = 0

        self.state_machine = StateMachine("idle")

        self._setup_transitions()

    def _setup_transitions(self):
        #windup->active after windup_time
        self.state_machine.add_transition(
            "windup",
            "active",
            lambda m, t:m.time_in_state >= self.windup_time
        )

        #active->recovery after active_time
        self.state_machine.add_transition(
            "active",
            "recovery",
            lambda m, t :m.time_in_state >= self.active_time
        )
        
        #recover -> cooldown after recovery_time
        self.state_machine.add_transition(
            "recovery",
            "cooldown",
            lambda m, t: m.time_in_state >= self.recovery_time
        )


        self.state_machine.add_transition(
            "cooldown",
            "idle",
            lambda m, t: m.time_in_state >= self.cooldown_time
        )
    
    def try_activate(self):
        """
        Attempts to activate the ability. Returns True if successful, False otherwise.
        """
        if self.machine.state != "idle":
            return False
        
        self.machine.set_state("windup")
        return True
    
    def update(self, delta_time):
        """
        Called every frame to update the state machine and handle cooldowns.
        """
        previous_state = self.machine.state
        self.machine.update(delta_time)
        current_state = self.machine.state

        if previous_state != current_state:
            self.on_state_change(current_state)

        self.on_update(current_state, delta_time)

    def on_state_enter(self, state, delta_time):
        """
        Override for entering a state
        """
        if state == "cooldown":
            self.cooldown_end_time = delta_time + self.cooldown_time

    def on_update(self, state, delta_time):
        """
        Override for per-frame behaviour
        """
        pass

    def is_active(self):
        return self.machine.state == "active"
    
    def is_busy(self):
        return self.machine.state != "idle"

