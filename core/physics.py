import math
import pygame

def distance_sq(x1, y1, x2, y2):
    # returns the squared distance between two points
    # using squared distance avoids a costly sqrt, useful for comparisons where exact distance isn't needed
    """Basic distance math"""
    dx = x2 - x1
    dy = y2 - y1
    return dx * dx + dy * dy

def normalize(dx, dy):
    # converts a direction vector into a unit vector (length of 1)
    # used whenever we need a direction without caring about magnitude
    """Normalization of distance"""
    length = math.hypot(dx, dy)
    if length == 0:
        return 0, 0  # avoid division by zero, return zero vector if no direction
    return dx / length, dy / length

def circle_overlap(cx1, cy1, r1, cx2, cy2, r2):
    # checks if two circles are overlapping using squared distance to avoid sqrt
    # returns True if the circles intersect, False otherwise
    """Returns True if two circles overlap."""
    dist_sq = distance_sq(cx1, cy1, cx2, cy2)
    min_dist = r1 + r2
    return dist_sq < min_dist * min_dist  # compare squared values directly for efficiency

def circle_overlap_data(cx1, cy1, r1, cx2, cy2, r2):
    # extended version of circle_overlap that also returns overlap details
    # useful when you need to know not just if circles overlap, but by how much and in which direction
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

    # early exit if circles are not overlapping or centers are exactly the same
    if dist_sq >= min_dist * min_dist or dist_sq == 0:
        return False, 0, 0, 0

    dist = math.sqrt(dist_sq)
    nx = dx / dist  # normalized x direction from circle 1 to circle 2
    ny = dy / dist  # normalized y direction from circle 1 to circle 2
    overlap = min_dist - dist  # how deeply the two circles are intersecting
    return True, nx, ny, overlap

def resolve_circle_overlap(entity_a, entity_b, weight_a=0.5, weight_b=0.5):
    # pushes two overlapping entities apart based on their overlap amount and assigned weights
    # weight_a and weight_b control how much each entity is pushed, default is equal split
    """Pushes two entities apart based on overlap."""
    cx1 = entity_a.rect.centerx
    cy1 = entity_a.rect.centery
    cx2 = entity_b.rect.centerx
    cy2 = entity_b.rect.centery

    overlapping, nx, ny, overlap = circle_overlap_data(
        cx1, cy1, entity_a.core_radius,
        cx2, cy2, entity_b.core_radius
    )

    if not overlapping:
        return False  # nothing to resolve, entities are not touching

    # push each entity away from the other proportional to their weight
    entity_a.rect.x -= nx * overlap * weight_a
    entity_a.rect.y -= ny * overlap * weight_a
    entity_b.rect.x += nx * overlap * weight_b
    entity_b.rect.y += ny * overlap * weight_b
    return True

def apply_impulse(entity, nx, ny, strength):
    # adds a velocity kick to an entity in the given direction scaled by strength
    # used for knockback, explosions, or any sudden push effect
    """Applies velocity impulse in direction (nx, ny) for smoother animation."""
    entity.velocity += pygame.Vector2(nx, ny) * strength