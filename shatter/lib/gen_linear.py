from pathlib import Path
from itertools import product, permutations
from sys import argv
from typing import Iterable, Literal

# Components of a Vector obj

# * __slots__
# * __init__
# ! arg/radians and angle for Vec2 (? Vec3 and Vec4 as 2-tuple and 3-tuple)
# * new method
# * frozen property
# * length/norm property
# *__abs__
# * normalise/normalize and normalised/normalized
# * dot
# * __matmul__, __rmatmul__, and __imatmul__
# * cross (manually defined for 2d)
# * __bool__ (Always Truthy)
# * __repr__
# * __str__
# ! __complex__ (for 2d)
# ? __format__
# ? __contains__
# * __hash__
# * __eq__
# * __neq__
# * __len__
# * __getitem__
# * __iter__
# * __neg__
# * __add__ / __radd__ etc
# * inplace operations
# * swizzle operators
# * swizzle setters

axis = "xyzw"
type Dim = Literal[2] | Literal[3] | Literal[4]

_HEADER_STR = """# ! DO NOT EDIT DIRECTLY. THIS IS AN AUTO GENERATED FILE !
from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Self, Literal, overload

"""

_CLS_STR = """type Point{dim} = Vec{dim} | tuple[{tpl}]
class Vec{dim}(Sequence[float]):
    __slots__ = {chrs}
"""
_INIT_NONE_STR = "{depth}if {none}:\n{depth}    {eq} = {a}\n{depth}    return\n"
_INIT_SCLR_STR = "{depth}{el}if isinstance({a}, float) or isinstance({a}, int):\n"
_INIT_POINT_STR = "{depth}{el}if isinstance({a}, Vec{dim}) or (isinstance({a}, tuple) and len({a})=={dim}):\n"
def _tabs(depth: int) -> str:
    return f"    {"    "*depth}"
_INIT_STR = """
    def __init__(self, {args}) -> None:
{init}
"""

_NEW_STR = """
    @classmethod
    def new(cls, {args}) -> Vec{dim}:
        vec = cls.__new__(cls)
{vec}
        return vec
"""

_FROZ_STR = """
    @property
    def frozen(self) -> tuple[{tpl}]:
        return {rtrn}
"""

_LEN_STR = """
    # -- LENGTH METHODS --

    @property
    def length_sqr(self) -> float:
        return {len}
    norm_sqr = length_sqr

    @property
    def length(self) -> float:
        return ({len})**0.5
    norm = length

    def __abs__(self) -> float:
        return ({len})**0.5
"""

_NRM_STR = "        self.{a} = self.{a} / l"
_NRMD_STR = "self.{a} / l"
_Vec2_CROSS_STR = "        return -{a2} * {b1} + {a1} * {b2}\n"
_Vec4_CROSS_STR = "        raise NotImplementedError('Vec4 does not implement cross product')"
_Vec3_CROSS_STR = """        a1, a2, a3 = {first}
        b1, b2, b3 = {second}
        return Vec3.new(a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1)
"""

_VEC_STR = """
    # -- VECTOR OPERATORS --

    def normalise(self) -> None:
        l = abs(self)
{normalise}
    normalize = normalise

    def normalised(self) -> Vec{dim}:
        l = abs(self)
        return Vec{dim}.new({normalised})
    normalized = normalised

    def dot(self, other: Point{dim}, /) -> float:
        return {dot}

    def __matmul__(self, other: Point{dim}, /) -> float:
        match other:
            case Vec{dim}():
                return self.dot(other)
            case ({point}):
                return self.dot(other)
        return NotImplemented

    def __rmatmul__(self, other: Point{dim}, /) -> float:
        match other: # Multiplication with Matrix is not commutative even though it is with vectors
            case Vec{dim}():
                return self.dot(other)
            case ({point}):
                return self.dot(other)
        return NotImplemented

    def __imatmul__(self, other: Point2, /):
        return NotImplemented

    def cross(self, other: Point{dim}, /) -> {cross_rtrn}:
{cross}

    def rcross(self, other: Point{dim}, /) -> {cross_rtrn}:
{rcross}
"""

_HASH_STR = """
    # -- HASH METHODS --

    def __hash__(self) -> int:
        return hash(({tpl}))

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Vec{dim}) or isinstance(other, tuple):
            {set} = other
            return {eq}
        return NotImplemented

    def __ne__(self, other: object, /) -> bool:
        if isinstance(other, Vec{dim}) or isinstance(other, tuple):
            {set} = other
            return {ne}
        return NotImplemented
"""

