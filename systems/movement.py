import math

from entities import entity

def movement_system(entity, input_vector=None, world_bounds=None, delta_time = 0):
    """
    Handles movement for an entity.
    input_vector: (dx, dy) or None
    world_bounds: (left, top, right, bottom) or None
    """

    # --- 1. Input Movement ---
    if input_vector:
        dx, dy = input_vector
        length = math.hypot(dx, dy)

        if length != 0:
            dx /= length
            dy /= length

            entity.rect.x += dx * entity.get_stat("speed") * delta_time
            entity.rect.y += dy * entity.get_stat("speed") * delta_time

    # --- 2. Apply Velocity (Impulse / Knockback / Lunge) ---
    entity.rect.x += entity.velocity.x * delta_time
    entity.rect.y += entity.velocity.y * delta_time

    # --- 3. Decay Velocity ---
    entity.velocity *= entity.knockback_decay ** (delta_time / 1000)

    # --- 4. Clamp to World ---
    if world_bounds:
        left, top, right, bottom = world_bounds

        entity.rect.x = max(left, min(entity.rect.x, right - entity.rect.width))
        entity.rect.y = max(top, min(entity.rect.y, bottom - entity.rect.height))