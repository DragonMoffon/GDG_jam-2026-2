"""
A Rotationless Iterative 2D Physics Engine
"""

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(slots=True)
class Vec2:
    x: float
    y: float

    def __getitem__(self, key: int):
        match key:
            case 0:
                return self.x
            case 1:
                return self.y
        raise KeyError("Vec2 only accepts idx 0 or 1 for x and y respectively")

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def __len__(self) -> int:
        return 2

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y))


@dataclass
class Shape:
    pass


@dataclass(slots=True)
class Body:
    m: float  # Mass
    m_inv: float  # Inverse Mass
    p: Vec2  # Position
    v: Vec2  # Velocity
    f: Vec2  # Force
    b: Vec2  # Bias
    s: Shape  # Shape


class World:
    pass
