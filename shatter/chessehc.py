from enum import IntEnum, auto
from tomllib import load as load_toml

from arcade import (
    LBWH,
    XYWH,
    Camera2D,
    Text,
    View,
    draw_lbwh_rectangle_filled,
    draw_texture_rect,
    key,
    load_texture,
)
from arcade.types import Color

from .navigation import navigation as nav

T_SIZE = 16
MOUSE_BUFFER = 0.15

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

DEBUG_FONT = "GohuFont 11 Nerd Font Mono"


class colors:
    first_tile = Color(202, 166, 131)
    first_piece = Color(255, 255, 255, 255)
    first_mirror_tile = Color(147, 172, 236)
    first_mirror_piece = Color(255, 255, 255, 255)

    second_tile = Color(76, 47, 12)
    second_piece = Color(0, 0, 0, 255)
    second_mirror_tile = Color(12, 24, 76)
    second_mirror_piece = Color(0, 0, 0, 255)


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

        self.horizontal_mirror: int | None = None  # Mirror things horizontally
        self.vertical_mirror: int | None = None  # Mirror things vertically

        self.alpha = 255

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
        return (0 <= mirror and a < mirror) or (mirror <= 0 and size + mirror <= a)

    def is_location_mirrored(self, location: tuple[int, int]):
        return bool(
            self.is_axis_mirrored(location[0], self.width, self.horizontal_mirror)
            or self.is_axis_mirrored(location[1], self.height, self.vertical_mirror)
        )

    def get_axis_range(self, size: int, mirror: int | None) -> range:
        if mirror is None:
            return range(size)
        if mirror == 0:
            return range(-size, 2 * size)
        return range(0, 2 * (size + mirror)) if mirror <= 0 else range(2 * mirror - size, size)

    def get_mirrored_ranges(self) -> tuple[range, range]:
        return (
            self.get_axis_range(self.width, self.horizontal_mirror),
            self.get_axis_range(self.height, self.vertical_mirror),
        )

    def draw(self):
        draw_lbwh_rectangle_filled(
            -5,
            -5,
            self.width * T_SIZE + 10,
            self.height * T_SIZE + 10,
            (152, 118, 84, self.alpha),
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
                    tc = (
                        colors.second_mirror_tile.replace(a=self.alpha)
                        if second_tile
                        else colors.first_mirror_tile.replace(a=self.alpha)
                    )
                else:
                    tc = (
                        colors.second_tile.replace(a=self.alpha)
                        if second_tile
                        else colors.first_tile.replace(a=self.alpha)
                    )
                draw_lbwh_rectangle_filled(x * T_SIZE, y * T_SIZE, T_SIZE, T_SIZE, tc)

                if tile.type is None or tile.team is None:
                    continue

                second_piece = tile.team == Team.second
                if mirrored:
                    pc = colors.second_mirror_piece if second_piece else colors.first_mirror_piece
                else:
                    pc = colors.second_piece if second_piece else colors.first_piece

                draw_texture_rect(
                    FULL_TEXTURES[tile.type],
                    LBWH(x * T_SIZE, y * T_SIZE, T_SIZE, T_SIZE),
                    color=Color.from_iterable(pc),
                    pixelated=True,
                    alpha=self.alpha,
                )


class ChessehcView(View):
    def __init__(self):
        super().__init__()
        self.board = Board(8, 8)
        for data in BOARDS.get("regular", ()):
            if not (tile := self.board[data.get("x", -1), data.get("y", -1)]):
                continue
            tile.type = PieceType(data["type"]) if "type" in data else None
            tile.team = Team(data["team"]) if "team" in data else None

        self.camera = Camera2D(projection=XYWH(0, 0, 256, 144))
        self.camera.position = (
            T_SIZE * self.board.width / 2.0,
            T_SIZE * self.board.height / 2.0,
        )

        self.tile_x: int | None = None
        self.tile_y: int | None = None
        self.intratile_x: float | None = None
        self.intratile_y: float | None = None

        self.debug = False
        self.debug_text = Text(
            "DEBUG",
            5,
            self.height - 5,
            font_size=11,
            anchor_y="top",
            font_name=DEBUG_FONT,
            multiline=True,
            width=self.width / 2,
        )

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        x, y = int(x), int(y)  # typing is lying these are floats until you do this
        cam_x, cam_y, _ = self.camera.unproject((x, y))
        intratile_x, intratile_y = round(cam_x / T_SIZE % 1, 3), round(cam_y / T_SIZE % 1, 3)
        cam_x, cam_y = int(cam_x / T_SIZE), int(cam_y / T_SIZE)
        tile = self.board.get((cam_x, cam_y))
        if tile and not self.board.is_location_mirrored((tile.x, tile.y)):
            self.tile_x = tile.x
            self.tile_y = tile.y
            self.intratile_x = intratile_x
            self.intratile_y = intratile_y
            self.debug_text.text = (
                f"({x}, {y})\nTILE: ({tile.x}, {tile.y})\nINTRA: ({intratile_x}, {intratile_y})"
            )
        else:
            self.tile_x, self.tile_y, self.intratile_x, self.intratile_y = None, None, None, None
            self.debug_text.text = f"({x}, {y})\nTILE: None)"

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if (
            self.tile_x is None
        ):  # I'm not checking all the variables here but the assumption is tile_y and the intratile_'s are also None
            self.board.horizontal_mirror = None
            self.board.vertical_mirror = None
            return

        dir = None
        if self.intratile_x < MOUSE_BUFFER:
            dir = "left"
        elif self.intratile_x > (1 - MOUSE_BUFFER):
            dir = "right"
        elif self.intratile_y < MOUSE_BUFFER:
            dir = "bottom"
        elif self.intratile_y > (1 - MOUSE_BUFFER):
            dir = "top"
        else:
            pass

        match dir:
            case "left":
                self.board.horizontal_mirror = self.tile_x
                self.board.vertical_mirror = None
            case "right":
                self.board.horizontal_mirror = -(7 - self.tile_x)
                self.board.vertical_mirror = None
            case "bottom":
                self.board.horizontal_mirror = None
                self.board.vertical_mirror = self.tile_y
            case "top":
                self.board.horizontal_mirror = None
                self.board.vertical_mirror = -(7 - self.tile_y)
            case _:
                self.board.horizontal_mirror = None
                self.board.vertical_mirror = None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        match symbol:
            case key.D:
                self.debug = not self.debug
            case key.BACKSPACE:
                nav.pop()

    def on_draw(self) -> bool | None:
        self.clear()
        with self.camera.activate():
            self.board.draw()
        if self.debug:
            self.debug_text.draw()
