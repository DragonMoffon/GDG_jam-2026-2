from __future__ import annotations

from collections.abc import Iterator, Sequence
from math import atan2
from typing import Self, overload

type Point2 = Vec2 | tuple[float, float]
type Point3 = Vec3 | tuple[float, float, float]


class Vec2(Sequence[float]):
    __slots__ = ("x", "y")

    @overload
    def __init__(self, x: float, y: float) -> None: ...

    @overload
    def __init__(self, x: float) -> None:
        pass

    def __init__(self, x: float, y: float | None = None) -> None:
        self.x = x
        self.y = x if y is None else y

    @classmethod
    def new(cls, x: float, y: float) -> Self:
        vec = cls.__new__(cls)
        vec.x = x
        vec.y = y
        return vec

    @property
    def length(self) -> float:
        return abs(self)

    norm = length

    @property
    def radians(self) -> float:
        return atan2(self.y, self.x)

    arg = radians

    @property
    def xx(self) -> Vec2:
        return Vec2(self.x, self.x)

    @property
    def yy(self) -> Vec2:
        return Vec2(self.y, self.y)

    @property
    def yx(self) -> Vec2:
        return Vec2(self.y, self.x)

    @property
    def xy(self) -> Vec2:
        return Vec2(self.x, self.y)

    @property
    def ccw(self) -> Vec2:
        return Vec2(-self.y, self.x)

    @property
    def cw(self) -> Vec2:
        return Vec2(self.y, -self.x)

    @property
    def frozen(self) -> tuple[float, float]:
        return self.x, self.y

    # -- SEQUENCE METHODS --
    def __len__(self) -> int:
        return 2

    @overload
    def __getitem__(self, idx: int) -> float: ...

    @overload
    def __getitem__(self, idx: slice) -> tuple[float, ...]: ...

    def __getitem__(self, idx: int | slice) -> float | tuple[float, ...]:
        return (self.x, self.y)[idx]

    def __iter__(self) -> Iterator[float]:
        # ! This iterator does not promise that y will be equal to what y was when you call
        # ! `iter(Vec2(...))`
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"<{self.x}, {self.y}>"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Vec2 | tuple):
            ox, oy = value
            return self.x == ox and self.y == oy
        return NotImplemented

    def __ne__(self, value: object, /) -> bool:
        if isinstance(value, Vec2 | tuple):
            ox, oy = value
            return self.x != ox or self.y != oy
        return NotImplemented

    # -- Vector Operations --
    def __neg__(self) -> Vec2:
        return Vec2.new(-self.x, -self.y)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def dot(self, other: Point2, /) -> float:
        return self.x * other[0] + self.y * other[1]

    def cross(self, other: Vec2, /) -> float:
        return -self.y * other.x + self.x * other.y

    def normalise(self) -> Vec2:
        l = abs(self)
        return Vec2.new(self.x / l, self.y / l)

    normalize = normalise

    def __add__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x + other.x, self.y + other.y)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x + other[0], self.y + other[1])
            case float() | int():
                return Vec2.new(self.x + other, self.y + other)
        return NotImplemented

    def __radd__(self, other: Point2 | float, /) -> Vec2:
        return self.__add__(other)

    def __sub__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x - other.x, self.y - other.y)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x - other[0], self.y - other[1])
            case float() | int():
                return Vec2.new(self.x - other, self.y - other)
        return NotImplemented

    def __rsub__(self, other: Point2 | float, /) -> Vec2:
        return (-self).__add__(other)

    def __mul__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x * other.x, self.y * other.y)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x * other[0], self.y * other[1])
            case float() | int():
                return Vec2.new(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other: Point2 | float, /) -> Vec2:
        return self.__mul__(other)

    def __truediv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x / other.x, self.y / other.y)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x / other[0], self.y / other[1])
            case float() | int():
                return Vec2.new(self.x / other, self.y / other)
        return NotImplemented

    def __rtruediv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x / self.x, other.y / self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] / self.x, other[1] / self.y)
            case float() | int():
                return Vec2.new(other / self.x, other / self.y)
        return NotImplemented

    def __mod__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x % other.x, self.y % other.y)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x % other[0], self.y % other[1])
            case float() | int():
                return Vec2.new(self.x % other, self.y % other)
        return NotImplemented

    def __rmod__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x % self.x, other.y % self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] % self.x, other[1] % self.y)
            case float() | int():
                return Vec2.new(other % self.x, other % self.y)
        return NotImplemented

    def __floordiv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x // other.x, self.y // other.y)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x // other[0], self.y // other[1])
            case float() | int():
                return Vec2.new(self.x // other, self.y // other)
        return NotImplemented

    def __rfloordiv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x // self.x, other.y // self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] // self.x, other[1] // self.y)
            case float() | int():
                return Vec2.new(other // self.x, other // self.y)
        return NotImplemented

    def __pow__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x**other.x, self.y**other.y)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x ** other[0], self.y ** other[1])
            case float() | int():
                return Vec2.new(self.x**other, self.y**other)
        return NotImplemented

    def __rpow__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x**self.x, other.y**self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] ** self.x, other[1] ** self.y)
            case float() | int():
                return Vec2.new(other**self.x, other**self.y)
        return NotImplemented

    def __matmul__(self, other: Point2, /) -> float:
        match other:
            case Vec2():
                return self.dot(other)
            case (float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __rmatmul__(self, other: Point2, /) -> float:
        match other:
            case Vec2():
                return other.dot(self)
            case (float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented


class Vec3(Sequence[float]):
    __slots__ = ("x", "y", "z")

    @overload
    def __init__(self, x: float) -> None: ...

    @overload
    def __init__(self, x: float, y: float, z: float) -> None: ...

    @overload
    def __init__(self, x: Point2, y: float) -> None: ...

    @overload
    def __init__(self, x: float, y: Point2) -> None: ...

    def __init__(
        self, x: Point2 | float, y: Point2 | float | None = None, z: float | None = None
    ) -> None:
        match (x, y, z):
            case (float() | int(), None, None):
                self.x = self.y = self.z = x
            case float() | int(), float() | int(), float() | int():
                self.x: float = x
                self.y: float = y
                self.z: float = z
            case (Vec2() | (float() | int(), float() | int()), float() | int(), None):
                self.x: float = x[0]
                self.y: float = x[1]
                self.z: float = y
            case (float() | int(), (float() | int(), float() | int()) | Vec2(), None):
                self.x = x
                self.y = y[0]
                self.z = y[1]
            case _:
                raise NotImplementedError(
                    f"Vec3 does not support Vec3({type(x)}, {type(y)}, {type(z)})"
                )

    @classmethod
    def new(cls, x: float, y: float, z: float) -> Self:
        vec = cls.__new__(cls)
        vec.x = x
        vec.y = y
        vec.z = z
        return vec

    @property
    def length(self) -> float:
        return abs(self)

    norm = length

    @property
    def frozen(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    # -- SEQUENCE METHODS --
    def __len__(self) -> int:
        return 3

    @overload
    def __getitem__(self, idx: int) -> float: ...

    @overload
    def __getitem__(self, idx: slice) -> tuple[float, ...]: ...

    def __getitem__(self, idx: int | slice) -> float | tuple[float, ...]:
        return (self.x, self.y, self.z)[idx]

    def __iter__(self) -> Iterator[float]:
        # ! This iterator does not promise that y or z will be equal to what they were when you call
        # ! `iter(Vec3(...))``
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self) -> str:
        return f"<{self.x}, {self.y}, {self.z}>"

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Vec3 | tuple):
            ox, oy, oz = value
            return self.x == ox and self.y == oy and self.z == oz
        return NotImplemented

    def __ne__(self, value: object, /) -> bool:
        if isinstance(value, Vec3 | tuple):
            ox, oy, oz = value
            return self.x != ox or self.y != oy or self.z != oz
        return NotImplemented

    # -- Vector Operations --
    def __neg__(self) -> Vec3:
        return Vec3.new(-self.x, -self.y, -self.z)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def dot(self, other: Point3, /) -> float:
        return self.x * other[0] + self.y * other[1] + self.z * other[2]

    def cross(self, other: Vec3, /) -> Vec3:
        sx, sy, sz = self
        ox, oy, oz = other
        return Vec3.new(sy * oz - sz * oy, sz * ox - sx * oz, sx * oy - sy * ox)

    def normalise(self) -> Vec3:
        l = abs(self)
        return Vec3.new(self.x / l, self.y / l, self.z / l)

    normalize = normalise

    def __add__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x + other.x, self.y + other.y, self.z + other.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x + other[0], self.y + other[1], self.z + other[2])
            case float() | int():
                return Vec3.new(self.x + other, self.y + other, self.z + other)
        return NotImplemented

    def __radd__(self, other: Point3 | float, /) -> Vec3:
        return self.__add__(other)

    def __sub__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x - other.x, self.y - other.y, self.z - other.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x - other[0], self.y - other[1], self.z - other[2])
            case float() | int():
                return Vec3.new(self.x - other, self.y - other, self.z - other)
        return NotImplemented

    def __rsub__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x - self.x, other.y - self.y, other.z - self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] - self.x, other[1] - self.y, other[2] - self.z)
            case float() | int():
                return Vec3.new(other - self.x, other - self.y, other - self.z)
        return NotImplemented

    def __mul__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x * other.x, self.y * other.y, self.z * other.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x * other[0], self.y * other[1], self.z * other[2])
            case float() | int():
                return Vec3.new(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other: Point3 | float, /) -> Vec3:
        return self.__mul__(other)

    def __truediv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x / other.x, self.y / other.y, self.z / other.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x / other[0], self.y / other[1], self.z / other[2])
            case float() | int():
                return Vec3.new(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError(f"Vec3 does not support division with {type(other)}")

    def __rtruediv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x / self.x, other.y / self.y, other.z / self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] / self.x, other[1] / self.y, other[2] / self.z)
            case float() | int():
                return Vec3.new(other / self.x, other / self.y, other / self.z)
        return NotImplemented

    def __mod__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x % other.x, self.y % other.y, self.z % other.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x % other[0], self.y % other[1], self.z % other[2])
            case float() | int():
                return Vec3.new(self.x % other, self.y % other, self.z % other)
        return NotImplemented

    def __rmod__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x % self.x, other.y % self.y, other.z % self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] % self.x, other[1] % self.y, other[2] % self.z)
            case float() | int():
                return Vec3.new(other % self.x, other % self.y, other % self.z)
        return NotImplemented

    def __floordiv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x // other.x, self.y // other.y, self.z // other.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x // other[0], self.y // other[1], self.z // other[2])
            case float() | int():
                return Vec3.new(self.x // other, self.y // other, self.z // other)
        return NotImplemented

    def __rfloordiv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x // self.x, other.y // self.y, other.z // self.x)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] // self.x, other[1] // self.y, other[2] // self.z)
            case float() | int():
                return Vec3.new(other // self.x, other // self.y, other // self.z)
        return NotImplemented

    def __pow__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x**other.x, self.y**other.y, self.z**other.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x ** other[0], self.y ** other[1], self.z ** other[2])
            case float() | int():
                return Vec3.new(self.x**other, self.y**other, self.z**other)
        return NotImplemented

    def __rpow__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x**self.x, other.y**self.y, other.z**self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] ** self.x, other[1] ** self.y, other[2] ** self.z)
            case float() | int():
                return Vec3.new(other**self.x, other**self.y, other**self.z)
        return NotImplemented

    def __matmul__(self, other: Point3, /) -> float:
        match other:
            case Vec3():
                return self.dot(other)
            case (float() | int(), float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __rmatmul__(self, other: Point3, /) -> float:
        match other:
            case Vec3():
                return other.dot(self)
            case (float() | int(), float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented
