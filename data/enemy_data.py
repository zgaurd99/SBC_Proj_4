ENEMY_TYPES = {
    "basic": {
        "attack": 1,
        "health": 3,
        "defense": 1.0,
        "speed": 2,
        "rigidity": 5,
        "attack_speed": 1.0,
        "stun_factor": 1.0,
        "stun_strength": 1.0,
        "crit_chance": 0.1,
        "crit_multiplier": 1.5,
        "gauge_cost": 1,
        "colour": (200, 50, 50),
        "animation": {
            "sheet": "assets/enemies/brittle_archer/BrittleArcher.png",
            "json":  "assets/enemies/brittle_archer/BrittleArcher.json"
        }
    },
    "fast": {
        "width": 20,
        "height": 20,
        "attack": 1,
        "health": 2,
        "defense": 0.5,
        "speed": 3,
        "rigidity": 3,
        "attack_speed": 2.0,
        "stun_factor": 2.0,
        "stun_strength": 0.5,
        "crit_chance": 0.2,
        "crit_multiplier": 1.25,
        "gauge_cost": 2,
        "colour": (200, 50, 50)
    },
    "tank": {
        "width": 45,
        "height": 45,
        "attack": 2,
        "health": 5,
        "defense": 1.5,
        "speed": 1,
        "rigidity": 7,
        "attack_speed": 0.5,
        "stun_factor": 0.5,
        "stun_strength": 2.0,
        "crit_chance": 0.5,
        "crit_multiplier": 1.75,
        "gauge_cost": 3,
        "colour": (200, 50, 50)
    }
}
