from __future__ import annotations

from typing import Optional, Tuple

from pyglet.gl import glTranslatef, glScalef, glRotatef

from misc import constrain


class Camera:
    """
    A simple 3D camera that allows for moving and looking around.
    """
    def __init__(self, movement_speed=1, rotation_speed=0.1, min_zoom=1, max_zoom=4):
        assert min_zoom <= max_zoom, "Minimum zoom must not be greater than maximum zoom"
        # position
        self._tx = 0
        self._ty = 0
        self._tz = 0
        self._tspeed = movement_speed
        self._tlimit: Tuple[Optional[float], Optional[float], Optional[float]] = (None, None, None)
        # rotation - degrees
        self._pitch = 0
        self._yaw = 0
        self._rspeed = rotation_speed
        self._rlimit: Tuple[Optional[float], Optional[float], Optional[float]] = (None, None, None)
        # zoom
        self._zoom = 1
        self._max_zoom = max_zoom
        self._min_zoom = min_zoom

    def zoom(self, value):
        self._zoom = constrain(self._zoom + value, self._min_zoom, self._max_zoom)

    def move(self, dx, dy, dz):
        speed = self._tspeed / self._zoom
        self._tx += speed * dx
        self._ty += speed * dy
        self._tz += speed * dz

    def rotate(self, yaw, pitch, roll):
        # rotate the camera relative to the current scene's rotation and projection
        speed = self._rspeed
        self._pitch += speed * pitch
        self._yaw += speed * yaw

    def begin(self):
        # Set the current camera offset so you can draw your scene.
        # Translate using the zoom and the offset.
        glTranslatef(-self._tx, -self._ty, -self._tz)
        # Rotate
        glRotatef(self._pitch, -1, 0, 0)
        glRotatef(self._yaw, 0, 1, 0)
        # Scale by zoom level.
        glScalef(self._zoom, self._zoom, self._zoom)

    def end(self):
        # Reverse scale.
        r_scale = 1 / self._zoom
        glScalef(r_scale, r_scale, r_scale)
        # Reverse rotate.
        glRotatef(self._yaw, 0, -1, 0)
        glRotatef(self._pitch, 1, 0, 0)
        # Reverse translate.
        glTranslatef(self._tx, self._ty, self._tz)

    def __enter__(self):
        self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end()
