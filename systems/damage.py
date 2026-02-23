import pygame

from core.physics import circle_overlap, normalize, apply_impulse

def damage_system(player,enemies, delta_time):
    """
    Handles player taking contact damage from enemies.
    """

    for enemy in enemies:

        #makes it so the next part only runs if collision actually occurs
        if not circle_overlap(
            player.rect.centerx, player.rect.centery, player.core_radius,
            enemy.rect.centerx, enemy.rect.centery, enemy.core_radius
        ):
            continue
        
        # skips ahead if player is invunerable at current frame
        if player.invuln_timer > 0:
            continue
            
        # skips to next enemy if current one is on attack cooldown
        if enemy.hit_timer > 0:
            continue

        player.take_damage(enemy.damage)
        enemy.hit_timer = enemy.hit_cooldown
        player.invuln_timer = player.invulnerability_duration
        enemy.last_hit_time = 0.0

        dx = enemy.rect.centerx - player.rect.centerx
        dy = enemy.rect.centery - player.rect.centery
        nx, ny = normalize(dx, dy)

        Rp = player.rigidity
        Re = enemy.rigidity
        base_force = 30

        Rt = Rp + Re

        if Rt == 0:
            return
        
        Wp = Re / Rt
        We = Rp / Rt

        apply_impulse(player, -nx, -ny, base_force * Wp)
        apply_impulse(enemy, nx, ny, base_force * We)

        enemy.stun_end_time = delta_time + enemy.stun_duratio