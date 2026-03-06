from core.physics import resolve_circle_overlap

def player_enemy_collision_system(player, enemies):
    """
    Resolves positional overlap between player and enemies.
    Does NOT apply damage.
    """

    for enemy in enemies:
        resolve_circle_overlap(player, enemy, weight_a=0.4, weight_b=0.6)

def enemy_enemy_collision_system(enemies):
    """
    Resolves positional overlap between enemies.
    """

    for i in range(len(enemies)):
        for j in range(i + 1, len(enemies)):
            resolve_circle_overlap(enemies[i], enemies[j])