from arcade import Sprite, SpriteList, draw_circle_outline
from arcade.future.input import ActionState
from math import atan2, degrees
from arcade.types import Point2

from resources import get_spritesheet, get_texture
from shatter.collision import Circle, World, Line, CollisionLayers
from shatter.linear import Vec2
from shatter.context import GameLayers, Actions, Axis, get_axis
from shatter.pieces.piece import Piece


class Player(Piece):
    SPEED = 100

    def __init__(self) -> None:
        sprite_sheet = get_spritesheet("Player_Body")
        self.frames = sprite_sheet.get_texture_grid((16, 16), 6, 6)
        self.sprite: Sprite = Sprite(self.frames[0], 3)
        self.sprite.depth = 24
        self.shadow: Sprite = Sprite(get_texture("Player_Shadow"))
        self.collider: Circle = Circle(CollisionLayers.PLAYER, CollisionLayers.PLAYER_HAZARD, Vec2(), 48)
        self.mirror: Mirror = Mirror()

        self.hozirontal: int = 0
        self.vertical: int = 0

    def attach(self, world: World, layers: GameLayers):
        world.add_collider(self.collider)
        layers.shadows.append(self.shadow)
        layers.pieces.append(self.sprite)
        self.mirror.attach(world, layers)

    def detach(self, world: World, layers: GameLayers):
        layers.pieces.remove(self.sprite)
        layers.shadows.remove(self.shadow)
        world.rem_collider(self.collider)
        self.mirror.detach(world, layers)

    def update(self, dt: float):
        h = get_axis(Axis.MoveHorizontal)
        v = get_axis(Axis.MoveVertical)
        motion = Vec2(h + v, v - h)
        if motion.length_sqr > 0:
            motion.normalise()

        self.sprite.scale_x = 3.0 if h >= 0 else -3.0

        velocity = motion * Player.SPEED * dt
        self.collider.center += velocity
        self.sprite.position = self.collider.center.frozen
        self.shadow.position = self.collider.center.frozen

        self.mirror.normal = (self.mirror.position - self.collider.center)

        self.mirror.update()

    def on_action(self, action: str, pressed: ActionState):
        pass

    def on_mouse_motion(self, x: float, y: float):
        self.mirror.position = (x, y)

    @property
    def position(self) -> Vec2:
        return self.collider.center

    @position.setter
    def position(self, pos: Point2 | float):
        self.collider.center.xy = pos
        self.shadow.position = self.collider.center.frozen
        self.sprite.position = self.collider.center.frozen


class Mirror(Piece):

    def __init__(self) -> None:
        sprite_sheet = get_spritesheet("Mirror")
        frames = sprite_sheet.get_texture_grid((96, 96), 16, 32)
        self.shadow_textures = frames[:16]
        self.body_textures = frames[16:]

        self.sprite: Sprite = Sprite(self.body_textures[2])
        self.sprite.depth = 48
        self.shadow: Sprite = Sprite(self.shadow_textures[2])
        # TODO: Make polygon
        self.collider: Line = Line(CollisionLayers.MIRROR, CollisionLayers.NONE, Vec2(), Vec2(1.0, 0.0), 64.0)

    def attach(self, world: World, layers: GameLayers):
        world.add_collider(self.collider)
        layers.shadows.append(self.shadow)
        layers.pieces.append(self.sprite)

    def detach(self, world: World, layers: GameLayers):
        layers.pieces.remove(self.sprite)
        layers.shadows.remove(self.shadow)
        world.rem_collider(self.collider)

    def update(self): ...

    @property
    def position(self) -> Vec2:
        return self.collider.center

    @position.setter
    def position(self, pos: Point2 | float):
        self.collider.center.xy = pos
        self.shadow.position = self.collider.center.frozen
        self.sprite.position = self.collider.center.frozen

    @property
    def normal(self) -> Vec2:
        return self.collider.normal

    @normal.setter
    def normal(self, norm: Vec2):
        if norm.length_sqr > 0.0:
            norm.normalise()
            self.collider.normal.xy = norm
            angle = degrees(atan2(norm.y, norm.x)) + 45
            frame = round(angle * 8 / 180)

            self.sprite.texture = self.body_textures[frame]
            self.shadow.texture = self.shadow_textures[frame]