# ! DO NOT EDIT DIRECTLY. THIS IS AN AUTO GENERATED FILE !
from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Self, Literal, overload

type Point2 = Vec2 | tuple[float, float]
class Vec2(Sequence[float]):
    __slots__ = ('x', 'y')
    @overload
    def __init__(self, x: float, y: float): ...
    @overload
    def __init__(self, x: Point2): ...

    def __init__(self, x: float | Point2 = 0.0, y: float | None = None) -> None:
        if isinstance(x, float) or isinstance(x, int):
            self.x = x
            if y is None:
                self.y = x
                return
            elif isinstance(y, float) or isinstance(y, int):
                self.y = y
                return
        elif isinstance(x, Vec2) or (isinstance(x, tuple) and len(x)==2):
            self.x, self.y = x
            return
        raise ValueError(f"Invalid input arguments for Vec2({x}, {y})")

    @classmethod
    def new(cls, x: float = 0.0, y: float = 0.0) -> Vec2:
        vec = cls.__new__(cls)
        vec.x = x
        vec.y = y
        return vec

    @property
    def frozen(self) -> tuple[float, float]:
        return self.x, self.y

    # -- LENGTH METHODS --

    @property
    def length_sqr(self) -> float:
        return self.x**2 + self.y**2
    norm_sqr = length_sqr

    @property
    def length(self) -> float:
        return (self.x**2 + self.y**2)**0.5
    norm = length

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    # -- VECTOR OPERATORS --

    def normalise(self) -> None:
        l = abs(self)
        self.x = self.x / l
        self.y = self.y / l
    normalize = normalise

    def normalised(self) -> Vec2:
        l = abs(self)
        return Vec2.new(self.x / l, self.y / l)
    normalized = normalised

    def dot(self, other: Point2, /) -> float:
        return self.x * other[0] + self.y * other[1]

    def __matmul__(self, other: Point2, /) -> float:
        match other:
            case Vec2():
                return self.dot(other)
            case (float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __rmatmul__(self, other: Point2, /) -> float:
        match other: # Multiplication with Matrix is not commutative even though it is with vectors
            case Vec2():
                return self.dot(other)
            case (float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __imatmul__(self, other: Point2, /):
        return NotImplemented

    def cross(self, other: Point2, /) -> float:
        return -self.y * other[0] + self.x * other[1]


    def rcross(self, other: Point2, /) -> float:
        return -other[1] * self.x + other[0] * self.y


    # -- HASH METHODS --

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Vec2) or isinstance(other, tuple):
            ox, oy = other
            return self.x == ox and self.y == oy
        return NotImplemented

    def __ne__(self, other: object, /) -> bool:
        if isinstance(other, Vec2) or isinstance(other, tuple):
            ox, oy = other
            return self.x != ox or self.y != oy
        return NotImplemented

    # -- SEQUENCE METHODS --

    def __len__(self) -> int:
        return 2

    @overload
    def __getitem__(self, idx: int) -> float: ...

    @overload
    def __getitem__(self, idx: slice) -> tuple[float, ...]: ...

    def __getitem__(self, idx: int | slice) -> float | tuple[float, ...]:
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        return (self.x, self.y)[idx]

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    # -- TYPE METHODS --

    def __bool__(self) -> Literal[True]:
        return True

    def __repr__(self) -> str:
        return f"Vec2(x = {self.x}, y = {self.y})"

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}>"

    # -- SCALAR OPERATORS --

    def __neg__(self) -> Vec2:
        return Vec2.new(-self.x, -self.y)

    def __add__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x + other.x, self.y + other.y)
            case float() | int():
                return Vec2.new(self.x + other, self.y + other)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __radd__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x + self.x, other.y + self.y)
            case float() | int():
                return Vec2.new(other + self.x, other + self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] + self.x, other[1] + self.y)
        return NotImplemented

    def __iadd__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                self.x += other.x
                self.y += other.y
            case float() | int():
                self.x += other
                self.y += other
            case (float() | int(), float() | int()):
                self.x += other[0]
                self.y += other[1]
        return NotImplemented

    def __sub__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x - other.x, self.y - other.y)
            case float() | int():
                return Vec2.new(self.x - other, self.y - other)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x - other[0], self.y - other[1])
        return NotImplemented

    def __rsub__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x - self.x, other.y - self.y)
            case float() | int():
                return Vec2.new(other - self.x, other - self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] - self.x, other[1] - self.y)
        return NotImplemented

    def __isub__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                self.x -= other.x
                self.y -= other.y
            case float() | int():
                self.x -= other
                self.y -= other
            case (float() | int(), float() | int()):
                self.x -= other[0]
                self.y -= other[1]
        return NotImplemented

    def __mul__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x * other.x, self.y * other.y)
            case float() | int():
                return Vec2.new(self.x * other, self.y * other)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x * other[0], self.y * other[1])
        return NotImplemented

    def __rmul__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x * self.x, other.y * self.y)
            case float() | int():
                return Vec2.new(other * self.x, other * self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] * self.x, other[1] * self.y)
        return NotImplemented

    def __imul__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                self.x *= other.x
                self.y *= other.y
            case float() | int():
                self.x *= other
                self.y *= other
            case (float() | int(), float() | int()):
                self.x *= other[0]
                self.y *= other[1]
        return NotImplemented

    def __truediv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x / other.x, self.y / other.y)
            case float() | int():
                return Vec2.new(self.x / other, self.y / other)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x / other[0], self.y / other[1])
        return NotImplemented

    def __rtruediv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x / self.x, other.y / self.y)
            case float() | int():
                return Vec2.new(other / self.x, other / self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] / self.x, other[1] / self.y)
        return NotImplemented

    def __itruediv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                self.x /= other.x
                self.y /= other.y
            case float() | int():
                self.x /= other
                self.y /= other
            case (float() | int(), float() | int()):
                self.x /= other[0]
                self.y /= other[1]
        return NotImplemented

    def __mod__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x % other.x, self.y % other.y)
            case float() | int():
                return Vec2.new(self.x % other, self.y % other)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x % other[0], self.y % other[1])
        return NotImplemented

    def __rmod__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x % self.x, other.y % self.y)
            case float() | int():
                return Vec2.new(other % self.x, other % self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] % self.x, other[1] % self.y)
        return NotImplemented

    def __imod__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                self.x %= other.x
                self.y %= other.y
            case float() | int():
                self.x %= other
                self.y %= other
            case (float() | int(), float() | int()):
                self.x %= other[0]
                self.y %= other[1]
        return NotImplemented

    def __floordiv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x // other.x, self.y // other.y)
            case float() | int():
                return Vec2.new(self.x // other, self.y // other)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x // other[0], self.y // other[1])
        return NotImplemented

    def __rfloordiv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x // self.x, other.y // self.y)
            case float() | int():
                return Vec2.new(other // self.x, other // self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] // self.x, other[1] // self.y)
        return NotImplemented

    def __ifloordiv__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                self.x //= other.x
                self.y //= other.y
            case float() | int():
                self.x //= other
                self.y //= other
            case (float() | int(), float() | int()):
                self.x //= other[0]
                self.y //= other[1]
        return NotImplemented

    def __pow__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(self.x ** other.x, self.y ** other.y)
            case float() | int():
                return Vec2.new(self.x ** other, self.y ** other)
            case (float() | int(), float() | int()):
                return Vec2.new(self.x ** other[0], self.y ** other[1])
        return NotImplemented

    def __rpow__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                return Vec2.new(other.x ** self.x, other.y ** self.y)
            case float() | int():
                return Vec2.new(other ** self.x, other ** self.y)
            case (float() | int(), float() | int()):
                return Vec2.new(other[0] ** self.x, other[1] ** self.y)
        return NotImplemented

    def __ipow__(self, other: Point2 | float, /) -> Vec2:
        match other:
            case Vec2():
                self.x **= other.x
                self.y **= other.y
            case float() | int():
                self.x **= other
                self.y **= other
            case (float() | int(), float() | int()):
                self.x **= other[0]
                self.y **= other[1]
        return NotImplemented

    # -- SWIZZLE COMBINATIONS --
    xx = property(lambda self: Vec2.new(self.x, self.x))
    xy = property(lambda self: Vec2.new(self.x, self.y))
    yx = property(lambda self: Vec2.new(self.y, self.x))
    yy = property(lambda self: Vec2.new(self.y, self.y))
    xxx = property(lambda self: Vec3.new(self.x, self.x, self.x))
    xxy = property(lambda self: Vec3.new(self.x, self.x, self.y))
    xyx = property(lambda self: Vec3.new(self.x, self.y, self.x))
    xyy = property(lambda self: Vec3.new(self.x, self.y, self.y))
    yxx = property(lambda self: Vec3.new(self.y, self.x, self.x))
    yxy = property(lambda self: Vec3.new(self.y, self.x, self.y))
    yyx = property(lambda self: Vec3.new(self.y, self.y, self.x))
    yyy = property(lambda self: Vec3.new(self.y, self.y, self.y))
    xxxx = property(lambda self: Vec4.new(self.x, self.x, self.x, self.x))
    xxxy = property(lambda self: Vec4.new(self.x, self.x, self.x, self.y))
    xxyx = property(lambda self: Vec4.new(self.x, self.x, self.y, self.x))
    xxyy = property(lambda self: Vec4.new(self.x, self.x, self.y, self.y))
    xyxx = property(lambda self: Vec4.new(self.x, self.y, self.x, self.x))
    xyxy = property(lambda self: Vec4.new(self.x, self.y, self.x, self.y))
    xyyx = property(lambda self: Vec4.new(self.x, self.y, self.y, self.x))
    xyyy = property(lambda self: Vec4.new(self.x, self.y, self.y, self.y))
    yxxx = property(lambda self: Vec4.new(self.y, self.x, self.x, self.x))
    yxxy = property(lambda self: Vec4.new(self.y, self.x, self.x, self.y))
    yxyx = property(lambda self: Vec4.new(self.y, self.x, self.y, self.x))
    yxyy = property(lambda self: Vec4.new(self.y, self.x, self.y, self.y))
    yyxx = property(lambda self: Vec4.new(self.y, self.y, self.x, self.x))
    yyxy = property(lambda self: Vec4.new(self.y, self.y, self.x, self.y))
    yyyx = property(lambda self: Vec4.new(self.y, self.y, self.y, self.x))
    yyyy = property(lambda self: Vec4.new(self.y, self.y, self.y, self.y))


    # -- SWIZZLE SETTERS -- 

    @xy.setter  # type: ignore -- reportGeneralTypeIssues
    def xy(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = other
        else:
            self.x, self.y = other

    @yx.setter  # type: ignore -- reportGeneralTypeIssues
    def yx(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = other
        else:
            self.y, self.x = other


type Point3 = Vec3 | tuple[float, float, float]
class Vec3(Sequence[float]):
    __slots__ = ('x', 'y', 'z')
    @overload
    def __init__(self, x: float, y: float, z: float): ...
    @overload
    def __init__(self, x: float, y: Point2): ...
    @overload
    def __init__(self, x: Point2, y: float): ...
    @overload
    def __init__(self, x: Point3): ...

    def __init__(self, x: float | Point2 | Point3 = 0.0, y: float | Point2 | None = None, z: float | None = None) -> None:
        if isinstance(x, float) or isinstance(x, int):
            self.x = x
            if y is None and z is None:
                self.y = self.z = x
                return
            elif isinstance(y, float) or isinstance(y, int):
                self.y = y
                if isinstance(z, float) or isinstance(z, int):
                    self.z = z
                    return
            elif isinstance(y, Vec2) or (isinstance(y, tuple) and len(y)==2):
                self.y, self.z = y
                return
        elif isinstance(x, Vec2) or (isinstance(x, tuple) and len(x)==2):
            self.x, self.y = x
            if isinstance(z, float) or isinstance(z, int):
                self.z = z
                return
        elif isinstance(x, Vec3) or (isinstance(x, tuple) and len(x)==3):
            self.x, self.y, self.z = x
            return
        raise ValueError(f"Invalid input arguments for Vec3({x}, {y}, {z})")

    @classmethod
    def new(cls, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Vec3:
        vec = cls.__new__(cls)
        vec.x = x
        vec.y = y
        vec.z = z
        return vec

    @property
    def frozen(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    # -- LENGTH METHODS --

    @property
    def length_sqr(self) -> float:
        return self.x**2 + self.y**2 + self.z**2
    norm_sqr = length_sqr

    @property
    def length(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    norm = length

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    # -- VECTOR OPERATORS --

    def normalise(self) -> None:
        l = abs(self)
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l
    normalize = normalise

    def normalised(self) -> Vec3:
        l = abs(self)
        return Vec3.new(self.x / l, self.y / l, self.z / l)
    normalized = normalised

    def dot(self, other: Point3, /) -> float:
        return self.x * other[0] + self.y * other[1] + self.z * other[2]

    def __matmul__(self, other: Point3, /) -> float:
        match other:
            case Vec3():
                return self.dot(other)
            case (float() | int(), float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __rmatmul__(self, other: Point3, /) -> float:
        match other: # Multiplication with Matrix is not commutative even though it is with vectors
            case Vec3():
                return self.dot(other)
            case (float() | int(), float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __imatmul__(self, other: Point2, /):
        return NotImplemented

    def cross(self, other: Point3, /) -> Vec3:
        a1, a2, a3 = self
        b1, b2, b3 = other
        return Vec3.new(a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1)


    def rcross(self, other: Point3, /) -> Vec3:
        a1, a2, a3 = other
        b1, b2, b3 = self
        return Vec3.new(a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1)


    # -- HASH METHODS --

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Vec3) or isinstance(other, tuple):
            ox, oy, oz = other
            return self.x == ox and self.y == oy and self.z == oz
        return NotImplemented

    def __ne__(self, other: object, /) -> bool:
        if isinstance(other, Vec3) or isinstance(other, tuple):
            ox, oy, oz = other
            return self.x != ox or self.y != oy or self.z != oz
        return NotImplemented

    # -- SEQUENCE METHODS --

    def __len__(self) -> int:
        return 3

    @overload
    def __getitem__(self, idx: int) -> float: ...

    @overload
    def __getitem__(self, idx: slice) -> tuple[float, ...]: ...

    def __getitem__(self, idx: int | slice) -> float | tuple[float, ...]:
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        return (self.x, self.y, self.z)[idx]

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z

    # -- TYPE METHODS --

    def __bool__(self) -> Literal[True]:
        return True

    def __repr__(self) -> str:
        return f"Vec3(x = {self.x}, y = {self.y}, z = {self.z})"

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}, {self.z}>"

    # -- SCALAR OPERATORS --

    def __neg__(self) -> Vec3:
        return Vec3.new(-self.x, -self.y, -self.z)

    def __add__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x + other.x, self.y + other.y, self.z + other.z)
            case float() | int():
                return Vec3.new(self.x + other, self.y + other, self.z + other)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x + other[0], self.y + other[1], self.z + other[2])
        return NotImplemented

    def __radd__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x + self.x, other.y + self.y, other.z + self.z)
            case float() | int():
                return Vec3.new(other + self.x, other + self.y, other + self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] + self.x, other[1] + self.y, other[2] + self.z)
        return NotImplemented

    def __iadd__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                self.x += other.x
                self.y += other.y
                self.z += other.z
            case float() | int():
                self.x += other
                self.y += other
                self.z += other
            case (float() | int(), float() | int(), float() | int()):
                self.x += other[0]
                self.y += other[1]
                self.z += other[2]
        return NotImplemented

    def __sub__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x - other.x, self.y - other.y, self.z - other.z)
            case float() | int():
                return Vec3.new(self.x - other, self.y - other, self.z - other)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x - other[0], self.y - other[1], self.z - other[2])
        return NotImplemented

    def __rsub__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x - self.x, other.y - self.y, other.z - self.z)
            case float() | int():
                return Vec3.new(other - self.x, other - self.y, other - self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] - self.x, other[1] - self.y, other[2] - self.z)
        return NotImplemented

    def __isub__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                self.x -= other.x
                self.y -= other.y
                self.z -= other.z
            case float() | int():
                self.x -= other
                self.y -= other
                self.z -= other
            case (float() | int(), float() | int(), float() | int()):
                self.x -= other[0]
                self.y -= other[1]
                self.z -= other[2]
        return NotImplemented

    def __mul__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x * other.x, self.y * other.y, self.z * other.z)
            case float() | int():
                return Vec3.new(self.x * other, self.y * other, self.z * other)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x * other[0], self.y * other[1], self.z * other[2])
        return NotImplemented

    def __rmul__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x * self.x, other.y * self.y, other.z * self.z)
            case float() | int():
                return Vec3.new(other * self.x, other * self.y, other * self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] * self.x, other[1] * self.y, other[2] * self.z)
        return NotImplemented

    def __imul__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                self.x *= other.x
                self.y *= other.y
                self.z *= other.z
            case float() | int():
                self.x *= other
                self.y *= other
                self.z *= other
            case (float() | int(), float() | int(), float() | int()):
                self.x *= other[0]
                self.y *= other[1]
                self.z *= other[2]
        return NotImplemented

    def __truediv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x / other.x, self.y / other.y, self.z / other.z)
            case float() | int():
                return Vec3.new(self.x / other, self.y / other, self.z / other)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x / other[0], self.y / other[1], self.z / other[2])
        return NotImplemented

    def __rtruediv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x / self.x, other.y / self.y, other.z / self.z)
            case float() | int():
                return Vec3.new(other / self.x, other / self.y, other / self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] / self.x, other[1] / self.y, other[2] / self.z)
        return NotImplemented

    def __itruediv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                self.x /= other.x
                self.y /= other.y
                self.z /= other.z
            case float() | int():
                self.x /= other
                self.y /= other
                self.z /= other
            case (float() | int(), float() | int(), float() | int()):
                self.x /= other[0]
                self.y /= other[1]
                self.z /= other[2]
        return NotImplemented

    def __mod__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x % other.x, self.y % other.y, self.z % other.z)
            case float() | int():
                return Vec3.new(self.x % other, self.y % other, self.z % other)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x % other[0], self.y % other[1], self.z % other[2])
        return NotImplemented

    def __rmod__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x % self.x, other.y % self.y, other.z % self.z)
            case float() | int():
                return Vec3.new(other % self.x, other % self.y, other % self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] % self.x, other[1] % self.y, other[2] % self.z)
        return NotImplemented

    def __imod__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                self.x %= other.x
                self.y %= other.y
                self.z %= other.z
            case float() | int():
                self.x %= other
                self.y %= other
                self.z %= other
            case (float() | int(), float() | int(), float() | int()):
                self.x %= other[0]
                self.y %= other[1]
                self.z %= other[2]
        return NotImplemented

    def __floordiv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x // other.x, self.y // other.y, self.z // other.z)
            case float() | int():
                return Vec3.new(self.x // other, self.y // other, self.z // other)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x // other[0], self.y // other[1], self.z // other[2])
        return NotImplemented

    def __rfloordiv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x // self.x, other.y // self.y, other.z // self.z)
            case float() | int():
                return Vec3.new(other // self.x, other // self.y, other // self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] // self.x, other[1] // self.y, other[2] // self.z)
        return NotImplemented

    def __ifloordiv__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                self.x //= other.x
                self.y //= other.y
                self.z //= other.z
            case float() | int():
                self.x //= other
                self.y //= other
                self.z //= other
            case (float() | int(), float() | int(), float() | int()):
                self.x //= other[0]
                self.y //= other[1]
                self.z //= other[2]
        return NotImplemented

    def __pow__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(self.x ** other.x, self.y ** other.y, self.z ** other.z)
            case float() | int():
                return Vec3.new(self.x ** other, self.y ** other, self.z ** other)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(self.x ** other[0], self.y ** other[1], self.z ** other[2])
        return NotImplemented

    def __rpow__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                return Vec3.new(other.x ** self.x, other.y ** self.y, other.z ** self.z)
            case float() | int():
                return Vec3.new(other ** self.x, other ** self.y, other ** self.z)
            case (float() | int(), float() | int(), float() | int()):
                return Vec3.new(other[0] ** self.x, other[1] ** self.y, other[2] ** self.z)
        return NotImplemented

    def __ipow__(self, other: Point3 | float, /) -> Vec3:
        match other:
            case Vec3():
                self.x **= other.x
                self.y **= other.y
                self.z **= other.z
            case float() | int():
                self.x **= other
                self.y **= other
                self.z **= other
            case (float() | int(), float() | int(), float() | int()):
                self.x **= other[0]
                self.y **= other[1]
                self.z **= other[2]
        return NotImplemented

    # -- SWIZZLE COMBINATIONS --
    xx = property(lambda self: Vec2.new(self.x, self.x))
    xy = property(lambda self: Vec2.new(self.x, self.y))
    xz = property(lambda self: Vec2.new(self.x, self.z))
    yx = property(lambda self: Vec2.new(self.y, self.x))
    yy = property(lambda self: Vec2.new(self.y, self.y))
    yz = property(lambda self: Vec2.new(self.y, self.z))
    zx = property(lambda self: Vec2.new(self.z, self.x))
    zy = property(lambda self: Vec2.new(self.z, self.y))
    zz = property(lambda self: Vec2.new(self.z, self.z))
    xxx = property(lambda self: Vec3.new(self.x, self.x, self.x))
    xxy = property(lambda self: Vec3.new(self.x, self.x, self.y))
    xxz = property(lambda self: Vec3.new(self.x, self.x, self.z))
    xyx = property(lambda self: Vec3.new(self.x, self.y, self.x))
    xyy = property(lambda self: Vec3.new(self.x, self.y, self.y))
    xyz = property(lambda self: Vec3.new(self.x, self.y, self.z))
    xzx = property(lambda self: Vec3.new(self.x, self.z, self.x))
    xzy = property(lambda self: Vec3.new(self.x, self.z, self.y))
    xzz = property(lambda self: Vec3.new(self.x, self.z, self.z))
    yxx = property(lambda self: Vec3.new(self.y, self.x, self.x))
    yxy = property(lambda self: Vec3.new(self.y, self.x, self.y))
    yxz = property(lambda self: Vec3.new(self.y, self.x, self.z))
    yyx = property(lambda self: Vec3.new(self.y, self.y, self.x))
    yyy = property(lambda self: Vec3.new(self.y, self.y, self.y))
    yyz = property(lambda self: Vec3.new(self.y, self.y, self.z))
    yzx = property(lambda self: Vec3.new(self.y, self.z, self.x))
    yzy = property(lambda self: Vec3.new(self.y, self.z, self.y))
    yzz = property(lambda self: Vec3.new(self.y, self.z, self.z))
    zxx = property(lambda self: Vec3.new(self.z, self.x, self.x))
    zxy = property(lambda self: Vec3.new(self.z, self.x, self.y))
    zxz = property(lambda self: Vec3.new(self.z, self.x, self.z))
    zyx = property(lambda self: Vec3.new(self.z, self.y, self.x))
    zyy = property(lambda self: Vec3.new(self.z, self.y, self.y))
    zyz = property(lambda self: Vec3.new(self.z, self.y, self.z))
    zzx = property(lambda self: Vec3.new(self.z, self.z, self.x))
    zzy = property(lambda self: Vec3.new(self.z, self.z, self.y))
    zzz = property(lambda self: Vec3.new(self.z, self.z, self.z))
    xxxx = property(lambda self: Vec4.new(self.x, self.x, self.x, self.x))
    xxxy = property(lambda self: Vec4.new(self.x, self.x, self.x, self.y))
    xxxz = property(lambda self: Vec4.new(self.x, self.x, self.x, self.z))
    xxyx = property(lambda self: Vec4.new(self.x, self.x, self.y, self.x))
    xxyy = property(lambda self: Vec4.new(self.x, self.x, self.y, self.y))
    xxyz = property(lambda self: Vec4.new(self.x, self.x, self.y, self.z))
    xxzx = property(lambda self: Vec4.new(self.x, self.x, self.z, self.x))
    xxzy = property(lambda self: Vec4.new(self.x, self.x, self.z, self.y))
    xxzz = property(lambda self: Vec4.new(self.x, self.x, self.z, self.z))
    xyxx = property(lambda self: Vec4.new(self.x, self.y, self.x, self.x))
    xyxy = property(lambda self: Vec4.new(self.x, self.y, self.x, self.y))
    xyxz = property(lambda self: Vec4.new(self.x, self.y, self.x, self.z))
    xyyx = property(lambda self: Vec4.new(self.x, self.y, self.y, self.x))
    xyyy = property(lambda self: Vec4.new(self.x, self.y, self.y, self.y))
    xyyz = property(lambda self: Vec4.new(self.x, self.y, self.y, self.z))
    xyzx = property(lambda self: Vec4.new(self.x, self.y, self.z, self.x))
    xyzy = property(lambda self: Vec4.new(self.x, self.y, self.z, self.y))
    xyzz = property(lambda self: Vec4.new(self.x, self.y, self.z, self.z))
    xzxx = property(lambda self: Vec4.new(self.x, self.z, self.x, self.x))
    xzxy = property(lambda self: Vec4.new(self.x, self.z, self.x, self.y))
    xzxz = property(lambda self: Vec4.new(self.x, self.z, self.x, self.z))
    xzyx = property(lambda self: Vec4.new(self.x, self.z, self.y, self.x))
    xzyy = property(lambda self: Vec4.new(self.x, self.z, self.y, self.y))
    xzyz = property(lambda self: Vec4.new(self.x, self.z, self.y, self.z))
    xzzx = property(lambda self: Vec4.new(self.x, self.z, self.z, self.x))
    xzzy = property(lambda self: Vec4.new(self.x, self.z, self.z, self.y))
    xzzz = property(lambda self: Vec4.new(self.x, self.z, self.z, self.z))
    yxxx = property(lambda self: Vec4.new(self.y, self.x, self.x, self.x))
    yxxy = property(lambda self: Vec4.new(self.y, self.x, self.x, self.y))
    yxxz = property(lambda self: Vec4.new(self.y, self.x, self.x, self.z))
    yxyx = property(lambda self: Vec4.new(self.y, self.x, self.y, self.x))
    yxyy = property(lambda self: Vec4.new(self.y, self.x, self.y, self.y))
    yxyz = property(lambda self: Vec4.new(self.y, self.x, self.y, self.z))
    yxzx = property(lambda self: Vec4.new(self.y, self.x, self.z, self.x))
    yxzy = property(lambda self: Vec4.new(self.y, self.x, self.z, self.y))
    yxzz = property(lambda self: Vec4.new(self.y, self.x, self.z, self.z))
    yyxx = property(lambda self: Vec4.new(self.y, self.y, self.x, self.x))
    yyxy = property(lambda self: Vec4.new(self.y, self.y, self.x, self.y))
    yyxz = property(lambda self: Vec4.new(self.y, self.y, self.x, self.z))
    yyyx = property(lambda self: Vec4.new(self.y, self.y, self.y, self.x))
    yyyy = property(lambda self: Vec4.new(self.y, self.y, self.y, self.y))
    yyyz = property(lambda self: Vec4.new(self.y, self.y, self.y, self.z))
    yyzx = property(lambda self: Vec4.new(self.y, self.y, self.z, self.x))
    yyzy = property(lambda self: Vec4.new(self.y, self.y, self.z, self.y))
    yyzz = property(lambda self: Vec4.new(self.y, self.y, self.z, self.z))
    yzxx = property(lambda self: Vec4.new(self.y, self.z, self.x, self.x))
    yzxy = property(lambda self: Vec4.new(self.y, self.z, self.x, self.y))
    yzxz = property(lambda self: Vec4.new(self.y, self.z, self.x, self.z))
    yzyx = property(lambda self: Vec4.new(self.y, self.z, self.y, self.x))
    yzyy = property(lambda self: Vec4.new(self.y, self.z, self.y, self.y))
    yzyz = property(lambda self: Vec4.new(self.y, self.z, self.y, self.z))
    yzzx = property(lambda self: Vec4.new(self.y, self.z, self.z, self.x))
    yzzy = property(lambda self: Vec4.new(self.y, self.z, self.z, self.y))
    yzzz = property(lambda self: Vec4.new(self.y, self.z, self.z, self.z))
    zxxx = property(lambda self: Vec4.new(self.z, self.x, self.x, self.x))
    zxxy = property(lambda self: Vec4.new(self.z, self.x, self.x, self.y))
    zxxz = property(lambda self: Vec4.new(self.z, self.x, self.x, self.z))
    zxyx = property(lambda self: Vec4.new(self.z, self.x, self.y, self.x))
    zxyy = property(lambda self: Vec4.new(self.z, self.x, self.y, self.y))
    zxyz = property(lambda self: Vec4.new(self.z, self.x, self.y, self.z))
    zxzx = property(lambda self: Vec4.new(self.z, self.x, self.z, self.x))
    zxzy = property(lambda self: Vec4.new(self.z, self.x, self.z, self.y))
    zxzz = property(lambda self: Vec4.new(self.z, self.x, self.z, self.z))
    zyxx = property(lambda self: Vec4.new(self.z, self.y, self.x, self.x))
    zyxy = property(lambda self: Vec4.new(self.z, self.y, self.x, self.y))
    zyxz = property(lambda self: Vec4.new(self.z, self.y, self.x, self.z))
    zyyx = property(lambda self: Vec4.new(self.z, self.y, self.y, self.x))
    zyyy = property(lambda self: Vec4.new(self.z, self.y, self.y, self.y))
    zyyz = property(lambda self: Vec4.new(self.z, self.y, self.y, self.z))
    zyzx = property(lambda self: Vec4.new(self.z, self.y, self.z, self.x))
    zyzy = property(lambda self: Vec4.new(self.z, self.y, self.z, self.y))
    zyzz = property(lambda self: Vec4.new(self.z, self.y, self.z, self.z))
    zzxx = property(lambda self: Vec4.new(self.z, self.z, self.x, self.x))
    zzxy = property(lambda self: Vec4.new(self.z, self.z, self.x, self.y))
    zzxz = property(lambda self: Vec4.new(self.z, self.z, self.x, self.z))
    zzyx = property(lambda self: Vec4.new(self.z, self.z, self.y, self.x))
    zzyy = property(lambda self: Vec4.new(self.z, self.z, self.y, self.y))
    zzyz = property(lambda self: Vec4.new(self.z, self.z, self.y, self.z))
    zzzx = property(lambda self: Vec4.new(self.z, self.z, self.z, self.x))
    zzzy = property(lambda self: Vec4.new(self.z, self.z, self.z, self.y))
    zzzz = property(lambda self: Vec4.new(self.z, self.z, self.z, self.z))


    # -- SWIZZLE SETTERS -- 

    @xy.setter  # type: ignore -- reportGeneralTypeIssues
    def xy(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = other
        else:
            self.x, self.y = other

    @xz.setter  # type: ignore -- reportGeneralTypeIssues
    def xz(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.z = other
        else:
            self.x, self.z = other

    @yx.setter  # type: ignore -- reportGeneralTypeIssues
    def yx(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = other
        else:
            self.y, self.x = other

    @yz.setter  # type: ignore -- reportGeneralTypeIssues
    def yz(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.z = other
        else:
            self.y, self.z = other

    @zx.setter  # type: ignore -- reportGeneralTypeIssues
    def zx(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.x = other
        else:
            self.z, self.x = other

    @zy.setter  # type: ignore -- reportGeneralTypeIssues
    def zy(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.y = other
        else:
            self.z, self.y = other

    @xyz.setter  # type: ignore -- reportGeneralTypeIssues
    def xyz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = self.z = other
        else:
            self.x, self.y, self.z = other

    @xzy.setter  # type: ignore -- reportGeneralTypeIssues
    def xzy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.z = self.y = other
        else:
            self.x, self.z, self.y = other

    @yxz.setter  # type: ignore -- reportGeneralTypeIssues
    def yxz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = self.z = other
        else:
            self.y, self.x, self.z = other

    @yzx.setter  # type: ignore -- reportGeneralTypeIssues
    def yzx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.z = self.x = other
        else:
            self.y, self.z, self.x = other

    @zxy.setter  # type: ignore -- reportGeneralTypeIssues
    def zxy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.x = self.y = other
        else:
            self.z, self.x, self.y = other

    @zyx.setter  # type: ignore -- reportGeneralTypeIssues
    def zyx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.y = self.x = other
        else:
            self.z, self.y, self.x = other


type Point4 = Vec4 | tuple[float, float, float, float]
class Vec4(Sequence[float]):
    __slots__ = ('x', 'y', 'z', 'w')
    @overload
    def __init__(self, x: float, y: float, z: float, w: float): ...
    @overload
    def __init__(self, x: float, y: float, z: Point2): ...
    @overload
    def __init__(self, x: float, y: Point2, z: float): ...
    @overload
    def __init__(self, x: float, y: Point3): ...
    @overload
    def __init__(self, x: Point2, y: float, z: float): ...
    @overload
    def __init__(self, x: Point2, y: Point2): ...
    @overload
    def __init__(self, x: Point3, y: float): ...
    @overload
    def __init__(self, x: Point4): ...

    def __init__(self, x: float | Point2 | Point3 | Point4 = 0.0, y: float | Point2 | Point3 | None = None, z: float | Point2 | None = None, w: float | None = None) -> None:
        if isinstance(x, float) or isinstance(x, int):
            self.x = x
            if y is None and z is None and w is None:
                self.y = self.z = self.w = x
                return
            elif isinstance(y, float) or isinstance(y, int):
                self.y = y
                if isinstance(z, float) or isinstance(z, int):
                    self.z = z
                    if isinstance(w, float) or isinstance(w, int):
                        self.w = w
                        return
                elif isinstance(z, Vec2) or (isinstance(z, tuple) and len(z)==2):
                    self.z, self.w = z
                    return
            elif isinstance(y, Vec2) or (isinstance(y, tuple) and len(y)==2):
                self.y, self.z = y
                if isinstance(w, float) or isinstance(w, int):
                    self.w = w
                    return
            elif isinstance(y, Vec3) or (isinstance(y, tuple) and len(y)==3):
                self.y, self.z, self.w = y
                return
        elif isinstance(x, Vec2) or (isinstance(x, tuple) and len(x)==2):
            self.x, self.y = x
            if isinstance(z, float) or isinstance(z, int):
                self.z = z
                if isinstance(w, float) or isinstance(w, int):
                    self.w = w
                    return
            elif isinstance(z, Vec2) or (isinstance(z, tuple) and len(z)==2):
                self.z, self.w = z
                return
        elif isinstance(x, Vec3) or (isinstance(x, tuple) and len(x)==3):
            self.x, self.y, self.z = x
            if isinstance(w, float) or isinstance(w, int):
                self.w = w
                return
        elif isinstance(x, Vec4) or (isinstance(x, tuple) and len(x)==4):
            self.x, self.y, self.z, self.w = x
            return
        raise ValueError(f"Invalid input arguments for Vec4({x}, {y}, {z}, {w})")

    @classmethod
    def new(cls, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0) -> Vec4:
        vec = cls.__new__(cls)
        vec.x = x
        vec.y = y
        vec.z = z
        vec.w = w
        return vec

    @property
    def frozen(self) -> tuple[float, float, float, float]:
        return self.x, self.y, self.z, self.w

    # -- LENGTH METHODS --

    @property
    def length_sqr(self) -> float:
        return self.x**2 + self.y**2 + self.z**2 + self.w**2
    norm_sqr = length_sqr

    @property
    def length(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2 + self.w**2)**0.5
    norm = length

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2 + self.w**2)**0.5

    # -- VECTOR OPERATORS --

    def normalise(self) -> None:
        l = abs(self)
        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l
        self.w = self.w / l
    normalize = normalise

    def normalised(self) -> Vec4:
        l = abs(self)
        return Vec4.new(self.x / l, self.y / l, self.z / l, self.w / l)
    normalized = normalised

    def dot(self, other: Point4, /) -> float:
        return self.x * other[0] + self.y * other[1] + self.z * other[2] + self.w * other[3]

    def __matmul__(self, other: Point4, /) -> float:
        match other:
            case Vec4():
                return self.dot(other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __rmatmul__(self, other: Point4, /) -> float:
        match other: # Multiplication with Matrix is not commutative even though it is with vectors
            case Vec4():
                return self.dot(other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return self.dot(other)
        return NotImplemented

    def __imatmul__(self, other: Point2, /):
        return NotImplemented

    def cross(self, other: Point4, /) -> Vec4:
        raise NotImplementedError('Vec4 does not implement cross product')

    def rcross(self, other: Point4, /) -> Vec4:
        raise NotImplementedError('Vec4 does not implement cross product')

    # -- HASH METHODS --

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z, self.w))

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Vec4) or isinstance(other, tuple):
            ox, oy, oz, ow = other
            return self.x == ox and self.y == oy and self.z == oz and self.w == ow
        return NotImplemented

    def __ne__(self, other: object, /) -> bool:
        if isinstance(other, Vec4) or isinstance(other, tuple):
            ox, oy, oz, ow = other
            return self.x != ox or self.y != oy or self.z != oz or self.w != ow
        return NotImplemented

    # -- SEQUENCE METHODS --

    def __len__(self) -> int:
        return 4

    @overload
    def __getitem__(self, idx: int) -> float: ...

    @overload
    def __getitem__(self, idx: slice) -> tuple[float, ...]: ...

    def __getitem__(self, idx: int | slice) -> float | tuple[float, ...]:
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        elif idx == 3:
            return self.w
        return (self.x, self.y, self.z, self.w)[idx]

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z
        yield self.w

    # -- TYPE METHODS --

    def __bool__(self) -> Literal[True]:
        return True

    def __repr__(self) -> str:
        return f"Vec4(x = {self.x}, y = {self.y}, z = {self.z}, w = {self.w})"

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}, {self.z}, {self.w}>"

    # -- SCALAR OPERATORS --

    def __neg__(self) -> Vec4:
        return Vec4.new(-self.x, -self.y, -self.z, -self.w)

    def __add__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
            case float() | int():
                return Vec4.new(self.x + other, self.y + other, self.z + other, self.w + other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(self.x + other[0], self.y + other[1], self.z + other[2], self.w + other[3])
        return NotImplemented

    def __radd__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(other.x + self.x, other.y + self.y, other.z + self.z, other.w + self.w)
            case float() | int():
                return Vec4.new(other + self.x, other + self.y, other + self.z, other + self.w)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(other[0] + self.x, other[1] + self.y, other[2] + self.z, other[3] + self.w)
        return NotImplemented

    def __iadd__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                self.x += other.x
                self.y += other.y
                self.z += other.z
                self.w += other.w
            case float() | int():
                self.x += other
                self.y += other
                self.z += other
                self.w += other
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                self.x += other[0]
                self.y += other[1]
                self.z += other[2]
                self.w += other[3]
        return NotImplemented

    def __sub__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
            case float() | int():
                return Vec4.new(self.x - other, self.y - other, self.z - other, self.w - other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(self.x - other[0], self.y - other[1], self.z - other[2], self.w - other[3])
        return NotImplemented

    def __rsub__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(other.x - self.x, other.y - self.y, other.z - self.z, other.w - self.w)
            case float() | int():
                return Vec4.new(other - self.x, other - self.y, other - self.z, other - self.w)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(other[0] - self.x, other[1] - self.y, other[2] - self.z, other[3] - self.w)
        return NotImplemented

    def __isub__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                self.x -= other.x
                self.y -= other.y
                self.z -= other.z
                self.w -= other.w
            case float() | int():
                self.x -= other
                self.y -= other
                self.z -= other
                self.w -= other
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                self.x -= other[0]
                self.y -= other[1]
                self.z -= other[2]
                self.w -= other[3]
        return NotImplemented

    def __mul__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w)
            case float() | int():
                return Vec4.new(self.x * other, self.y * other, self.z * other, self.w * other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(self.x * other[0], self.y * other[1], self.z * other[2], self.w * other[3])
        return NotImplemented

    def __rmul__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(other.x * self.x, other.y * self.y, other.z * self.z, other.w * self.w)
            case float() | int():
                return Vec4.new(other * self.x, other * self.y, other * self.z, other * self.w)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(other[0] * self.x, other[1] * self.y, other[2] * self.z, other[3] * self.w)
        return NotImplemented

    def __imul__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                self.x *= other.x
                self.y *= other.y
                self.z *= other.z
                self.w *= other.w
            case float() | int():
                self.x *= other
                self.y *= other
                self.z *= other
                self.w *= other
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                self.x *= other[0]
                self.y *= other[1]
                self.z *= other[2]
                self.w *= other[3]
        return NotImplemented

    def __truediv__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w)
            case float() | int():
                return Vec4.new(self.x / other, self.y / other, self.z / other, self.w / other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(self.x / other[0], self.y / other[1], self.z / other[2], self.w / other[3])
        return NotImplemented

    def __rtruediv__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(other.x / self.x, other.y / self.y, other.z / self.z, other.w / self.w)
            case float() | int():
                return Vec4.new(other / self.x, other / self.y, other / self.z, other / self.w)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(other[0] / self.x, other[1] / self.y, other[2] / self.z, other[3] / self.w)
        return NotImplemented

    def __itruediv__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                self.x /= other.x
                self.y /= other.y
                self.z /= other.z
                self.w /= other.w
            case float() | int():
                self.x /= other
                self.y /= other
                self.z /= other
                self.w /= other
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                self.x /= other[0]
                self.y /= other[1]
                self.z /= other[2]
                self.w /= other[3]
        return NotImplemented

    def __mod__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(self.x % other.x, self.y % other.y, self.z % other.z, self.w % other.w)
            case float() | int():
                return Vec4.new(self.x % other, self.y % other, self.z % other, self.w % other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(self.x % other[0], self.y % other[1], self.z % other[2], self.w % other[3])
        return NotImplemented

    def __rmod__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(other.x % self.x, other.y % self.y, other.z % self.z, other.w % self.w)
            case float() | int():
                return Vec4.new(other % self.x, other % self.y, other % self.z, other % self.w)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(other[0] % self.x, other[1] % self.y, other[2] % self.z, other[3] % self.w)
        return NotImplemented

    def __imod__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                self.x %= other.x
                self.y %= other.y
                self.z %= other.z
                self.w %= other.w
            case float() | int():
                self.x %= other
                self.y %= other
                self.z %= other
                self.w %= other
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                self.x %= other[0]
                self.y %= other[1]
                self.z %= other[2]
                self.w %= other[3]
        return NotImplemented

    def __floordiv__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(self.x // other.x, self.y // other.y, self.z // other.z, self.w // other.w)
            case float() | int():
                return Vec4.new(self.x // other, self.y // other, self.z // other, self.w // other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(self.x // other[0], self.y // other[1], self.z // other[2], self.w // other[3])
        return NotImplemented

    def __rfloordiv__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(other.x // self.x, other.y // self.y, other.z // self.z, other.w // self.w)
            case float() | int():
                return Vec4.new(other // self.x, other // self.y, other // self.z, other // self.w)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(other[0] // self.x, other[1] // self.y, other[2] // self.z, other[3] // self.w)
        return NotImplemented

    def __ifloordiv__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                self.x //= other.x
                self.y //= other.y
                self.z //= other.z
                self.w //= other.w
            case float() | int():
                self.x //= other
                self.y //= other
                self.z //= other
                self.w //= other
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                self.x //= other[0]
                self.y //= other[1]
                self.z //= other[2]
                self.w //= other[3]
        return NotImplemented

    def __pow__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(self.x ** other.x, self.y ** other.y, self.z ** other.z, self.w ** other.w)
            case float() | int():
                return Vec4.new(self.x ** other, self.y ** other, self.z ** other, self.w ** other)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(self.x ** other[0], self.y ** other[1], self.z ** other[2], self.w ** other[3])
        return NotImplemented

    def __rpow__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                return Vec4.new(other.x ** self.x, other.y ** self.y, other.z ** self.z, other.w ** self.w)
            case float() | int():
                return Vec4.new(other ** self.x, other ** self.y, other ** self.z, other ** self.w)
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                return Vec4.new(other[0] ** self.x, other[1] ** self.y, other[2] ** self.z, other[3] ** self.w)
        return NotImplemented

    def __ipow__(self, other: Point4 | float, /) -> Vec4:
        match other:
            case Vec4():
                self.x **= other.x
                self.y **= other.y
                self.z **= other.z
                self.w **= other.w
            case float() | int():
                self.x **= other
                self.y **= other
                self.z **= other
                self.w **= other
            case (float() | int(), float() | int(), float() | int(), float() | int()):
                self.x **= other[0]
                self.y **= other[1]
                self.z **= other[2]
                self.w **= other[3]
        return NotImplemented

    # -- SWIZZLE COMBINATIONS --
    xx = property(lambda self: Vec2.new(self.x, self.x))
    xy = property(lambda self: Vec2.new(self.x, self.y))
    xz = property(lambda self: Vec2.new(self.x, self.z))
    xw = property(lambda self: Vec2.new(self.x, self.w))
    yx = property(lambda self: Vec2.new(self.y, self.x))
    yy = property(lambda self: Vec2.new(self.y, self.y))
    yz = property(lambda self: Vec2.new(self.y, self.z))
    yw = property(lambda self: Vec2.new(self.y, self.w))
    zx = property(lambda self: Vec2.new(self.z, self.x))
    zy = property(lambda self: Vec2.new(self.z, self.y))
    zz = property(lambda self: Vec2.new(self.z, self.z))
    zw = property(lambda self: Vec2.new(self.z, self.w))
    wx = property(lambda self: Vec2.new(self.w, self.x))
    wy = property(lambda self: Vec2.new(self.w, self.y))
    wz = property(lambda self: Vec2.new(self.w, self.z))
    ww = property(lambda self: Vec2.new(self.w, self.w))
    xxx = property(lambda self: Vec3.new(self.x, self.x, self.x))
    xxy = property(lambda self: Vec3.new(self.x, self.x, self.y))
    xxz = property(lambda self: Vec3.new(self.x, self.x, self.z))
    xxw = property(lambda self: Vec3.new(self.x, self.x, self.w))
    xyx = property(lambda self: Vec3.new(self.x, self.y, self.x))
    xyy = property(lambda self: Vec3.new(self.x, self.y, self.y))
    xyz = property(lambda self: Vec3.new(self.x, self.y, self.z))
    xyw = property(lambda self: Vec3.new(self.x, self.y, self.w))
    xzx = property(lambda self: Vec3.new(self.x, self.z, self.x))
    xzy = property(lambda self: Vec3.new(self.x, self.z, self.y))
    xzz = property(lambda self: Vec3.new(self.x, self.z, self.z))
    xzw = property(lambda self: Vec3.new(self.x, self.z, self.w))
    xwx = property(lambda self: Vec3.new(self.x, self.w, self.x))
    xwy = property(lambda self: Vec3.new(self.x, self.w, self.y))
    xwz = property(lambda self: Vec3.new(self.x, self.w, self.z))
    xww = property(lambda self: Vec3.new(self.x, self.w, self.w))
    yxx = property(lambda self: Vec3.new(self.y, self.x, self.x))
    yxy = property(lambda self: Vec3.new(self.y, self.x, self.y))
    yxz = property(lambda self: Vec3.new(self.y, self.x, self.z))
    yxw = property(lambda self: Vec3.new(self.y, self.x, self.w))
    yyx = property(lambda self: Vec3.new(self.y, self.y, self.x))
    yyy = property(lambda self: Vec3.new(self.y, self.y, self.y))
    yyz = property(lambda self: Vec3.new(self.y, self.y, self.z))
    yyw = property(lambda self: Vec3.new(self.y, self.y, self.w))
    yzx = property(lambda self: Vec3.new(self.y, self.z, self.x))
    yzy = property(lambda self: Vec3.new(self.y, self.z, self.y))
    yzz = property(lambda self: Vec3.new(self.y, self.z, self.z))
    yzw = property(lambda self: Vec3.new(self.y, self.z, self.w))
    ywx = property(lambda self: Vec3.new(self.y, self.w, self.x))
    ywy = property(lambda self: Vec3.new(self.y, self.w, self.y))
    ywz = property(lambda self: Vec3.new(self.y, self.w, self.z))
    yww = property(lambda self: Vec3.new(self.y, self.w, self.w))
    zxx = property(lambda self: Vec3.new(self.z, self.x, self.x))
    zxy = property(lambda self: Vec3.new(self.z, self.x, self.y))
    zxz = property(lambda self: Vec3.new(self.z, self.x, self.z))
    zxw = property(lambda self: Vec3.new(self.z, self.x, self.w))
    zyx = property(lambda self: Vec3.new(self.z, self.y, self.x))
    zyy = property(lambda self: Vec3.new(self.z, self.y, self.y))
    zyz = property(lambda self: Vec3.new(self.z, self.y, self.z))
    zyw = property(lambda self: Vec3.new(self.z, self.y, self.w))
    zzx = property(lambda self: Vec3.new(self.z, self.z, self.x))
    zzy = property(lambda self: Vec3.new(self.z, self.z, self.y))
    zzz = property(lambda self: Vec3.new(self.z, self.z, self.z))
    zzw = property(lambda self: Vec3.new(self.z, self.z, self.w))
    zwx = property(lambda self: Vec3.new(self.z, self.w, self.x))
    zwy = property(lambda self: Vec3.new(self.z, self.w, self.y))
    zwz = property(lambda self: Vec3.new(self.z, self.w, self.z))
    zww = property(lambda self: Vec3.new(self.z, self.w, self.w))
    wxx = property(lambda self: Vec3.new(self.w, self.x, self.x))
    wxy = property(lambda self: Vec3.new(self.w, self.x, self.y))
    wxz = property(lambda self: Vec3.new(self.w, self.x, self.z))
    wxw = property(lambda self: Vec3.new(self.w, self.x, self.w))
    wyx = property(lambda self: Vec3.new(self.w, self.y, self.x))
    wyy = property(lambda self: Vec3.new(self.w, self.y, self.y))
    wyz = property(lambda self: Vec3.new(self.w, self.y, self.z))
    wyw = property(lambda self: Vec3.new(self.w, self.y, self.w))
    wzx = property(lambda self: Vec3.new(self.w, self.z, self.x))
    wzy = property(lambda self: Vec3.new(self.w, self.z, self.y))
    wzz = property(lambda self: Vec3.new(self.w, self.z, self.z))
    wzw = property(lambda self: Vec3.new(self.w, self.z, self.w))
    wwx = property(lambda self: Vec3.new(self.w, self.w, self.x))
    wwy = property(lambda self: Vec3.new(self.w, self.w, self.y))
    wwz = property(lambda self: Vec3.new(self.w, self.w, self.z))
    www = property(lambda self: Vec3.new(self.w, self.w, self.w))
    xxxx = property(lambda self: Vec4.new(self.x, self.x, self.x, self.x))
    xxxy = property(lambda self: Vec4.new(self.x, self.x, self.x, self.y))
    xxxz = property(lambda self: Vec4.new(self.x, self.x, self.x, self.z))
    xxxw = property(lambda self: Vec4.new(self.x, self.x, self.x, self.w))
    xxyx = property(lambda self: Vec4.new(self.x, self.x, self.y, self.x))
    xxyy = property(lambda self: Vec4.new(self.x, self.x, self.y, self.y))
    xxyz = property(lambda self: Vec4.new(self.x, self.x, self.y, self.z))
    xxyw = property(lambda self: Vec4.new(self.x, self.x, self.y, self.w))
    xxzx = property(lambda self: Vec4.new(self.x, self.x, self.z, self.x))
    xxzy = property(lambda self: Vec4.new(self.x, self.x, self.z, self.y))
    xxzz = property(lambda self: Vec4.new(self.x, self.x, self.z, self.z))
    xxzw = property(lambda self: Vec4.new(self.x, self.x, self.z, self.w))
    xxwx = property(lambda self: Vec4.new(self.x, self.x, self.w, self.x))
    xxwy = property(lambda self: Vec4.new(self.x, self.x, self.w, self.y))
    xxwz = property(lambda self: Vec4.new(self.x, self.x, self.w, self.z))
    xxww = property(lambda self: Vec4.new(self.x, self.x, self.w, self.w))
    xyxx = property(lambda self: Vec4.new(self.x, self.y, self.x, self.x))
    xyxy = property(lambda self: Vec4.new(self.x, self.y, self.x, self.y))
    xyxz = property(lambda self: Vec4.new(self.x, self.y, self.x, self.z))
    xyxw = property(lambda self: Vec4.new(self.x, self.y, self.x, self.w))
    xyyx = property(lambda self: Vec4.new(self.x, self.y, self.y, self.x))
    xyyy = property(lambda self: Vec4.new(self.x, self.y, self.y, self.y))
    xyyz = property(lambda self: Vec4.new(self.x, self.y, self.y, self.z))
    xyyw = property(lambda self: Vec4.new(self.x, self.y, self.y, self.w))
    xyzx = property(lambda self: Vec4.new(self.x, self.y, self.z, self.x))
    xyzy = property(lambda self: Vec4.new(self.x, self.y, self.z, self.y))
    xyzz = property(lambda self: Vec4.new(self.x, self.y, self.z, self.z))
    xyzw = property(lambda self: Vec4.new(self.x, self.y, self.z, self.w))
    xywx = property(lambda self: Vec4.new(self.x, self.y, self.w, self.x))
    xywy = property(lambda self: Vec4.new(self.x, self.y, self.w, self.y))
    xywz = property(lambda self: Vec4.new(self.x, self.y, self.w, self.z))
    xyww = property(lambda self: Vec4.new(self.x, self.y, self.w, self.w))
    xzxx = property(lambda self: Vec4.new(self.x, self.z, self.x, self.x))
    xzxy = property(lambda self: Vec4.new(self.x, self.z, self.x, self.y))
    xzxz = property(lambda self: Vec4.new(self.x, self.z, self.x, self.z))
    xzxw = property(lambda self: Vec4.new(self.x, self.z, self.x, self.w))
    xzyx = property(lambda self: Vec4.new(self.x, self.z, self.y, self.x))
    xzyy = property(lambda self: Vec4.new(self.x, self.z, self.y, self.y))
    xzyz = property(lambda self: Vec4.new(self.x, self.z, self.y, self.z))
    xzyw = property(lambda self: Vec4.new(self.x, self.z, self.y, self.w))
    xzzx = property(lambda self: Vec4.new(self.x, self.z, self.z, self.x))
    xzzy = property(lambda self: Vec4.new(self.x, self.z, self.z, self.y))
    xzzz = property(lambda self: Vec4.new(self.x, self.z, self.z, self.z))
    xzzw = property(lambda self: Vec4.new(self.x, self.z, self.z, self.w))
    xzwx = property(lambda self: Vec4.new(self.x, self.z, self.w, self.x))
    xzwy = property(lambda self: Vec4.new(self.x, self.z, self.w, self.y))
    xzwz = property(lambda self: Vec4.new(self.x, self.z, self.w, self.z))
    xzww = property(lambda self: Vec4.new(self.x, self.z, self.w, self.w))
    xwxx = property(lambda self: Vec4.new(self.x, self.w, self.x, self.x))
    xwxy = property(lambda self: Vec4.new(self.x, self.w, self.x, self.y))
    xwxz = property(lambda self: Vec4.new(self.x, self.w, self.x, self.z))
    xwxw = property(lambda self: Vec4.new(self.x, self.w, self.x, self.w))
    xwyx = property(lambda self: Vec4.new(self.x, self.w, self.y, self.x))
    xwyy = property(lambda self: Vec4.new(self.x, self.w, self.y, self.y))
    xwyz = property(lambda self: Vec4.new(self.x, self.w, self.y, self.z))
    xwyw = property(lambda self: Vec4.new(self.x, self.w, self.y, self.w))
    xwzx = property(lambda self: Vec4.new(self.x, self.w, self.z, self.x))
    xwzy = property(lambda self: Vec4.new(self.x, self.w, self.z, self.y))
    xwzz = property(lambda self: Vec4.new(self.x, self.w, self.z, self.z))
    xwzw = property(lambda self: Vec4.new(self.x, self.w, self.z, self.w))
    xwwx = property(lambda self: Vec4.new(self.x, self.w, self.w, self.x))
    xwwy = property(lambda self: Vec4.new(self.x, self.w, self.w, self.y))
    xwwz = property(lambda self: Vec4.new(self.x, self.w, self.w, self.z))
    xwww = property(lambda self: Vec4.new(self.x, self.w, self.w, self.w))
    yxxx = property(lambda self: Vec4.new(self.y, self.x, self.x, self.x))
    yxxy = property(lambda self: Vec4.new(self.y, self.x, self.x, self.y))
    yxxz = property(lambda self: Vec4.new(self.y, self.x, self.x, self.z))
    yxxw = property(lambda self: Vec4.new(self.y, self.x, self.x, self.w))
    yxyx = property(lambda self: Vec4.new(self.y, self.x, self.y, self.x))
    yxyy = property(lambda self: Vec4.new(self.y, self.x, self.y, self.y))
    yxyz = property(lambda self: Vec4.new(self.y, self.x, self.y, self.z))
    yxyw = property(lambda self: Vec4.new(self.y, self.x, self.y, self.w))
    yxzx = property(lambda self: Vec4.new(self.y, self.x, self.z, self.x))
    yxzy = property(lambda self: Vec4.new(self.y, self.x, self.z, self.y))
    yxzz = property(lambda self: Vec4.new(self.y, self.x, self.z, self.z))
    yxzw = property(lambda self: Vec4.new(self.y, self.x, self.z, self.w))
    yxwx = property(lambda self: Vec4.new(self.y, self.x, self.w, self.x))
    yxwy = property(lambda self: Vec4.new(self.y, self.x, self.w, self.y))
    yxwz = property(lambda self: Vec4.new(self.y, self.x, self.w, self.z))
    yxww = property(lambda self: Vec4.new(self.y, self.x, self.w, self.w))
    yyxx = property(lambda self: Vec4.new(self.y, self.y, self.x, self.x))
    yyxy = property(lambda self: Vec4.new(self.y, self.y, self.x, self.y))
    yyxz = property(lambda self: Vec4.new(self.y, self.y, self.x, self.z))
    yyxw = property(lambda self: Vec4.new(self.y, self.y, self.x, self.w))
    yyyx = property(lambda self: Vec4.new(self.y, self.y, self.y, self.x))
    yyyy = property(lambda self: Vec4.new(self.y, self.y, self.y, self.y))
    yyyz = property(lambda self: Vec4.new(self.y, self.y, self.y, self.z))
    yyyw = property(lambda self: Vec4.new(self.y, self.y, self.y, self.w))
    yyzx = property(lambda self: Vec4.new(self.y, self.y, self.z, self.x))
    yyzy = property(lambda self: Vec4.new(self.y, self.y, self.z, self.y))
    yyzz = property(lambda self: Vec4.new(self.y, self.y, self.z, self.z))
    yyzw = property(lambda self: Vec4.new(self.y, self.y, self.z, self.w))
    yywx = property(lambda self: Vec4.new(self.y, self.y, self.w, self.x))
    yywy = property(lambda self: Vec4.new(self.y, self.y, self.w, self.y))
    yywz = property(lambda self: Vec4.new(self.y, self.y, self.w, self.z))
    yyww = property(lambda self: Vec4.new(self.y, self.y, self.w, self.w))
    yzxx = property(lambda self: Vec4.new(self.y, self.z, self.x, self.x))
    yzxy = property(lambda self: Vec4.new(self.y, self.z, self.x, self.y))
    yzxz = property(lambda self: Vec4.new(self.y, self.z, self.x, self.z))
    yzxw = property(lambda self: Vec4.new(self.y, self.z, self.x, self.w))
    yzyx = property(lambda self: Vec4.new(self.y, self.z, self.y, self.x))
    yzyy = property(lambda self: Vec4.new(self.y, self.z, self.y, self.y))
    yzyz = property(lambda self: Vec4.new(self.y, self.z, self.y, self.z))
    yzyw = property(lambda self: Vec4.new(self.y, self.z, self.y, self.w))
    yzzx = property(lambda self: Vec4.new(self.y, self.z, self.z, self.x))
    yzzy = property(lambda self: Vec4.new(self.y, self.z, self.z, self.y))
    yzzz = property(lambda self: Vec4.new(self.y, self.z, self.z, self.z))
    yzzw = property(lambda self: Vec4.new(self.y, self.z, self.z, self.w))
    yzwx = property(lambda self: Vec4.new(self.y, self.z, self.w, self.x))
    yzwy = property(lambda self: Vec4.new(self.y, self.z, self.w, self.y))
    yzwz = property(lambda self: Vec4.new(self.y, self.z, self.w, self.z))
    yzww = property(lambda self: Vec4.new(self.y, self.z, self.w, self.w))
    ywxx = property(lambda self: Vec4.new(self.y, self.w, self.x, self.x))
    ywxy = property(lambda self: Vec4.new(self.y, self.w, self.x, self.y))
    ywxz = property(lambda self: Vec4.new(self.y, self.w, self.x, self.z))
    ywxw = property(lambda self: Vec4.new(self.y, self.w, self.x, self.w))
    ywyx = property(lambda self: Vec4.new(self.y, self.w, self.y, self.x))
    ywyy = property(lambda self: Vec4.new(self.y, self.w, self.y, self.y))
    ywyz = property(lambda self: Vec4.new(self.y, self.w, self.y, self.z))
    ywyw = property(lambda self: Vec4.new(self.y, self.w, self.y, self.w))
    ywzx = property(lambda self: Vec4.new(self.y, self.w, self.z, self.x))
    ywzy = property(lambda self: Vec4.new(self.y, self.w, self.z, self.y))
    ywzz = property(lambda self: Vec4.new(self.y, self.w, self.z, self.z))
    ywzw = property(lambda self: Vec4.new(self.y, self.w, self.z, self.w))
    ywwx = property(lambda self: Vec4.new(self.y, self.w, self.w, self.x))
    ywwy = property(lambda self: Vec4.new(self.y, self.w, self.w, self.y))
    ywwz = property(lambda self: Vec4.new(self.y, self.w, self.w, self.z))
    ywww = property(lambda self: Vec4.new(self.y, self.w, self.w, self.w))
    zxxx = property(lambda self: Vec4.new(self.z, self.x, self.x, self.x))
    zxxy = property(lambda self: Vec4.new(self.z, self.x, self.x, self.y))
    zxxz = property(lambda self: Vec4.new(self.z, self.x, self.x, self.z))
    zxxw = property(lambda self: Vec4.new(self.z, self.x, self.x, self.w))
    zxyx = property(lambda self: Vec4.new(self.z, self.x, self.y, self.x))
    zxyy = property(lambda self: Vec4.new(self.z, self.x, self.y, self.y))
    zxyz = property(lambda self: Vec4.new(self.z, self.x, self.y, self.z))
    zxyw = property(lambda self: Vec4.new(self.z, self.x, self.y, self.w))
    zxzx = property(lambda self: Vec4.new(self.z, self.x, self.z, self.x))
    zxzy = property(lambda self: Vec4.new(self.z, self.x, self.z, self.y))
    zxzz = property(lambda self: Vec4.new(self.z, self.x, self.z, self.z))
    zxzw = property(lambda self: Vec4.new(self.z, self.x, self.z, self.w))
    zxwx = property(lambda self: Vec4.new(self.z, self.x, self.w, self.x))
    zxwy = property(lambda self: Vec4.new(self.z, self.x, self.w, self.y))
    zxwz = property(lambda self: Vec4.new(self.z, self.x, self.w, self.z))
    zxww = property(lambda self: Vec4.new(self.z, self.x, self.w, self.w))
    zyxx = property(lambda self: Vec4.new(self.z, self.y, self.x, self.x))
    zyxy = property(lambda self: Vec4.new(self.z, self.y, self.x, self.y))
    zyxz = property(lambda self: Vec4.new(self.z, self.y, self.x, self.z))
    zyxw = property(lambda self: Vec4.new(self.z, self.y, self.x, self.w))
    zyyx = property(lambda self: Vec4.new(self.z, self.y, self.y, self.x))
    zyyy = property(lambda self: Vec4.new(self.z, self.y, self.y, self.y))
    zyyz = property(lambda self: Vec4.new(self.z, self.y, self.y, self.z))
    zyyw = property(lambda self: Vec4.new(self.z, self.y, self.y, self.w))
    zyzx = property(lambda self: Vec4.new(self.z, self.y, self.z, self.x))
    zyzy = property(lambda self: Vec4.new(self.z, self.y, self.z, self.y))
    zyzz = property(lambda self: Vec4.new(self.z, self.y, self.z, self.z))
    zyzw = property(lambda self: Vec4.new(self.z, self.y, self.z, self.w))
    zywx = property(lambda self: Vec4.new(self.z, self.y, self.w, self.x))
    zywy = property(lambda self: Vec4.new(self.z, self.y, self.w, self.y))
    zywz = property(lambda self: Vec4.new(self.z, self.y, self.w, self.z))
    zyww = property(lambda self: Vec4.new(self.z, self.y, self.w, self.w))
    zzxx = property(lambda self: Vec4.new(self.z, self.z, self.x, self.x))
    zzxy = property(lambda self: Vec4.new(self.z, self.z, self.x, self.y))
    zzxz = property(lambda self: Vec4.new(self.z, self.z, self.x, self.z))
    zzxw = property(lambda self: Vec4.new(self.z, self.z, self.x, self.w))
    zzyx = property(lambda self: Vec4.new(self.z, self.z, self.y, self.x))
    zzyy = property(lambda self: Vec4.new(self.z, self.z, self.y, self.y))
    zzyz = property(lambda self: Vec4.new(self.z, self.z, self.y, self.z))
    zzyw = property(lambda self: Vec4.new(self.z, self.z, self.y, self.w))
    zzzx = property(lambda self: Vec4.new(self.z, self.z, self.z, self.x))
    zzzy = property(lambda self: Vec4.new(self.z, self.z, self.z, self.y))
    zzzz = property(lambda self: Vec4.new(self.z, self.z, self.z, self.z))
    zzzw = property(lambda self: Vec4.new(self.z, self.z, self.z, self.w))
    zzwx = property(lambda self: Vec4.new(self.z, self.z, self.w, self.x))
    zzwy = property(lambda self: Vec4.new(self.z, self.z, self.w, self.y))
    zzwz = property(lambda self: Vec4.new(self.z, self.z, self.w, self.z))
    zzww = property(lambda self: Vec4.new(self.z, self.z, self.w, self.w))
    zwxx = property(lambda self: Vec4.new(self.z, self.w, self.x, self.x))
    zwxy = property(lambda self: Vec4.new(self.z, self.w, self.x, self.y))
    zwxz = property(lambda self: Vec4.new(self.z, self.w, self.x, self.z))
    zwxw = property(lambda self: Vec4.new(self.z, self.w, self.x, self.w))
    zwyx = property(lambda self: Vec4.new(self.z, self.w, self.y, self.x))
    zwyy = property(lambda self: Vec4.new(self.z, self.w, self.y, self.y))
    zwyz = property(lambda self: Vec4.new(self.z, self.w, self.y, self.z))
    zwyw = property(lambda self: Vec4.new(self.z, self.w, self.y, self.w))
    zwzx = property(lambda self: Vec4.new(self.z, self.w, self.z, self.x))
    zwzy = property(lambda self: Vec4.new(self.z, self.w, self.z, self.y))
    zwzz = property(lambda self: Vec4.new(self.z, self.w, self.z, self.z))
    zwzw = property(lambda self: Vec4.new(self.z, self.w, self.z, self.w))
    zwwx = property(lambda self: Vec4.new(self.z, self.w, self.w, self.x))
    zwwy = property(lambda self: Vec4.new(self.z, self.w, self.w, self.y))
    zwwz = property(lambda self: Vec4.new(self.z, self.w, self.w, self.z))
    zwww = property(lambda self: Vec4.new(self.z, self.w, self.w, self.w))
    wxxx = property(lambda self: Vec4.new(self.w, self.x, self.x, self.x))
    wxxy = property(lambda self: Vec4.new(self.w, self.x, self.x, self.y))
    wxxz = property(lambda self: Vec4.new(self.w, self.x, self.x, self.z))
    wxxw = property(lambda self: Vec4.new(self.w, self.x, self.x, self.w))
    wxyx = property(lambda self: Vec4.new(self.w, self.x, self.y, self.x))
    wxyy = property(lambda self: Vec4.new(self.w, self.x, self.y, self.y))
    wxyz = property(lambda self: Vec4.new(self.w, self.x, self.y, self.z))
    wxyw = property(lambda self: Vec4.new(self.w, self.x, self.y, self.w))
    wxzx = property(lambda self: Vec4.new(self.w, self.x, self.z, self.x))
    wxzy = property(lambda self: Vec4.new(self.w, self.x, self.z, self.y))
    wxzz = property(lambda self: Vec4.new(self.w, self.x, self.z, self.z))
    wxzw = property(lambda self: Vec4.new(self.w, self.x, self.z, self.w))
    wxwx = property(lambda self: Vec4.new(self.w, self.x, self.w, self.x))
    wxwy = property(lambda self: Vec4.new(self.w, self.x, self.w, self.y))
    wxwz = property(lambda self: Vec4.new(self.w, self.x, self.w, self.z))
    wxww = property(lambda self: Vec4.new(self.w, self.x, self.w, self.w))
    wyxx = property(lambda self: Vec4.new(self.w, self.y, self.x, self.x))
    wyxy = property(lambda self: Vec4.new(self.w, self.y, self.x, self.y))
    wyxz = property(lambda self: Vec4.new(self.w, self.y, self.x, self.z))
    wyxw = property(lambda self: Vec4.new(self.w, self.y, self.x, self.w))
    wyyx = property(lambda self: Vec4.new(self.w, self.y, self.y, self.x))
    wyyy = property(lambda self: Vec4.new(self.w, self.y, self.y, self.y))
    wyyz = property(lambda self: Vec4.new(self.w, self.y, self.y, self.z))
    wyyw = property(lambda self: Vec4.new(self.w, self.y, self.y, self.w))
    wyzx = property(lambda self: Vec4.new(self.w, self.y, self.z, self.x))
    wyzy = property(lambda self: Vec4.new(self.w, self.y, self.z, self.y))
    wyzz = property(lambda self: Vec4.new(self.w, self.y, self.z, self.z))
    wyzw = property(lambda self: Vec4.new(self.w, self.y, self.z, self.w))
    wywx = property(lambda self: Vec4.new(self.w, self.y, self.w, self.x))
    wywy = property(lambda self: Vec4.new(self.w, self.y, self.w, self.y))
    wywz = property(lambda self: Vec4.new(self.w, self.y, self.w, self.z))
    wyww = property(lambda self: Vec4.new(self.w, self.y, self.w, self.w))
    wzxx = property(lambda self: Vec4.new(self.w, self.z, self.x, self.x))
    wzxy = property(lambda self: Vec4.new(self.w, self.z, self.x, self.y))
    wzxz = property(lambda self: Vec4.new(self.w, self.z, self.x, self.z))
    wzxw = property(lambda self: Vec4.new(self.w, self.z, self.x, self.w))
    wzyx = property(lambda self: Vec4.new(self.w, self.z, self.y, self.x))
    wzyy = property(lambda self: Vec4.new(self.w, self.z, self.y, self.y))
    wzyz = property(lambda self: Vec4.new(self.w, self.z, self.y, self.z))
    wzyw = property(lambda self: Vec4.new(self.w, self.z, self.y, self.w))
    wzzx = property(lambda self: Vec4.new(self.w, self.z, self.z, self.x))
    wzzy = property(lambda self: Vec4.new(self.w, self.z, self.z, self.y))
    wzzz = property(lambda self: Vec4.new(self.w, self.z, self.z, self.z))
    wzzw = property(lambda self: Vec4.new(self.w, self.z, self.z, self.w))
    wzwx = property(lambda self: Vec4.new(self.w, self.z, self.w, self.x))
    wzwy = property(lambda self: Vec4.new(self.w, self.z, self.w, self.y))
    wzwz = property(lambda self: Vec4.new(self.w, self.z, self.w, self.z))
    wzww = property(lambda self: Vec4.new(self.w, self.z, self.w, self.w))
    wwxx = property(lambda self: Vec4.new(self.w, self.w, self.x, self.x))
    wwxy = property(lambda self: Vec4.new(self.w, self.w, self.x, self.y))
    wwxz = property(lambda self: Vec4.new(self.w, self.w, self.x, self.z))
    wwxw = property(lambda self: Vec4.new(self.w, self.w, self.x, self.w))
    wwyx = property(lambda self: Vec4.new(self.w, self.w, self.y, self.x))
    wwyy = property(lambda self: Vec4.new(self.w, self.w, self.y, self.y))
    wwyz = property(lambda self: Vec4.new(self.w, self.w, self.y, self.z))
    wwyw = property(lambda self: Vec4.new(self.w, self.w, self.y, self.w))
    wwzx = property(lambda self: Vec4.new(self.w, self.w, self.z, self.x))
    wwzy = property(lambda self: Vec4.new(self.w, self.w, self.z, self.y))
    wwzz = property(lambda self: Vec4.new(self.w, self.w, self.z, self.z))
    wwzw = property(lambda self: Vec4.new(self.w, self.w, self.z, self.w))
    wwwx = property(lambda self: Vec4.new(self.w, self.w, self.w, self.x))
    wwwy = property(lambda self: Vec4.new(self.w, self.w, self.w, self.y))
    wwwz = property(lambda self: Vec4.new(self.w, self.w, self.w, self.z))
    wwww = property(lambda self: Vec4.new(self.w, self.w, self.w, self.w))


    # -- SWIZZLE SETTERS -- 

    @xy.setter  # type: ignore -- reportGeneralTypeIssues
    def xy(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = other
        else:
            self.x, self.y = other

    @xz.setter  # type: ignore -- reportGeneralTypeIssues
    def xz(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.z = other
        else:
            self.x, self.z = other

    @xw.setter  # type: ignore -- reportGeneralTypeIssues
    def xw(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.w = other
        else:
            self.x, self.w = other

    @yx.setter  # type: ignore -- reportGeneralTypeIssues
    def yx(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = other
        else:
            self.y, self.x = other

    @yz.setter  # type: ignore -- reportGeneralTypeIssues
    def yz(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.z = other
        else:
            self.y, self.z = other

    @yw.setter  # type: ignore -- reportGeneralTypeIssues
    def yw(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.w = other
        else:
            self.y, self.w = other

    @zx.setter  # type: ignore -- reportGeneralTypeIssues
    def zx(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.x = other
        else:
            self.z, self.x = other

    @zy.setter  # type: ignore -- reportGeneralTypeIssues
    def zy(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.y = other
        else:
            self.z, self.y = other

    @zw.setter  # type: ignore -- reportGeneralTypeIssues
    def zw(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.w = other
        else:
            self.z, self.w = other

    @wx.setter  # type: ignore -- reportGeneralTypeIssues
    def wx(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.x = other
        else:
            self.w, self.x = other

    @wy.setter  # type: ignore -- reportGeneralTypeIssues
    def wy(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.y = other
        else:
            self.w, self.y = other

    @wz.setter  # type: ignore -- reportGeneralTypeIssues
    def wz(self, other: Point2 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.z = other
        else:
            self.w, self.z = other

    @xyz.setter  # type: ignore -- reportGeneralTypeIssues
    def xyz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = self.z = other
        else:
            self.x, self.y, self.z = other

    @xyw.setter  # type: ignore -- reportGeneralTypeIssues
    def xyw(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = self.w = other
        else:
            self.x, self.y, self.w = other

    @xzy.setter  # type: ignore -- reportGeneralTypeIssues
    def xzy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.z = self.y = other
        else:
            self.x, self.z, self.y = other

    @xzw.setter  # type: ignore -- reportGeneralTypeIssues
    def xzw(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.z = self.w = other
        else:
            self.x, self.z, self.w = other

    @xwy.setter  # type: ignore -- reportGeneralTypeIssues
    def xwy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.w = self.y = other
        else:
            self.x, self.w, self.y = other

    @xwz.setter  # type: ignore -- reportGeneralTypeIssues
    def xwz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.w = self.z = other
        else:
            self.x, self.w, self.z = other

    @yxz.setter  # type: ignore -- reportGeneralTypeIssues
    def yxz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = self.z = other
        else:
            self.y, self.x, self.z = other

    @yxw.setter  # type: ignore -- reportGeneralTypeIssues
    def yxw(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = self.w = other
        else:
            self.y, self.x, self.w = other

    @yzx.setter  # type: ignore -- reportGeneralTypeIssues
    def yzx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.z = self.x = other
        else:
            self.y, self.z, self.x = other

    @yzw.setter  # type: ignore -- reportGeneralTypeIssues
    def yzw(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.z = self.w = other
        else:
            self.y, self.z, self.w = other

    @ywx.setter  # type: ignore -- reportGeneralTypeIssues
    def ywx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.w = self.x = other
        else:
            self.y, self.w, self.x = other

    @ywz.setter  # type: ignore -- reportGeneralTypeIssues
    def ywz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.w = self.z = other
        else:
            self.y, self.w, self.z = other

    @zxy.setter  # type: ignore -- reportGeneralTypeIssues
    def zxy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.x = self.y = other
        else:
            self.z, self.x, self.y = other

    @zxw.setter  # type: ignore -- reportGeneralTypeIssues
    def zxw(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.x = self.w = other
        else:
            self.z, self.x, self.w = other

    @zyx.setter  # type: ignore -- reportGeneralTypeIssues
    def zyx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.y = self.x = other
        else:
            self.z, self.y, self.x = other

    @zyw.setter  # type: ignore -- reportGeneralTypeIssues
    def zyw(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.y = self.w = other
        else:
            self.z, self.y, self.w = other

    @zwx.setter  # type: ignore -- reportGeneralTypeIssues
    def zwx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.w = self.x = other
        else:
            self.z, self.w, self.x = other

    @zwy.setter  # type: ignore -- reportGeneralTypeIssues
    def zwy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.w = self.y = other
        else:
            self.z, self.w, self.y = other

    @wxy.setter  # type: ignore -- reportGeneralTypeIssues
    def wxy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.x = self.y = other
        else:
            self.w, self.x, self.y = other

    @wxz.setter  # type: ignore -- reportGeneralTypeIssues
    def wxz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.x = self.z = other
        else:
            self.w, self.x, self.z = other

    @wyx.setter  # type: ignore -- reportGeneralTypeIssues
    def wyx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.y = self.x = other
        else:
            self.w, self.y, self.x = other

    @wyz.setter  # type: ignore -- reportGeneralTypeIssues
    def wyz(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.y = self.z = other
        else:
            self.w, self.y, self.z = other

    @wzx.setter  # type: ignore -- reportGeneralTypeIssues
    def wzx(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.z = self.x = other
        else:
            self.w, self.z, self.x = other

    @wzy.setter  # type: ignore -- reportGeneralTypeIssues
    def wzy(self, other: Point3 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.z = self.y = other
        else:
            self.w, self.z, self.y = other

    @xyzw.setter  # type: ignore -- reportGeneralTypeIssues
    def xyzw(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = self.z = self.w = other
        else:
            self.x, self.y, self.z, self.w = other

    @xywz.setter  # type: ignore -- reportGeneralTypeIssues
    def xywz(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.y = self.w = self.z = other
        else:
            self.x, self.y, self.w, self.z = other

    @xzyw.setter  # type: ignore -- reportGeneralTypeIssues
    def xzyw(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.z = self.y = self.w = other
        else:
            self.x, self.z, self.y, self.w = other

    @xzwy.setter  # type: ignore -- reportGeneralTypeIssues
    def xzwy(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.z = self.w = self.y = other
        else:
            self.x, self.z, self.w, self.y = other

    @xwyz.setter  # type: ignore -- reportGeneralTypeIssues
    def xwyz(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.w = self.y = self.z = other
        else:
            self.x, self.w, self.y, self.z = other

    @xwzy.setter  # type: ignore -- reportGeneralTypeIssues
    def xwzy(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.x = self.w = self.z = self.y = other
        else:
            self.x, self.w, self.z, self.y = other

    @yxzw.setter  # type: ignore -- reportGeneralTypeIssues
    def yxzw(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = self.z = self.w = other
        else:
            self.y, self.x, self.z, self.w = other

    @yxwz.setter  # type: ignore -- reportGeneralTypeIssues
    def yxwz(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.x = self.w = self.z = other
        else:
            self.y, self.x, self.w, self.z = other

    @yzxw.setter  # type: ignore -- reportGeneralTypeIssues
    def yzxw(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.z = self.x = self.w = other
        else:
            self.y, self.z, self.x, self.w = other

    @yzwx.setter  # type: ignore -- reportGeneralTypeIssues
    def yzwx(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.z = self.w = self.x = other
        else:
            self.y, self.z, self.w, self.x = other

    @ywxz.setter  # type: ignore -- reportGeneralTypeIssues
    def ywxz(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.w = self.x = self.z = other
        else:
            self.y, self.w, self.x, self.z = other

    @ywzx.setter  # type: ignore -- reportGeneralTypeIssues
    def ywzx(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.y = self.w = self.z = self.x = other
        else:
            self.y, self.w, self.z, self.x = other

    @zxyw.setter  # type: ignore -- reportGeneralTypeIssues
    def zxyw(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.x = self.y = self.w = other
        else:
            self.z, self.x, self.y, self.w = other

    @zxwy.setter  # type: ignore -- reportGeneralTypeIssues
    def zxwy(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.x = self.w = self.y = other
        else:
            self.z, self.x, self.w, self.y = other

    @zyxw.setter  # type: ignore -- reportGeneralTypeIssues
    def zyxw(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.y = self.x = self.w = other
        else:
            self.z, self.y, self.x, self.w = other

    @zywx.setter  # type: ignore -- reportGeneralTypeIssues
    def zywx(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.y = self.w = self.x = other
        else:
            self.z, self.y, self.w, self.x = other

    @zwxy.setter  # type: ignore -- reportGeneralTypeIssues
    def zwxy(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.w = self.x = self.y = other
        else:
            self.z, self.w, self.x, self.y = other

    @zwyx.setter  # type: ignore -- reportGeneralTypeIssues
    def zwyx(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.z = self.w = self.y = self.x = other
        else:
            self.z, self.w, self.y, self.x = other

    @wxyz.setter  # type: ignore -- reportGeneralTypeIssues
    def wxyz(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.x = self.y = self.z = other
        else:
            self.w, self.x, self.y, self.z = other

    @wxzy.setter  # type: ignore -- reportGeneralTypeIssues
    def wxzy(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.x = self.z = self.y = other
        else:
            self.w, self.x, self.z, self.y = other

    @wyxz.setter  # type: ignore -- reportGeneralTypeIssues
    def wyxz(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.y = self.x = self.z = other
        else:
            self.w, self.y, self.x, self.z = other

    @wyzx.setter  # type: ignore -- reportGeneralTypeIssues
    def wyzx(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.y = self.z = self.x = other
        else:
            self.w, self.y, self.z, self.x = other

    @wzxy.setter  # type: ignore -- reportGeneralTypeIssues
    def wzxy(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.z = self.x = self.y = other
        else:
            self.w, self.z, self.x, self.y = other

    @wzyx.setter  # type: ignore -- reportGeneralTypeIssues
    def wzyx(self, other: Point4 | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            self.w = self.z = self.y = self.x = other
        else:
            self.w, self.z, self.y, self.x = other
