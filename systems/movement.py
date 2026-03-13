import math
from entities import entity

def movement_system(entity, input_vector=None, world_bounds=None, delta_time=0):

    dt = delta_time / 1000

    if input_vector:
        dx, dy = input_vector
        length = math.hypot(dx, dy)

        if length != 0:
            dx /= length
            dy /= length

            speed = entity.get_stat("speed")

            entity.rect.x += dx * speed * dt * 200
            entity.rect.y += dy * speed * dt * 200

    entity.rect.x += entity.velocity.x * dt
    entity.rect.y += entity.velocity.y * dt

    entity.velocity *= entity.knockback_decay

    if world_bounds:
        left, top, right, bottom = world_bounds
        entity.rect.x = max(left, min(entity.rect.x, right - entity.rect.width))
        entity.rect.y = max(top, min(entity.rect.y, bottom - entity.rect.height))