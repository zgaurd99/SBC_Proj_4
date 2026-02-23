import math
import pygame

def distance_sq(x1, y1, x2, y2):
    """
    Basic distance math
    """
    dx = x2 - x1
    dy = y2 - y1
    return dx * dx + dy * dy

def normalize(dx, dy):
    """
    normalization of diatnce
    """
    length = math.hypot(dx, dy)
    if length == 0:
        return 0, 0
    return dx / length, dy / length

def circle_overlap(cx1, cy1, r1, cx2, cy2, r2):
    """
    Returns True if two circles overlap.
    """
    dist_sq = distance_sq(cx1, cy1, cx2, cy2)
    min_dist = r1 + r2
    return dist_sq < min_dist * min_dist

def circle_overlap_data(cx1, cy1, r1, cx2, cy2, r2):
    """
    Returns:
        (overlapping: bool,
         nx, ny: normalized direction from 1 to 2,
         overlap_amount)
    """
    dx = cx2 - cx1
    dy = cy2 - cy1

    dist_sq = dx * dx + dy * dy
    min_dist = r1 + r2

    if dist_sq >= min_dist * min_dist or dist_sq == 0:
        return False, 0, 0, 0

    dist = math.sqrt(dist_sq)
    nx = dx / dist
    ny = dy / dist
    overlap = min_dist - dist

    return True, nx, ny, overlap

def resolve_circle_overlap(entity_a, entity_b, weight_a=0.5, weight_b=0.5):
    """
    Pushes two entities apart based on overlap.
    """
    cx1 = entity_a.rect.centerx
    cy1 = entity_a.rect.centery
    cx2 = entity_b.rect.centerx
    cy2 = entity_b.rect.centery

    overlapping, nx, ny, overlap = circle_overlap_data(
        cx1, cy1, entity_a.core_radius,
        cx2, cy2, entity_b.core_radius
    )

    if not overlapping:
        return False

    entity_a.rect.x -= nx * overlap * weight_a
    entity_a.rect.y -= ny * overlap * weight_a

    entity_b.rect.x += nx * overlap * weight_b
    entity_b.rect.y += ny * overlap * weight_b

    return True

def apply_impulse(entity, nx, ny, strength):
    """
    Applies velocity impulse in direction (nx, ny) for smoother animation.
    """
    entity.velocity += pygame.Vector2(nx, ny) * strength