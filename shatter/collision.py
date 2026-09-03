from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import IntFlag
from itertools import combinations
from typing import Literal

from .linear import Vec2


def _nop(collision: Collision): ...


@dataclass
class Collider:
    layer: int
    mask: int

    def __post_init__(self):
        self.uid: int = id(self)
        self.type: type[Collider] = type(self)
        self.on_collision_enter: Callable[[Collision], None] = _nop
        self.on_collision_exit: Callable[[Collision], None] = _nop
        self.on_collision: Callable[[Collision], None] = _nop


@dataclass(slots=True)
class Collision:
    a: Collider
    b: Collider
    normal: Vec2
    depth: float

    def __bool__(self) -> Literal[True]:
        return True

    def reversed(self) -> Collision:
        return Collision(self.b, self.a, -self.normal, self.depth)


@dataclass(slots=True)
class CollisionHistory:
    collider: Collider
    collision: Collision
    age: int
    frame: int

    def update(self, collision: Collision, frame: int):
        self.collision = collision
        self.frame = frame


@dataclass(slots=True)
class Line(Collider):
    center: Vec2
    tangent: Vec2
    length: float

    @property
    def normal(self) -> Vec2:
        return Vec2.new(-self.tangent.y, self.tangent.x)

    @property
    def radius(self) -> float:
        return self.length / 2.0

    @property
    def start(self) -> Vec2:
        return self.center - self.tangent * (0.5 * self.length)

    @property
    def end(self) -> Vec2:
        return self.center + self.tangent * (0.5 * self.length)


@dataclass(slots=True)
class Plane(Collider):
    normal: Vec2
    offset: float


@dataclass(slots=True)
class Circle(Collider):
    center: Vec2
    radius: float


class Polygon(Collider):
    points: tuple[Vec2, ...]


type CollisionFunction = Callable[..., Literal[False] | Collision]


def plane_circle_collision(a: Plane, b: Circle) -> Literal[False] | Collision:
    depth = b.radius - (a.normal.dot(b.center) - a.offset)
    if depth < 0:  # Circle is 'infront' of plane
        return False
    return Collision(a, b, a.normal, depth)


def circle_plane_collision(a: Circle, b: Plane) -> Literal[False] | Collision:
    if collision := plane_circle_collision(b, a):
        collision.a, collision.b = a, b
        collision.normal = -collision.normal
        return collision
    return False


def line_circle_collision(a: Line, b: Circle) -> Literal[False] | Collision:
    diff = a.center - a.center
    length = abs(diff)
    along = a.tangent.dot(diff)
    nabla = along**2 - length**2 + b.radius**2

    if nabla < 0:
        return False  # Line never intersects circle

    sqrt_nabla = nabla**0.5
    h_length = a.radius
    d1 = -along + sqrt_nabla
    d2 = -along - sqrt_nabla

    if h_length < abs(d1) and h_length < abs(d2) and b.radius < length:
        # Line segment never intersects circle and is outside of it
        return False

    normal = a.normal
    separation = -normal @ diff
    abs_sep = abs(separation)
    sign = separation / abs_sep

    return Collision(a, b, sign * normal, b.radius - abs_sep)


def circle_line_collision(a: Circle, b: Line) -> Literal[False] | Collision:
    if collision := line_circle_collision(b, a):
        collision.a, collision.b = a, b
        collision.normal = -collision.normal
        return collision
    return False


def circle_circle_collision(a: Circle, b: Circle) -> Literal[False] | Collision:
    diff = b.center - a.center
    length = diff.length_sqr
    if (a.radius**2 + b.radius**2) < length:  # Circles are too far apart
        return False
    sep = a.radius + b.radius - length**0.5
    return Collision(a, b, diff.normalised(), sep)


def unimplemented_collision(a: Collider, b: Collider):
    raise NotImplementedError(f"No collision function implemented for {type(a)} and {type(b)}")


_COLLISIONS_FUNCTIONS: dict[tuple[type[Collider], type[Collider]], CollisionFunction] = {
    (Circle, Plane): circle_plane_collision,
    (Plane, Circle): plane_circle_collision,
    (Circle, Line): circle_line_collision,
    (Line, Circle): line_circle_collision,
    (Circle, Circle): circle_circle_collision,
}


def collide(a: Collider, b: Collider) -> Literal[False] | Collision:
    func = _COLLISIONS_FUNCTIONS.get((a.type, b.type), unimplemented_collision)
    return func(a, b)


class World:
    def __init__(self) -> None:
        self.colliders: dict[int, Collider] = {}
        self.collisions: dict[tuple[int, int], CollisionHistory] = {}
        self.frame: int = 0

    def add_collider(self, collider: Collider):
        if collider.uid in self.colliders:
            return
        self.colliders[collider.uid] = collider

    def rem_collider(self, collider: Collider):
        if collider.uid not in self.colliders:
            return
        self.colliders.pop(collider.uid)

    def update(self):
        self.frame += 1
        # TODO: Broad Phase
        self.narrow_phase_collisions()
        # TODO: For a physics eninge we would want to solve constraints in here somewhere
        self.handle_collisions()

    def narrow_phase_collisions(self):
        for a, b in combinations(self.colliders.values(), 2):
            from_a = a.mask & b.layer
            from_b = b.mask & a.layer
            if not (from_a or from_b) or not (collision := collide(a, b)):
                continue  # No collision occurred or the two object's don't care about each other

            if from_a:
                key = (a.uid, b.uid)
                if key in self.collisions:
                    history = self.collisions[key]
                    history.update(collision, self.frame)
                else:
                    self.collisions[key] = CollisionHistory(a, collision, self.frame, self.frame)

            if from_b:
                key = (b.uid, a.uid)
                if key in self.collisions:
                    self.collisions[key].update(collision.reversed(), self.frame)
                else:
                    self.collisions[key] = CollisionHistory(
                        b, collision.reversed(), self.frame, self.frame
                    )

    def handle_collisions(self):
        for key, history in tuple(self.collisions.items()):
            if history.age == self.frame:
                history.collider.on_collision_enter(history.collision)
            history.collider.on_collision(history.collision)
            if history.frame != self.frame:
                history.collider.on_collision_exit(history.collision)
                self.collisions.pop(key)


class CollisionLayers(IntFlag):
    NONE = 0b0000_0000
    GEOMETRY = 0b0000_0001
    PLAYER = 0b0000_0010
    MIRROR = 0b0000_0100
    ORB = 0b0000_1000
    GEMS = 0b0001_0000
    ORB_HAZARD = 0b0010_0000
    PLAYER_HAZARD = 0b0100_0000

    PLAYER_MASK = GEOMETRY | ORB | PLAYER_HAZARD
    ORB_REFLECTIVE = GEOMETRY | MIRROR
    ORB_MASK = ORB_REFLECTIVE | GEMS | ORB_HAZARD
