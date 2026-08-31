from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Literal

from .linear import Vec2


@dataclass
class Shape:
    def __post_init__(self):
        self.type = ShapeType(type(self))


@dataclass(slots=True)
class Line(Shape):
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
        return self.center - 0.5 * self.length * self.tangent

    @property
    def end(self) -> Vec2:
        return self.center + 0.5 * self.length * self.tangent


@dataclass(slots=True)
class Circle(Shape):
    center: Vec2
    radius: float


class Polygon(Shape):
    pass

class ShapeType(Enum):
    LINE = Line
    CIRCLE = Circle
    POLYGON = Polygon

@dataclass(slots=True)
class Collision:
    normal: Vec2
    depth: float

    def reverse(self):
        return Collision(-self.normal, self.depth)


type CollisionFunction = Callable[..., Literal[False] | Collision]


def line_circle_collision(line: Line, circle: Circle) -> Literal[False] | Collision:
    diff = line.center - circle.center
    length = abs(diff)
    along = line.tangent.dot(diff)
    nabla = along**2 - length**2 + circle.radius**2

    if nabla < 0:
        return False  # Line never intersects circle

    sqrt_nabla = nabla**0.5
    h_length = line.radius
    d1 = -along + sqrt_nabla
    d2 = -along - sqrt_nabla

    if h_length < abs(d1) and h_length < abs(d2) and circle.radius < length:
        # Line segment never intersects circle and is outside of it
        return False

    normal = line.normal
    separation = -normal @ diff
    abs_sep = abs(separation)
    sign = separation / abs_sep

    return Collision(sign * normal, circle.radius - abs_sep)


def circle_line_collision(circle: Circle, line: Line) -> Literal[False] | Collision:
    if collision := line_circle_collision(line, circle):
        return collision.reverse()
    return False


def unimplemented_collision(a: Shape, b: Shape):
    raise NotImplementedError(f"No collision function implemented for {type(a)} and {type(b)}")

def collide(a: Shape, b: Shape) -> Literal[False] | Collision:
    match (a.type, b.type):
        case ShapeType.LINE, ShapeType.CIRCLE:
            return line_circle_collision(a, b) # type: ignore
        case ShapeType.CIRCLE, ShapeType.LINE:
            return circle_line_collision(a, b) # type: ignore
    return False
