from __future__ import annotations

from game import NodeHackers

import pyglet
pyglet.options['debug_gl'] = True
pyglet.options['debug_gl_trace'] = True


game = NodeHackers()
game.run()
