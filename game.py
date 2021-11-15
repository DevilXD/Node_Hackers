from __future__ import annotations

import pyglet
from pyglet.gl import glTranslatef, glRotatef, glEnable, GL_CULL_FACE
from pyglet.window import mouse, key

from node import Node
from camera import Camera
from misc import DrawContext
from controller import Controller


class NodeHackers:
    def __init__(self):
        self.event_loop = pyglet.app.EventLoop()
        self.clock = pyglet.clock.Clock()
        self.event_loop.clock = self.clock
        self.window = pyglet.window.Window(1280, 720, caption="In Development")
        self.window.projection = pyglet.window.Projection3D()
        self.camera = Camera(0.5)
        self._ctx = DrawContext()
        self._cnt = Controller()
        self._fps: int = 0

        self.window.event(self.on_draw)
        self.window.event(self.on_close)
        self.window.event(self.on_mouse_drag)
        self.window.event(self.on_mouse_scroll)
        self.window.push_handlers(self._cnt)
        glEnable(GL_CULL_FACE)
        glTranslatef(0, 0, -3)
        glRotatef(40, 1, 0, 0)
        self.fps = 30
        self.setup()  # pass control to further setup

    def run(self):
        """
        Main run method. This will block until the game exits.
        """
        self.event_loop.run()

    def request_exit(self):
        """
        When called, requests the main run method to safely exit the app.
        """
        self.event_loop.exit()

    def on_close(self):
        self.event_loop.exit()

    def setup(self):
        self._node = Node(self._ctx, "Access Point", (255, 255, 255, 255))

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps: int):
        self.clock.unschedule(self.update)
        if fps > 0:
            self.clock.schedule_interval(self.update, 1 / fps)
        self._fps = fps

    def on_draw(self):
        self.window.clear()
        with self.camera:
            self._ctx.main_batch.draw()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.RIGHT:
            self.camera.rotate(dx, dy, 0)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.zoom(scroll_y)

    def update(self, dt):
        """
        Main update method. This is called every ``1 / FPS`` seconds, to update the game state.
        """
        if self._cnt[key.W]:
            self.camera.move(0, 0, 0.1)
        elif self._cnt[key.A]:
            self.camera.move(0.1, 0, 0)
        elif self._cnt[key.S]:
            self.camera.move(0, 0, -0.1)
        elif self._cnt[key.D]:
            self.camera.move(-0.1, 0, 0)
