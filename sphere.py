from __future__ import annotations

from itertools import chain
from math import pi as PI, ceil, sin, cos
from typing import Optional, List, Tuple

from pyglet.gl import GL_TRIANGLES
from pyglet.graphics.vertexdomain import VertexList

from misc import Color, DrawContext


class Sphere:
    def __init__(
        self,
        ctx: DrawContext,
        base_color: Color,
        radius: float,
        *,
        stacks: Optional[int] = None,
        sectors: Optional[int] = None,
    ):
        self._ctx = ctx
        self._radius: float = radius
        self._color = base_color
        stacks = stacks or ceil(radius * 1.25)
        self._stacks: int = max(14, stacks)
        sectors = sectors or ceil(radius * 1.25)
        self._sectors: int = max(14, sectors)
        self._vertices: Optional[VertexList] = None
        self._frame_vertices: Optional[VertexList] = None

    def draw_at(self, x: float, y: float, z: float, wireframe: bool = False):
        sector_step = 2 * PI / self._sectors
        stack_step = PI / self._stacks
        # generate frame vertices
        frame_vertices: List[List[Tuple[float, float, float]]] = []
        for i in range(1, self._stacks):
            stack_vertices: List[Tuple[float, float, float]] = []
            stack_angle = PI / 2 - i * stack_step
            pxz = self._radius * cos(stack_angle)
            py = self._radius * sin(stack_angle) + y

            for j in range(1, self._sectors+1):
                sector_angle = j * sector_step
                px = x + pxz * cos(sector_angle)
                pz = z + pxz * -sin(sector_angle)
                stack_vertices.append((px, py, pz))
            # duplicate the first sector of a stack, and stick it at the end,
            # for the walls to connect last sector with the first properly
            stack_vertices.append(stack_vertices[0])
            frame_vertices.append(stack_vertices)
        # use frame vertices to generate a list of triangle vertices
        colors: List[float] = []
        vertices: List[float] = []
        # first, the north pole - center vertex (pole) is fixed, so all we need is a trangle fan
        pole = (x, y + self._radius, z)
        for v1, v2 in zip(frame_vertices[0], frame_vertices[0][1:]):
            vertices.extend(chain(pole, v1, v2))
            colors.extend(self._color * 3)
        # then the walls, two triangles per stack-sector
        # v1---v2
        # || / ||
        # v3---v4
        # v1 -> v3 -> v2 and v4 -> v2 -> v3
        for frame1, frame2 in zip(frame_vertices, frame_vertices[1:]):
            for v1, v2, v3, v4 in zip(frame1, frame1[1:], frame2, frame2[1:]):
                vertices.extend(chain(v1, v3, v2, v4, v2, v3))
                colors.extend(self._color * 6)
        # finally, the south pole - same deal as at the beginning
        pole = (x, y - self._radius, z)
        for v1, v2 in zip(frame_vertices[-1], frame_vertices[-1][1:]):
            vertices.extend(chain(pole, v2, v1))
            colors.extend(self._color * 3)
        # move the vertices
        if self._vertices is None:
            self._vertices = self._ctx.main_batch.add(
                len(vertices) // 3, GL_TRIANGLES, None, ("v3f", vertices), ("c4B", colors)
            )
        else:
            self._vertices.vertices[:] = vertices
            self._vertices.colors[:] = colors
        if wireframe:
            if self._frame_vertices is None:
                colors = [0, 0, 0, 255] * (len(vertices) // 3)  # use black
                self._frame_vertices = self._ctx.main_batch.add(
                    len(vertices) // 3,
                    GL_TRIANGLES,
                    self._ctx.wireframe_group,
                    ("v3f", vertices),
                    ("c4B", colors),
                )
            else:
                self._frame_vertices.vertices[:] = vertices
        elif self._frame_vertices is not None:
            self._frame_vertices.delete()
            self._frame_vertices = None

    def set_color(self, color: Color):
        self._color = color
        if self._vertices is not None:
            self._vertices.colors[:] = [*color] * self._vertices.get_size()
