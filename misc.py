from typing import Union, Tuple, TypeVar

from pyglet.graphics import Group, Batch
from pyglet.gl import glPolygonMode, GL_FRONT, GL_FILL, GL_LINE


_N1 = TypeVar("_N1", int, float)
_N2 = TypeVar("_N2", int, float)
_N3 = TypeVar("_N3", int, float)

Color = Tuple[int, int, int, int]


def constrain(value: _N1, min_value: _N2, max_value: _N3) -> Union[_N1, _N2, _N3]:
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    return value


class Wireframe(Group):
    def set_state(self):
        glPolygonMode(GL_FRONT, GL_LINE)

    def unset_state(self):
        glPolygonMode(GL_FRONT, GL_FILL)


class DrawContext:
    def __init__(self):
        self._ctx = self
        self.main_batch = Batch()
        self.wireframe_group = Wireframe()
