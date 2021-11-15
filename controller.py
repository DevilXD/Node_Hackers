from __future__ import annotations


class Controller:
    def __init__(self):
        self._map = {}

    def on_key_press(self, key, modifiers):
        self._map[key] = True

    def on_key_release(self, key, modifiers):
        self._map[key] = False

    def __getitem__(self, key):
        return self._map.get(key, False)
