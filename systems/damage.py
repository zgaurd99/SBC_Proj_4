import pygame

from core.physics import circle_overlap, normalize, apply_impulse

def damage_system(player,enemies, current_time):
    """
    Handles player taking contact damage from enemies.
    """

    for enemy in enemies:

        #makes it so the next part only runs if collision actually occurs
        if not circle_overlap(
            player.rect.centerx, player.rect.centery, player.core_raadius,
            enemy.rect.centerx, enemy.rect.centery, enemy.core_radius
        ):
            continue
        
        # skips ahead if player is invunerable at current frame
        if current_time < player.invunerable_until:
            continue
            
        # skips to next enemy if current one is on attack cooldown
        if current_time - enemy.last_hit_time < enemy.hit_cooldown:
            continue

        player.take_damage(enemy.damage)
        player.invunerable_until = current_time + player.invunerablility_duration
        enemy.last_hit_time = current_time

        dx = enemy.rect.centerex - player.rect.centerx
        dy = enemy.rect.centerex - player.rect.centery
        nx, ny = normalize(dx, dy)

        knockback_strength = player.contact_knockback

        apply_impulse(player, -nx, -ny, knockback_strength)
        apply_impulse(enemy, nx, ny )
