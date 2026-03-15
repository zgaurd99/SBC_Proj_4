class EntityRegistry:
    def __init__(self):
        self._entities = []

    def register(self, entity, role=None):
        entity.role = role
        self._entities.append(entity)

    def get_by_role(self, role):
        return next(
            (e for e in self._entities if getattr(e, "role", None) == role and e.alive),
            None
        )

    def update(self, delta_time):
        for entity in self._entities[:]:
            entity.update(delta_time)
            if not entity.alive:
                self._entities.remove(entity)

    def all(self):
        return list(self._entities)

    def clear(self):
        self._entities.clear()