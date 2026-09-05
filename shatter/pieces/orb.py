from arcade import Sprite, SpriteList

from resources import get_texture
from shatter.collision import Circle, Collision, CollisionLayers, World
from shatter.context import GameLayers
from shatter.linear import Vec2
from shatter.pieces.piece import Piece


class Orb(Piece):
    STARTING_POTENTIAL: float = 600.0
    ORB_RADIUS = 48
    ORB_HEIGHT = 48
    SPRITE_TEXTURE = "Orb_Body"
    SHADOW_TEXTURE = "Orb_Shadow"

    def __init__(self, position: Vec2) -> None:
        self.sprite: Sprite = Sprite(get_texture(Orb.SPRITE_TEXTURE), 1.0, position.x, position.y)
        self.sprite.depth = 48
        self.shadow: Sprite = Sprite(get_texture(Orb.SHADOW_TEXTURE), 1.0, position.x, position.y)
        self.collider: Circle = Circle(
            CollisionLayers.ORB, CollisionLayers.ORB_MASK, position, Orb.ORB_RADIUS
        )
        self.collider.on_collision_enter = self.on_collision_enter

        self.velocity: Vec2 = Vec2(Orb.STARTING_POTENTIAL, 0.0)
        self.potential: float = Orb.STARTING_POTENTIAL

    def attach(self, world: World, layers: GameLayers):
        world.add_collider(self.collider)
        layers.shadows.append(self.shadow)
        layers.pieces.append(self.sprite)

    def detach(self, world: World, layers: GameLayers):
        world.rem_collider(self.collider)
        layers.pieces.remove(self.sprite)
        layers.shadows.remove(self.shadow)

    def update(self, dt: float):
        self.collider.center += self.velocity * dt
        self.sprite.position = self.shadow.position = self.collider.center.x, self.collider.center.y

    def on_collision_enter(self, collision: Collision):
        # Our collider is always collider 'a' so we check collider 'b' for what layer we are on
        layer = collision.b.layer
        if layer & CollisionLayers.ORB_REFLECTIVE:
            # TODO: MAKE JUICEY (HIT STOP, SCREEN SHAKE ETC)
            along = collision.normal.dot(self.velocity)
            if along > 0:
                # Move Orb to surface of object being collided with, and flip velocity parallel with collision
                self.collider.center -= collision.normal * collision.depth
                self.velocity -= collision.normal * (2 * along)
        elif layer & CollisionLayers.ORB_HAZARD:
            ...  # TODO