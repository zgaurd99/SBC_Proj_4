import io
import pygame
import cairosvg


class AssetLoader:
    def __init__(self, manifest: dict):
        self.surfaces = {}
        self._load(manifest)

    def _load(self, manifest: dict):
        for key, config in manifest.items():
            path = config["path"]
            width, height = config["size"]

            with open(path, "r") as f:
                svg_data = f.read()

            import re

            # Extract native dimensions
            w_match = re.search(r'<svg[^>]*width="([^"]+)"', svg_data)
            h_match = re.search(r'<svg[^>]*height="([^"]+)"', svg_data)

            native_w = float(w_match.group(1)) if w_match else width
            native_h = float(h_match.group(1)) if h_match else height

            scale_x = width / native_w
            scale_y = height / native_h

            # Replace svg tag with scaled version
            svg_data = re.sub(
                r'<svg([^>]*?)width="[^"]*"([^>]*?)height="[^"]*"([^>]*?)>',
                f'<svg\\1width="{width}"\\2height="{height}"\\3><g transform="scale({scale_x},{scale_y})">',
                svg_data,
                count=1
            )
            svg_data = svg_data.replace("</svg>", "</g></svg>")

            buffer = io.BytesIO()
            cairosvg.svg2png(
                bytestring=svg_data.encode("utf-8"),
                write_to=buffer,
                output_width=width,
                output_height=height
            )

            buffer.seek(0)
            surface = pygame.image.load(buffer, "_.png").convert_alpha()
            self.surfaces[key] = surface

    def get(self, name: str) -> pygame.Surface | None:
        surface = self.surfaces.get(name)
        if surface is None:
            print(f"[AssetLoader] WARNING: '{name}' not found")
        return surface