_SEQ_IDX_STR = "        elif idx == {i}:\n            return self.{a}"
_SEQ_ITER_STR = "        yield self.{a}"
_SEQ_STR = """
    # -- SEQUENCE METHODS --

    def __len__(self) -> int:
        return {dim}

    @overload
    def __getitem__(self, idx: int) -> float: ...

    @overload
    def __getitem__(self, idx: slice) -> tuple[float, ...]: ...

    def __getitem__(self, idx: int | slice) -> float | tuple[float, ...]:
        if idx == 0:
            return self.{s1}
{other}
        return ({tpl})[idx]

    def __iter__(self) -> Iterator[float]:
{iter}
"""

_REPR_STR = "{a} = {{self.{a}}}"
_STR_STR = "{{self.{a}}}"
_TYPE_STR = """
    # -- TYPE METHODS --

    def __bool__(self) -> Literal[True]:
        return True

    def __repr__(self) -> str:
        return f"Vec{dim}({args})"

    def __str__(self) -> str:
        return f"<{tpl}>"
"""

_SCALAR_STR = """
    # -- SCALAR OPERATORS --

    def __neg__(self) -> Vec{dim}:
        return Vec{dim}.new({args})
"""

_OP_STR = """
    def __{name}__(self, other: Point{dim} | float, /) -> Vec{dim}:
        match other:
            case Vec{dim}():
                return Vec{dim}.new({vec})
            case float() | int():
                return Vec{dim}.new({sclr})
            case ({point}):
                return Vec{dim}.new({tpl})
        return NotImplemented
"""

_IOP_SET_STR = "                self.{a} {op}= {v}"
_IOP_STR = """
    def __{name}__(self, other: Point{dim} | float, /) -> Vec{dim}:
        match other:
            case Vec{dim}():
{vec}
            case float() | int():
{sclr}
            case ({point}):
{tpl}
        return NotImplemented
"""

_SWIZ_STR = "    {prop} = property(lambda self: Vec{dim}.new({args}))\n"
_SWIZ_EQ_STR = "{set} = other"
_SWIZ_SET_STR = """
    @{prop}.setter  # type: ignore -- reportGeneralTypeIssues
    def {prop}(self, other: Point{dim} | float) -> None:
        if isinstance(other, float) or isinstance(other, int):
            {sclr}
        else:
            {tpl}
"""

def generate_cls(dim: Dim):
    chrs = axis[:dim]
    return _CLS_STR.format(dim=dim, tpl=", ".join("float" for _ in chrs), chrs=tuple(chrs))

def get_init_combinations(dim: Dim):
    chrs = axis[:dim]
    def _chop(rngs: Iterable[int]):
        f = 0
        for e in rngs:
            yield chrs[f:e]
            f = e
        yield chrs[f:]
    splts = product(range(2), repeat=dim-1) # All 'cut' locations to get a unique combination
    rngs = ((i for i, x in enumerate(e, 1) if x == 0) for e in splts) # Ranges for each unique combination
    return (_chop(rng) for rng in rngs)

def generate_init_overload(combination: Iterable[str]):
    yield f"    @overload\n"
    types = ("float" if len(v) == 1 else f"Point{len(v)}" for v in combination)
    yield f"    def __init__(self, {", ".join(f"{axis[i]}: {t}" for i, t in enumerate(types))}): ...\n"

def get_init_args(dim: Dim):
    yield f"{axis[0]}: {" | ".join(("float", *(f"Point{sz}" for sz in range(2, dim+1))))} = 0.0"
    for i in range(dim-1, 0, -1):
        yield f"{axis[dim-i]}: {" | ".join(("float", *(f"Point{sz}" for sz in range(2, i+1)), "None"))} = None"

def generate_init_branch(val: str, branch: dict[str | None, dict], depth: int, el: bool = False):
    if len(val) == 1: # Scalar Case
        yield _INIT_SCLR_STR.format(
            depth=_tabs(depth),
            el="el" if el else "",
            a=val
        )
        yield f"{_tabs(depth+1)}self.{val} = {val}\n"
    elif len(val) > 1: # Vector Case
        yield _INIT_POINT_STR.format(
            depth=_tabs(depth),
            el="el" if el else "",
            dim=len(val),
            a=val[0],
        )
        yield f"{_tabs(depth+1)}{", ".join(f"self.{a}" for a in val)} = {val[0]}\n"
    if not branch:
        yield f"{_tabs(depth+1)}return\n"

    for idx, (key, sub) in enumerate(branch.items()):
        if key is None:
            yield _INIT_NONE_STR.format(
                depth=_tabs(depth+1),
                none=" and ".join(f"{a} is None" for a in axis[1:sub]),
                eq=" = ".join(f"self.{a}" for a in axis[1:sub]),
                a=val
            )
        else:
            yield from generate_init_branch(key, sub, depth+1, idx > 0)

