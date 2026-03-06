from core.state_machine import StateMachine

class BaseAbility:
    def __init__(self, owner):
        self.owner = owner

        self.windup_time = 0
        self.active_time = 0
        self.recovery_time = 0
        self.cooldown_time = 0

        self.machine = StateMachine("idle")

        self._setup_transitions()

    def _setup_transitions(self):
        # windup -> active
        self.machine.add_transition(
            "windup",
            "active",
            lambda m: m.time_in_state >= self.windup_time
        )

        # active -> recovery
        self.machine.add_transition(
            "active",
            "recovery",
            lambda m: m.time_in_state >= self.active_time
        )

        # recovery -> cooldown
        self.machine.add_transition(
            "recovery",
            "cooldown",
            lambda m: m.time_in_state >= self.recovery_time
        )

        # cooldown -> idle
        self.machine.add_transition(
            "cooldown",
            "idle",
            lambda m: m.time_in_state >= self.cooldown_time
        )

    def try_activate(self):
        if self.machine.state != "idle":
            return False

        self.machine.set_state("windup")
        return True

    def update(self, delta_time, targets=None):
        previous_state = self.machine.state

        self.machine.update(delta_time)

        current_state = self.machine.state

        if previous_state != current_state:
            self.on_state_enter(current_state)

        self.on_update(delta_time, targets or [])
        
    def on_update(self, delta_time, targets=None):
        """Override in subclasses"""
        pass

    def on_state_enter(self, state):
        """Override in subclasses"""
        pass

    def is_active(self):
        return self.machine.state == "active"

    def is_busy(self):
        return self.machine.state != "idle"