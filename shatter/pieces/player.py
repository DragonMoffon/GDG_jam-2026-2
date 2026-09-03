from arcade import Sprite, SpriteList, draw_circle_outline

from resources import get_texture
from shatter.collision import Collision, Circle, Line, World, CollisionLayers
from shatter.linear import Vec2
from shatter.layers import GameLayers
from shatter.pieces.piece import Piece


class Player(Piece):

    def __init__(self) -> None:
        self.sprite: Sprite
        self.shadow: Sprite
        self.collider: Circle
        self.mirror: Mirror = Mirror()

        self.hozirontal: int = 0
        self.vertical: int = 0

    def attach(self, world: World, layers: GameLayers):
        pass

class Mirror(Piece):

    def __init__(self) -> None:
        self.sprite: Sprite
        self.shadow: Sprite
        self.collider: Line # TODO: Make polygon

    def attach(self, world: World, layers: GameLayers):
        pass