def get_init_branches(dim: Dim, combinations: Iterable[Iterable[str]]):
    tree: dict = {axis[0]: {None: dim}}
    for combination in combinations:
        branch = tree
        for arg in combination:
            if arg not in branch:
                branch[arg] = {}
            branch = branch[arg]
    yield from generate_init_branch("", tree, 0)
    yield f"{_tabs(1)}raise ValueError(f\"Invalid input arguments for Vec{dim}({", ".join(f"{{{a}}}" for a in axis[:dim])})\")"

def generate_init(dim: Dim):
    combinations = get_init_combinations(dim)
    for combination in combinations:
        yield from generate_init_overload(combination)

    chrs = axis[:dim]
    yield _INIT_STR.format(dim=dim, args=", ".join(get_init_args(dim)), init="".join(get_init_branches(dim, get_init_combinations(dim))))
    yield _NEW_STR.format(dim=dim, args=", ".join(f"{c}: float = 0.0" for c in chrs), vec="\n".join(f"        vec.{char} = {char}" for char in chrs))
    yield _FROZ_STR.format(tpl=", ".join("float" for _ in chrs), rtrn=", ".join(f"self.{char}" for char in chrs))

def generate_length(dim: Dim):
    yield _LEN_STR.format(len=" + ".join(f"self.{a}**2" for a in axis[:dim]))

def generate_vec_ops(dim: Dim): # TODO: breakdown into sub functions esp for cross product and matmul
    chrs = axis[:dim]
    normalise = "\n".join(_NRM_STR.format(a=a) for a in chrs)
    normalised = ", ".join(_NRMD_STR.format(a=a) for a in chrs)
    match dim:
        case 2:
            cross_rtrn = "float"
            cross = _Vec2_CROSS_STR.format(a1 = f"self.{chrs[0]}", a2=f"self.{chrs[1]}", b1="other[0]", b2="other[1]")
            rcross = _Vec2_CROSS_STR.format(b1 = f"self.{chrs[0]}", b2=f"self.{chrs[1]}", a1="other[0]", a2="other[1]")
        case 3:
            cross_rtrn = "Vec3"
            cross = _Vec3_CROSS_STR.format(first = "self", second = "other")
            rcross = _Vec3_CROSS_STR.format(first = "other", second = "self")
        case 4:
            cross_rtrn = "Vec4"
            cross = _Vec4_CROSS_STR
            rcross = _Vec4_CROSS_STR
    return _VEC_STR.format(
        dim=dim,
        normalise=normalise,
        normalised=normalised,
        dot=" + ".join(f"self.{a} * other[{i}]" for i,a in enumerate(chrs)),
        point=", ".join("float() | int()" for _ in chrs),
        cross_rtrn=cross_rtrn,
        cross=cross,
        rcross=rcross,
    )

def generate_hash(dim: Dim):
    chrs = axis[:dim]
    return _HASH_STR.format(
        dim=dim,
        tpl=", ".join(f"self.{a}" for a in chrs),
        set=", ".join(f"o{a}" for a in chrs),
        eq=" and ".join(f"self.{a} == o{a}" for a in chrs),
        ne=" or ".join(f"self.{a} != o{a}" for a in chrs)
    )

def generate_sequence(dim: Dim):
    chrs = axis[:dim]
    return _SEQ_STR.format(
        dim=dim,
        s1=f"{chrs[0]}",
        other="\n".join(_SEQ_IDX_STR.format(a=a, i=i) for i, a in enumerate(chrs[1:], 1)),
        tpl=", ".join(f"self.{a}" for a in chrs),
        iter="\n".join(_SEQ_ITER_STR.format(a=a) for a in chrs)
    )

def generate_types(dim: Dim):
    chrs = axis[:dim]
    return _TYPE_STR.format(
        dim=dim,
        args=", ".join(_REPR_STR.format(a=a) for a in chrs),
        tpl=", ".join(_STR_STR.format(a=a) for a in chrs)
    )

