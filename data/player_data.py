PLAYER_DATA = {
    "P1": {
        "width": 20,
        "height": 20,
        "attack": 2,
        "attack_speed": 1.0,
        "stun_factor": 1.0,
        "stun_strength": 0.5,
        "crit_chance": 0.1,
        "crit_multiplier": 1.5,
        "speed": 1,
        "health": 100,
        "defense": 1,
        "rigidity": 20,
        "boosts": [1.0, 1.0, 1.0, 1.0],
        # 0 = speed
        # 1 = health
        # 2 = defense
        # 3 = rigidity
        "regen_time": 8,
        "regen_amt": 1,
        "abilities": {
            "active": ["sword", "decoy"],
            "passive": [],
            "bindings": {
                1: 0,  # left click  -> slot 0
                3: 1   # right click -> slot 1
            }
        }
    }
}