from arcade import SpriteList

from shatter.collision import World
from shatter.context import GameLayers


class Piece:

    def attach(self, world: World, layers: GameLayers): ...
    def detach(self, world: World, layers: GameLayers): ...
