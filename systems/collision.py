from core.physics import apply_impulse, circle_overlap_data, resolve_circle_overlap

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

def decoy_enemy_collision_system(decoy, enemies):
    """
    Resolves overlap between decoy and enemies, applies reduced recoil and stun.
    """
    if not decoy or not decoy.alive:
        return

    for enemy in enemies:
        overlapping, nx, ny, overlap = circle_overlap_data(
            decoy.rect.centerx, decoy.rect.centery, decoy.core_radius,
            enemy.rect.centerx, enemy.rect.centery, enemy.core_radius
        )

        if not overlapping:
            continue

        decoy.rect.x -= nx * overlap * 0.4
        decoy.rect.y -= ny * overlap * 0.4
        enemy.rect.x += nx * overlap * 0.6
        enemy.rect.y += ny * overlap * 0.6

        Rd = decoy.get_stat("rigidity")
        Re = enemy.get_stat("rigidity")
        Rt = Rd + Re

        if Rt == 0:
            continue

        base_force = 15  # half of player contact force (30)
        We = Rd / Rt

        apply_impulse(enemy, nx, ny, base_force * We)

        stun_duration = min(0.5, 
            0.4
            * enemy.get_stat("stun_factor")
            * decoy.get_stat("stun_strength")
        )
        enemy.stun_timer = stun_duration