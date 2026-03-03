from core.state_machine import StateMachine
#Arin Adkar Ka Coding Hai Im  Responsible
class BaseAbility:
    def __init__(self, owner):
        self.owner = owner          # the entity that owns and uses this ability
        self.windup_time = 0        # preparation time before the ability actually activates
        self.active_time = 0        # how long the ability stays active
        self.recovery_time = 0      # cooldown before the entity can move on
        self.cooldown_time = 0      # waiting time before the ability can be used again
        # create a state machine starting at idle, this manages which phase the ability is in
        self.machine = StateMachine("idle")
        self._setup_transitions()   # set up the rules for moving between phases

    def _setup_transitions(self):
        # each transition says: "when in state X, move to state Y once enough time has passed"

        # windup -> active: ability activates after windup time is done
        self.machine.add_transition(
            "windup",
            "active",
            lambda m, t: m.time_in_state >= self.windup_time
        )
        # active -> recovery: ability ends and enters recovery after active time is done
        self.machine.add_transition(
            "active",
            "recovery",
            lambda m, t: m.time_in_state >= self.active_time
        )
        # recovery -> cooldown: recovery finishes and cooldown begins
        self.machine.add_transition(
            "recovery",
            "cooldown",
            lambda m, t: m.time_in_state >= self.recovery_time
        )
        # cooldown -> idle: cooldown finishes and ability is ready to use again
        self.machine.add_transition(
            "cooldown",
            "idle",
            lambda m, t: m.time_in_state >= self.cooldown_time
        )

    def try_activate(self):
        # ability can only be activated when it's idle (not already in use)
        if self.machine.state != "idle":
            return False  # ability is busy, activation failed
        # move to windup phase to start the ability
        self.machine.set_state("windup")
        return True  # activation successful

    def update(self, delta_time):
        previous_state = self.machine.state  # remember the state before updating
        self.machine.update(delta_time)       # update the state machine, may trigger a transition
        current_state = self.machine.state    # check the state after updating
        # if the state changed, notify that we entered a new phase
        if previous_state != current_state:
            self.on_state_enter(current_state)
        self.on_update(delta_time)  # run any per-frame logic for the current state

    def on_state_enter(self, state):
        # called whenever the ability enters a new phase
        # subclasses can override this to do something specific on phase change
        """Override in subclasses"""
        pass

    def on_update(self, delta_time):
        # called every frame while the ability is running
        # subclasses can override this to add custom per-frame behavior
        """Override in subclasses"""
        pass

    def is_active(self):
        # returns True only if the ability is currently in its active phase
        return self.machine.state == "active"

    def is_busy(self):
        # returns True if the ability is in any phase other than idle
        # meaning the ability is currently in use and cannot be activated again
        return self.machine.state != "idle"