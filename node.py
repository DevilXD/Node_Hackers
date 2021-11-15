from __future__ import annotations

from sphere import Sphere
from misc import Color, DrawContext


class Node:
    def __init__(self, ctx: DrawContext, name: str, color: Color):
        self._ctx = ctx
        self.name: str = name
        self._sphere = Sphere(ctx, color, 1)
        self.draw()

    def draw(self):
        self._sphere.draw_at(0, 0, 0, wireframe=True)
