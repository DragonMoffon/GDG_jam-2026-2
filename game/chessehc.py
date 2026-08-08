from arcade import View, Camera2D, draw_lbwh_rectangle_filled

TILE_SIZE = 32


class Tile:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: tuple[tuple[Tile, ...], ...] = tuple(
            tuple(Tile(x, y) for y in range(self.height)) for x in range(self.width)
        )

        self.mirror_slice: int | None = None

    def __getitem__(self, location: tuple[int, int]) -> Tile:
        x, y = location
        if self.mirror_slice is None:
            return self.grid[x][y]

        if 0 <= self.mirror_slice and x < self.mirror_slice:
            x = (2 * self.mirror_slice) - 1 - x

        if self.mirror_slice <= 0 and self.width + self.mirror_slice <= x:
            x = (2 * (self.width + self.mirror_slice)) - 1 - x

        if not (0 <= x < self.width) or not (0 <= y < self.height):
            return None

        return self.grid[x][y]

    def __str__(self):
        lines = (", ".join(str(self[x, y]) for x in range(self.width)) for y in range(self.height))
        return "\n".join(lines)


class ChessehcView(View):
    def __init__(self):
        super().__init__()
        self.board = Board(8, 8)
        self.board.mirror_slice = -2

        self.camera = Camera2D()
        self.camera.position = (
            TILE_SIZE * self.board.width / 2.0,
            TILE_SIZE * self.board.height / 2.0,
        )

        print(str(self.board))

    def on_draw(self) -> bool | None:
        self.clear()
        with self.camera.activate():
            draw_lbwh_rectangle_filled(
                -15,
                -15,
                self.board.width * TILE_SIZE + 30,
                self.board.height * TILE_SIZE + 30,
                (152, 118, 84),
            )
            for x in range(self.board.width):
                for y in range(self.board.height):
                    color = (255, 255, 255) if (x + y) % 2 == 0 else (0, 0, 0)
                    draw_lbwh_rectangle_filled(
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, color
                    )
