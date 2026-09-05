from arcade import View

from shatter.views.game import GameView
from shatter.context import navigation

class MenuView(View):
    def on_draw(self) -> bool | None:
        from arcade import draw_text

        self.clear()
        draw_text(
            "Main Menu\nPress Anything To Start",
            self.center_x,
            self.center_y,
            multiline=True,
            width=int(self.width),
            align="center",
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if navigation.peek() is self:
            navigation.push(GameView())

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if navigation.peek() is self:
            navigation.push(GameView())
