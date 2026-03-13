from core.physics import resolve_circle_overlap

def player_enemy_collision_system(player, enemies):
    """
    Resolves positional overlap between player and enemies.
    Does NOT apply damage.
    """

    for enemy in enemies:
        if enemy.hit_timer > 0:
            continue
        resolve_circle_overlap(player, enemy, weight_a=0.4, weight_b=0.6)

def enemy_enemy_collision_system(enemies):
    """
    Resolves positional overlap between enemies.
    """

    for i in range(len(enemies)):
        for j in range(i + 1, len(enemies)):
            a, b = enemies[i], enemies[j]
            if a.hit_timer > 0 or b.hit_timer > 0:
                continue
            resolve_circle_overlap(a, b)