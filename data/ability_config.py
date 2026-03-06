ABILITY_CONFIG = {
    "sword": {
        "behavior": "melee",
        "windup_time": 0.25,
        "active_time": 0.1,
        "recovery_time": 0.25,
        "cooldown_time": 0.2,
        "radius": 60,
        "damage": 3,
        "base_force": 35,
        "lock_movement": True,
    },
    "bow": {
        "behavior": "ranged",
        "windup_time": 0.4,
        "active_time": 0.1,
        "recovery_time": 0.3,
        "cooldown_time": 0.5,
        "projectile_speed": 8,
        "damage": 2,
        "base_force": 20,
        "lock_movement": False,
    },
    "light_armour": {
        "behavior": "defensive",
        "defense_modifier": 0.2,
        "modifier_type": "percent",
    },
}