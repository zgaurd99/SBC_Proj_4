import json
import pygame


class AnimationComponent:
    def __init__(self, sheet_path, json_path):
        self._sheet = pygame.image.load(sheet_path).convert_alpha()

        with open(json_path, "r") as f:
            data = json.load(f)

        # Slice all frames from sheet
        self._frames = []
        for frame_data in data["frames"]:
            f = frame_data["frame"]
            surface = self._sheet.subsurface(
                pygame.Rect(f["x"], f["y"], f["w"], f["h"])
            )
            duration = frame_data["duration"]  # ms
            self._frames.append((surface, duration))

        # Map tag name -> list of frame indices
        self._tags = {}
        for tag in data["meta"]["frameTags"]:
            name = tag["name"]
            self._tags[name] = list(range(tag["from"], tag["to"] + 1))

        self._state = None
        self._frame_indices = []
        self._current_index = 0
        self._timer = 0.0

        # Set default state to first tag
        first_tag = data["meta"]["frameTags"][0]["name"]
        self.set_state(first_tag)

    def set_state(self, name):
        if name == self._state:
            return

        if name not in self._tags:
            return

        self._state = name
        self._frame_indices = self._tags[name]
        self._current_index = 0
        self._timer = 0.0

    def update(self, delta_time):
        # delta_time in ms to match Aseprite durations
        if not self._frame_indices:
            return

        self._timer += delta_time

        _, duration = self._frames[self._frame_indices[self._current_index]]

        if self._timer >= duration:
            self._timer -= duration
            self._current_index = (self._current_index + 1) % len(self._frame_indices)

    @property
    def current_frame(self):
        index = self._frame_indices[self._current_index]
        surface, _ = self._frames[index]
        return surface
    
    @property
    def frame_size(self):
        surface, _ = self._frames[0]
        return surface.get_width(), surface.get_height()