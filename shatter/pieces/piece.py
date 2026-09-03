from arcade import SpriteList

from shatter.collision import World
from shatter.layers import GameLayers


class Piece:

    def attach(self, world: World, layers: GameLayers): ...
    def dettatch(self, world: World, layers: GameLayers): ...