def generate_operation(dim: Dim, name: str, op: str, flip: bool = False):
    chrs = axis[:dim]
    point = ", ".join("float() | int()" for _ in chrs)
    if flip:
        vec = ", ".join(f"other.{a} {op} self.{a}" for a in chrs)
        sclr = ", ".join(f"other {op} self.{a}" for a in chrs)
        tpl = ", ".join(f"other[{i}] {op} self.{a}" for i, a in enumerate(chrs))
    else:
        vec = ", ".join(f"self.{a} {op} other.{a}" for a in chrs)
        sclr = ", ".join(f"self.{a} {op} other" for a in chrs)
        tpl = ", ".join(f"self.{a} {op} other[{i}]" for i, a in enumerate(chrs))
    return _OP_STR.format(name=name, dim=dim, vec=vec, sclr=sclr, point=point, tpl=tpl)

def generate_inplace(dim: Dim, name: str, op: str):
    chrs = axis[:dim]
    point = ", ".join("float() | int()" for _ in chrs)
    vec = "\n".join(_IOP_SET_STR.format(a=a, op=op, v=f"other.{a}") for a in chrs)
    sclr = "\n".join(_IOP_SET_STR.format(a=a, op=op, v="other") for a in chrs)
    tpl = "\n".join(_IOP_SET_STR.format(a=a, op=op, v=f"other[{i}]") for i, a in enumerate(chrs))
    return _IOP_STR.format(name=name, dim=dim, vec=vec, sclr=sclr, point=point, tpl=tpl)

# Excludes MatMut as that operates on Matrices and not scalars
_OPS = {
    "add": "+",
    "sub": "-",
    "truediv": "/",
    "mod": "%",
    "floordiv": "//",
    "pow": "**",
}

def generate_operations(dim: Dim):
    yield _SCALAR_STR.format(dim=dim, args=", ".join(f"-self.{a}" for a in axis[:dim]))
    for name, op in _OPS.items():
        yield generate_operation(dim, name, op, False)
        yield generate_operation(dim, f"r{name}", op, True)
        yield generate_inplace(dim, f"i{name}", op)

def generate_swizzle(prop: str):
    return _SWIZ_STR.format(prop=prop, dim=len(prop), args=", ".join(f"self.{a}" for a in prop))
    return f"    {prop} = property(lambda self: Vec{len(prop)}.new({", ".join(f"self.{a}" for a in prop)}))\n"

def generate_swizzles(dim: Dim):
    yield f"\n    # -- SWIZZLE COMBINATIONS --\n"
    chars = axis[:dim]
    swizzles = tuple(product(chars, repeat=i) for i in (2, 3, 4))
    for size in swizzles:
        for swizzle in size:
            yield generate_swizzle("".join(swizzle))
    yield "\n"

def generate_swizzle_setter(prop: str):
    sclr = _SWIZ_EQ_STR.format(set=" = ".join(f"self.{a}" for a in prop))
    tpl = _SWIZ_EQ_STR.format(set=", ".join(f"self.{a}" for a in prop))
    return _SWIZ_SET_STR.format(prop=prop, dim=len(prop), sclr=sclr, tpl=tpl)

def generate_swizzle_setters(dim: Dim):
    yield f"\n    # -- SWIZZLE SETTERS -- \n"
    chars = axis[:dim]
    swizzles = tuple(permutations(chars, i) for i in (2, 3, 4))
    for size in swizzles:
        for swizzle in size:
            yield from generate_swizzle_setter("".join(swizzle))

def create_vector(location: str | Path, dim: Dim = 4, append: bool = False):
    text = (
        *("\n\n" if append else _HEADER_STR),
        *generate_cls(dim),
        *generate_init(dim),
        *generate_length(dim),
        *generate_vec_ops(dim),
        *generate_hash(dim),
        *generate_sequence(dim),
        *generate_types(dim),
        *generate_operations(dim),
        *generate_swizzles(dim),
        *generate_swizzle_setters(dim)
    )
    marker = f"{"a" if append else "w" }t"
    with open(location, marker) as fp:
        fp.writelines(text)

def main():
    path = "vec.py" if len(argv) <= 1 else argv[1]
    create_vector(path, 2, False)
    create_vector(path, 3, True)
    create_vector(path, 4, True)

if __name__ == "__main__":
    main()