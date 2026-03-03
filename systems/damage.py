import math

from core.physics import circle_overlap, normalize, apply_impulse

def damage_system(player, enemies, delta_time):
    """
    Handles player taking contact damage from enemies.
    Includes knockback + stun.
    """

    for enemy in enemies:

        # --- 1. Collision Check ---
        if not circle_overlap(
            player.rect.centerx, player.rect.centery, player.core_radius,
            enemy.rect.centerx, enemy.rect.centery, enemy.core_radius
        ):
            continue

        # --- 2. Invulnerability Check ---
        if player.invuln_timer > 0:
            continue

        # --- 3. Enemy Hit Cooldown ---
        if enemy.hit_timer > 0:
            continue

        # --- 4. Apply Dealer-Based Damage ---
        player.take_damage(enemy)

        # Reset cooldown timers
        enemy.hit_timer = enemy.get_stat("attack_speed")
        player.invuln_timer = player.invulnerability_duration

        # --- 5. Knockback Calculation ---
        dx = enemy.rect.centerx - player.rect.centerx
        dy = enemy.rect.centery - player.rect.centery

        nx, ny = normalize(dx, dy)

        # If perfectly overlapping, fallback direction
        if nx == 0 and ny == 0:
            # Use enemy movement direction
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            nx, ny = normalize(dx, dy)

        # If STILL zero (rare), random small direction
        if nx == 0 and ny == 0:
            import random
            angle = random.uniform(0, 2 * math.pi)
            nx = math.cos(angle)
            ny = math.sin(angle)

        Rp = player.get_stat("rigidity")
        Re = enemy.get_stat("rigidity")
        base_force = 30

        Rt = Rp + Re
        if Rt == 0:
            continue

        Wp = Re / Rt
        We = Rp / Rt

        apply_impulse(player, -nx, -ny, base_force * Wp)
        apply_impulse(enemy, nx, ny, base_force * We)

        # --- 6. Stun Calculation (Event-Based) ---
        base_stun = 0.1  # small contact stagger

        stun_duration = (
            base_stun
            * player.get_stat("stun_factor")
            * enemy.get_stat("stun_strength")
        )

        stun_duration = min(0.5, stun_duration)

        enemy.stun_timer = stun_duration