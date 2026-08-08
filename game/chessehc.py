from enum import IntEnum, auto
from tomllib import load as load_toml

from arcade import XYWH, LBWH, View, Camera2D, draw_lbwh_rectangle_filled, load_texture, draw_texture_rect
from arcade.types import Color

T_SIZE = 16

FULL_TEXTURES = tuple(
    load_texture(f"resources/chessehc/{piece}.png")
    for piece in ("pawn", "rook", "knight", "bishop", "queen", "king")
)
HOLLOW_TEXTURES = tuple(
    load_texture(f"resources/chessehc/{piece} hollow.png")
    for piece in ("pawn", "rook", "knight", "bishop", "queen", "king")
)
with open("resources/chessehc/boards.toml", "rb") as fp:
    BOARDS: dict[str, list[dict[str, int]]] = load_toml(fp)

class colors:
    first_tile = (202, 166, 131)
    first_piece = (255, 255, 255, 255)
    first_mirror_tile = (147, 172, 236)
    first_mirror_piece = (255, 255, 255, 255)

    second_tile = (76, 47, 12)
    second_piece = (0, 0, 0, 255)
    second_mirror_tile = (12, 24, 76)
    second_mirror_piece = (0, 0, 0, 255)

class PieceType(IntEnum):
    pawn = 0
    rook = auto()
    knight = auto()
    bishop = auto()
    queen = auto()
    king = auto()

class Team(IntEnum):
    first = 0
    second = auto()

class Tile:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.type: PieceType | None = None
        self.team: Team | None = None

class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: tuple[tuple[Tile, ...], ...] = tuple(
            tuple(Tile(x, y) for y in range(self.height)) for x in range(self.width)
        )

        self.horizontal_mirror: int | None = None # Mirror things horizontally
        self.vertical_mirror: int | None = None # Mirror things vertically

    def __getitem__(self, location: tuple[int, int], /) -> Tile | None:
        x = self.mirror_axis(location[0], self.width, self.horizontal_mirror)
        y = self.mirror_axis(location[1], self.height, self.vertical_mirror)
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            return None
        return self.grid[x][y]

    def get[T](self, location: tuple[int, int], default: T = None) -> Tile | T:
        tile = self.__getitem__(location)
        return default if tile is None else tile

    def mirror_axis(self, a: int, size: int, mirror: int | None) -> int:
        if mirror is None:
            return a
        if 0 <= mirror and a < mirror:
            return 2 * mirror - 1 - a
        if mirror <= 0 and size + mirror <= a:
            return 2 * (size + mirror) - 1 - a
        return a

    def is_axis_mirrored(self, a: int, size: int, mirror: int | None) -> bool:
        if mirror is None:
            return False
        return (
            (0 <= mirror and a < mirror)
            or (mirror <= 0 and size + mirror <= a)
        )

    def is_location_mirrored(self, location: tuple[int, int]):
        return bool(
            self.is_axis_mirrored(location[0], self.width, self.horizontal_mirror)
            or self.is_axis_mirrored(location[1], self.height, self.vertical_mirror)
        )

    def get_axis_range(self, size: int, mirror: int | None) -> range:
        if mirror is None:
            return range(size)
        if mirror == 0:
            return range(-size, 2*size)
        return  range(0, 2 * (size + mirror)) if mirror <= 0 else range(2 * mirror - size, size)

    def get_mirrored_ranges(self) -> tuple[range, range]:
        return (
            self.get_axis_range(self.width, self.horizontal_mirror),
            self.get_axis_range(self.height, self.vertical_mirror)
        )

    def draw(self):
        draw_lbwh_rectangle_filled(
            -5,
            -5,
            self.width * T_SIZE + 10,
            self.height * T_SIZE + 10,
            (152, 118, 84),
        )

        rx, ry = self.get_mirrored_ranges()
        for x in rx:
            for y in ry:
                if not (tile := self[x, y]):
                    continue
                tx, ty = tile.x, tile.y
                mirrored = self.is_location_mirrored((x, y))
                second_tile = bool((tx + ty) % 2)
                if mirrored:
                    tc = colors.second_mirror_tile if second_tile else colors.first_mirror_tile
                else:
                    tc = colors.second_tile if second_tile else colors.first_tile
                draw_lbwh_rectangle_filled(x * T_SIZE, y * T_SIZE, T_SIZE, T_SIZE, tc)

                if tile.type is None or tile.team is None:
                    continue

                second_piece = tile.team == Team.second
                if mirrored:
                    pc = colors.second_mirror_piece if second_piece else colors.first_mirror_piece
                else:
                    pc = colors.second_piece if second_piece else colors.first_piece

                draw_texture_rect(FULL_TEXTURES[tile.type], LBWH(x * T_SIZE, y * T_SIZE, T_SIZE,T_SIZE), color=Color.from_iterable(pc), pixelated=True)

class ChessehcView(View):
    def __init__(self):
        super().__init__()
        self.board = Board(8, 8)
        for data in BOARDS.get('regular', ()):
            if not (tile := self.board[data.get("x", -1), data.get("y", -1)]):
                continue
            tile.type = PieceType(data['type']) if 'type' in data else None
            tile.team = Team(data['team']) if 'team' in data else None

        self.camera = Camera2D(projection=XYWH(0, 0, 256, 144))
        self.camera.position = (
            T_SIZE * self.board.width / 2.0,
            T_SIZE * self.board.height / 2.0,
        )

    def on_draw(self) -> bool | None:
        self.clear()
        with self.camera.activate():
            self.board.draw()
