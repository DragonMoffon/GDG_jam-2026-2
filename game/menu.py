from arcade import View, draw_text

from .chessehc import ChessehcView
from .context import nav
from .rebound import ReboundView


class MenuView(View):
    def __init__(self) -> None:
        super().__init__()
        self.mouse_x: int = 0

    def on_draw(self) -> bool | None:
        self.clear()

        c1 = (255, 255, 255) if self.mouse_x < self.center_x else (125, 125, 125)
        c2 = (125, 125, 125) if self.mouse_x < self.center_x else (255, 255, 255)

        draw_text(
            "Play Chessehc",
            0.25 * self.width,
            self.center_y,
            anchor_x="center",
            anchor_y="center",
            color=c1,
        )

        draw_text(
            "Play Rebound",
            0.75 * self.width,
            self.center_y,
            anchor_x="center",
            anchor_y="center",
            color=c2,
        )

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        self.mouse_x = x

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        self.mouse_x = x

        if self.mouse_x < self.center_y:
            nav.push(ChessehcView())
        else:
            nav.push(ReboundView())
